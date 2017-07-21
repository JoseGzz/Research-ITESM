import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

from TT.Classes.solutions.tt_solution.restrictions.same_room_and_time import SameRoomAndTime
from TT.Classes.solutions.tt_solution.restrictions.same_students import SameStudents
from TT.Classes.solutions.tt_solution.types import Day


class TtPlotter:
    def __init__(self):
        self.plots = []
        self.first_time = True
        self.days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        
        for fig_index, day in enumerate(self.days):
            fig = plt.figure(fig_index)
            self._set_axis(fig, day)
            self.plots.append(fig)
    
    def assign_time_slot(self, event, solution, fig):
        ax1 = fig.gca()
        rooms = solution.state['rooms']
        
        room_index = 0
        for i, room in rooms.items():
            if room.uid == event.room:
                break
            room_index += 1

        if SameRoomAndTime().is_violated(solution, event) or SameStudents().is_violated(solution, event):
            color = 'red'
        else:
            color = 'green'

        ax1.add_patch(
            patches.Rectangle(
                (room_index, (0.5 + (20.5 - (event.start_time // 12)) * 2) - (event.duration / 12.0) - 1),  # (x,y)
                1,  # width
                event.duration / 6.0,  # height
                color=color
            )
        )

    def plot(self, solution):
        for i, fig in enumerate(self.plots):
            fig = plt.figure(i)
            plt.clf()
            self._set_axis(fig, self.days[i])
            
            for k, events in solution.solution_space.items():
                for event in events:
                    if i == 0 and event.day == Day.Monday:
                        self.assign_time_slot(event, solution, fig)
                    if i == 1 and event.day == Day.Tuesday:
                        self.assign_time_slot(event, solution, fig)
                    if i == 2 and event.day == Day.Wednesday:
                        self.assign_time_slot(event, solution, fig)
                    if i == 3 and event.day == Day.Thursday:
                        self.assign_time_slot(event, solution, fig)
                    if i == 4 and event.day == Day.Friday:
                        self.assign_time_slot(event, solution, fig)
                    
            if self.first_time:
                plt.show()
            else:
                plt.show()
                fig.canvas.draw()
                plt.pause(0.1)

        self.first_time = False
        
    @staticmethod
    def _set_axis(fig, day):
        fig.set_size_inches(8, 6)
        fig.suptitle(day, fontsize=12)
        
        x_labels = [i for i in range(81)]
        y_labels = []
        for time in range(16):
            time = 21 - time
            y_labels.append("{0}:00".format(time))
            y_labels.append("{0}:30".format(time - 1))
    
        ax = fig.gca()
        ax.set_xlabel('Locations')
        ax.set_ylabel('Time Slots')
        ax.set_xticklabels('')
        ax.set_xticks([i + 0.5 for i in range(82)], minor=True)
        ax.set_xticklabels(x_labels, minor=True)
    
        plt.yticks(np.arange(0.5, 31, 1), y_labels)
        plt.xticks(np.arange(0, 82, 1))
        plt.rc('grid', linestyle="-", color='black')
        plt.grid(True)
        plt.ion()
