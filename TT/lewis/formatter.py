from student  import Student
from event    import Event
from room     import Room
from feature  import Feature
from timeslot import Timeslot
class Formatter():
	def __init__(self, no_events, no_students, no_rooms, no_features, no_timeslots):
		self.no_events    = no_events
		self.no_students  = no_students
		self.no_rooms     = no_rooms
		self.no_features  = no_features
		self.no_timeslots = no_timeslots

	def set_capacities(self, rooms_list, capacities):
		for room, capacity in zip(rooms_list, capacities):
			room.capacity = capacity
		return rooms_list

	def set_attendance(self, event_list, student_list, student_event_mat):
		for event in event_list:
			for student in student_list:
				if student_event_mat[student.student_id][event.event_id] == 1:
					event.student_list.append(student)
					student.event_list.append(event)
		return event_list, student_list

	def set_features(self, room_list, feature_list, room_feature_mat):
		for room in room_list:
			for feature in feature_list:
				if room_feature_mat[room.room_id][feature.feature_id] == 1:
					room.feature_list.append(feature)
					feature.rooms_list.append(room)
		return room_list, feature_list

	def set_requirements(self, event_list, feature_list, event_feature_mat):
		for event in event_list:
			for feature in feature_list:
				if event_feature_mat[event.event_id][feature.feature_id] == 1:
					event.required_features.append(feature)
					feature.required_by.append(room)
		return event_list, feature_list

	def set_possible_timeslots(self, event_list, timeslot_list, event_timeslot_mat):
		for event in event_list:
			for slot in timeslot_list:
				if event_timeslot_mat[event.event_id][slot.timeslot_id] == 1:
					event.possible_timeslots.append(slot)
					slot.required_by.append(room)
		return event_list, timeslot_list

	def set_precedence(self, event_list, event_event_m):
		for i in range(len(event_event_m)):
			for j in range(len(event_event_m[i])):
				if event_event_m[i][j] == 1:
					event_list[i].before = event_list[j]
					event_list[j].after = event_list[i]
				elif event_event_m[i][j] == -1:
					event_list[i].after  = event_list[j]
					event_list[j].before = event_list[i]
		return event_list

	def create_events(self):
		return [Event(event_id=event) for event in range(self.no_events)]

	def create_students(self):
		return [Student(student_id=student) for student in range(self.no_students)]

	def create_rooms(self):
		return [Room(room_id=room) for room in range(self.no_rooms)]

	def create_features(self):
		return [Feature(feature_id=feature) for feature in range(self.no_features)]

	def create_timeslots(self):
		return [Timeslot(timeslot_id=slot) for slot in range(self.no_timeslots)]