import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import matplotlib as mpl

from TT.Classes.solutions.tt_solution.restrictions.same_room_and_time import SameRoomAndTime
from TT.Classes.solutions.tt_solution.restrictions.same_students import SameStudents
from TT.Classes.solutions.tt_solution.types import Day

from matplotlib.colors import LinearSegmentedColormap
import matplotlib.colors
from palettable.cubehelix import perceptual_rainbow_16_r


class TtPlotter:
    def __init__(self):
        self.plots = []
        self.first_time = True
        self.days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        self.constraints = []
        self.soft_constraints = []
        self.cmap = perceptual_rainbow_16_r.get_mpl_colormap().from_list("color_list",
                                                                    perceptual_rainbow_16_r.mpl_colors, N=100)
        self.colors = matplotlib.colors.makeMappingArray(N=100, data=self.cmap)
        
        for fig_index, day in enumerate(self.days):
            fig = plt.figure(fig_index)
            ax1 = plt.subplot2grid((1, 8), (0, 0), colspan=6)
            ax2 = plt.subplot2grid((1, 8), (0, 7), colspan=1)
            
            self._set_axis(fig, ax1, day)
            self.plots.append((fig, ax1, ax2))
            
    def register_constraints(self, constraints):
        self.constraints = constraints
        
    def register_soft_constraints(self, constraints):
        self.soft_constraints = constraints
        
    def is_feasible(self, solution, event):
        for constraint in self.constraints:
            if constraint.is_violated(solution, event):
                return False
        
        return True
    
    def get_cost(self, solution, event):
        result = 0
        for soft_c in self.soft_constraints:
            result += soft_c.cost(solution, event)
            
        if result < 0:
            return self.colors[0]
        elif result > 99:
            return self.colors[99]
        else:
            return self.colors[int(result)]
    
    def assign_time_slot(self, event, solution, ax1):
        rooms = solution.state['rooms']
        
        room_index = 0
        for i, room in rooms.items():
            if room.uid == event.room:
                break
            room_index += 1

        if not self.is_feasible(solution, event):
            color = 'red'
        else:
            color = self.get_cost(solution, event)

        ax1.add_patch(
            patches.Rectangle(
                (room_index, (0.5 + (20.5 - (event.start_time // 12)) * 2) - (event.duration / 12.0) - 1),  # (x,y)
                1,                      # width
                event.duration / 6.0,   # height
                color=color
            )
        )

    def plot(self, solution):
        for i, (_, _, _) in enumerate(self.plots):
            fig = plt.figure(i)
            ax1 = plt.subplot2grid((1, 8), (0, 0), colspan=6)
            ax2 = plt.subplot2grid((1, 8), (0, 7), colspan=1)
            
            self._set_axis(fig, ax1, self.days[i])
            
            for k, events in solution.solution_space.items():
                for event in events:
                    if i == 0 and event.day == Day.Monday:
                        self.assign_time_slot(event, solution, ax1)
                    if i == 1 and event.day == Day.Tuesday:
                        self.assign_time_slot(event, solution, ax1)
                    if i == 2 and event.day == Day.Wednesday:
                        self.assign_time_slot(event, solution, ax1)
                    if i == 3 and event.day == Day.Thursday:
                        self.assign_time_slot(event, solution, ax1)
                    if i == 4 and event.day == Day.Friday:
                        self.assign_time_slot(event, solution, ax1)

            plt.ion()
            if self.first_time:
                plot_cmap(self.cmap, 100, ax2)
                plt.show()
                
                plt.pause(0.1)
            else:
                plot_cmap(self.cmap, 100, ax2)
                plt.show()
                fig.canvas.draw()
                
                plt.pause(0.1)
                
        self.first_time = False
        
    def _set_axis(self, fig, ax, day):
        fig.suptitle(day, fontsize=12)
        
        x_labels = [i for i in range(81)]
        y_labels = []
        for time in range(16):
            time = 21 - time
            y_labels.append("{0}:00".format(time))
            y_labels.append("{0}:30".format(time - 1))
    
        ax.set_xlabel('Locations')
        ax.set_ylabel('Time Slots')
        ax.set_xticklabels('')
        ax.set_xticks([i + 0.5 for i in range(82)], minor=True)
        ax.set_xticklabels(x_labels, minor=True)
    
        ax.set_yticklabels('')
        ax.set_yticks(np.arange(0.5, 31, 1), minor=True)
        ax.set_yticklabels(y_labels, minor=True)
        ax.set_xticks(np.arange(0, 82, 1))

        ax.grid(linestyle="-", color='black')


def plot_cmap(cmap, ncolor, ax):
    """
    A convenient function to plot colors of a matplotlib cmap

    Args:
        ncolor (int): number of color to show
        cmap: a cmap object or a matplotlib color name
    """

    if isinstance(cmap, str):
        try:
            cm = plt.get_cmap(cmap)
        except ValueError:
            print("WARNINGS :", cmap, " is not a known colormap")
            cm = plt.cm.gray
    else:
        cm = cmap

    with mpl.rc_context(mpl.rcParamsDefault):
        ax.pcolor(np.linspace(1, ncolor, ncolor).reshape(ncolor, 1), cmap=cm)
        ax.set_title(cm.name)
        ax.set_xticks([])
        ax.set_yticks(list(np.arange(0, 110, 10)))
