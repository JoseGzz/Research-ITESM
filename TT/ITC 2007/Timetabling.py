import numpy as np
from formatter import Formatter

class Timetabling():
	"""properties inicialization"""
	def __init__(self, file_name="", events=0, rooms=0, features=0, students=0, timeslots=0,
		room_capacities=0, student_event=None, room_feature=None, event_feature=None, event_timeslot=None, event_event=None):
		self.file_name = "comp-2007-2-1.tim"
		# quantities
		self.events          = events
		self.rooms           = rooms
		self.features        = features
		self.students        = students
		self.timeslots       = timeslots
		self.room_capacities = room_capacities
		# matrixes
		self.student_event  = student_event 
		self.room_feature   = room_feature
		self.event_feature  = event_feature
		self.event_timeslot = event_timeslot
		self.event_event    = event_event
		# object lists
		self.event_list    = []
		self.rooms_list    = []
		self.features_list = []
		self.students_list = []
		self.timeslot_list = []
		# execution functions
		self.read_data()
		self.create_matrixes()
		self.create_objects()

	"""read data from file"""
	def read_data(self):
		count = len(open(self.file_name).readlines())
		with open(self.file_name, 'r+') as f:
			no_elements = f.readline().split()
			# set quantitites
			self.events   = int(no_elements[0])
			self.rooms    = int(no_elements[1])
			self.features = int(no_elements[2])
			self.students = int(no_elements[3])
			# calculate number of available timeslots
			self.timeslots = int((count - (1 + self.rooms + self.events * self.students +
				self.rooms * self.features + self.events * self.features + self.events * self.events)) / self.events)
			# create lists with values from file to create the matrixes
			self.room_capacities = np.array([next(f).strip() for _ in range(self.rooms)])
			self.student_event   = np.array([next(f).strip() for _ in range(self.events * self.students)])
			self.room_feature    = np.array([next(f).strip() for _ in range(self.rooms  * self.features)])
			self.event_feature   = np.array([next(f).strip() for _ in range(self.events * self.features)])
			self.event_timeslot  = np.array([next(f).strip() for _ in range(self.events * self.timeslots)])
			self.event_event     = np.array([next(f).strip() for _ in range(self.events * self.events)])

	"""create matrixes from input"""
	def create_matrixes(self):
		self.student_event  = np.reshape(self.student_event , (self.students, self.events))
		self.room_feature   = np.reshape(self.room_feature  , (self.rooms   , self.features))
		self.event_feature  = np.reshape(self.event_feature , (self.events  , self.features))
		self.event_timeslot = np.reshape(self.event_timeslot, (self.events  , self.timeslots))
		self.event_event    = np.reshape(self.event_event   , (self.events  , self.events))

	"""generate object lists"""
	def create_objects(self):
		formatter = Formatter(self.events, self.students, self.rooms, self.features, self.timeslots)
		# assign ids to objects
		self.event_list    = formatter.create_events()
		self.rooms_list    = formatter.create_rooms()
		self.features_list = formatter.create_features()
		self.students_list = formatter.create_students()
		self.timeslot_list = formatter.create_timeslots()
		# assign object features
		self.rooms_list                = formatter.set_capacities        (self.rooms_list, self.room_capacities)
		self.event_list, students_list = formatter.set_attendance        (self.event_list, self.students_list, self.student_event)
		self.rooms_list, features_list = formatter.set_features          (self.rooms_list, self.features_list, self.room_feature)
		self.event_list, features_list = formatter.set_requirements      (self.event_list, self.features_list, self.event_feature)
		self.event_list, timeslot_list = formatter.set_possible_timeslots(self.event_list, self.timeslot_list, self.event_timeslot)
		self.event_list                = formatter.set_precedence        (self.event_list, self.event_event)

		"""
		for room in rooms_list:
			print(room.capacity) 
		"""

Timetabling()