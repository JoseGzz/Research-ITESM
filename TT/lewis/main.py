import numpy as np
from formatter import Formatter

def main():
	file_name  = "comp-2007-2-1.tim"
	count      = len(open(file_name).readlines())

	with open(file_name, 'r+') as f:
		no_elements = f.readline().split()
		events    = int(no_elements[0])
		rooms     = int(no_elements[1])
		features  = int(no_elements[2])
		students  = int(no_elements[3])
		timeslots = int((count - (1 + rooms + events * students + rooms * features + events * features + events * events)) / events)
		room_capacities = np.array([next(f).strip() for _ in range(rooms)])
		student_event   = np.array([next(f).strip() for _ in range(events * students)])
		room_feature    = np.array([next(f).strip() for _ in range(rooms  * features)])
		event_feature   = np.array([next(f).strip() for _ in range(events * features)])
		event_timeslot  = np.array([next(f).strip() for _ in range(events * timeslots)])
		event_event     = np.array([next(f).strip() for _ in range(events * events)])
		
		student_event  = np.reshape(student_event , (students, events))
		room_feature   = np.reshape(room_feature  , (rooms   , features))
		event_feature  = np.reshape(event_feature , (events  , features))
		event_timeslot = np.reshape(event_timeslot, (events  , timeslots))
		event_event    = np.reshape(event_event   , (events  , events))

		formatter     = Formatter(events, students, rooms, features, timeslots)
		event_list    = formatter.create_events()
		rooms_list    = formatter.create_rooms()
		features_list = formatter.create_features()
		students_list = formatter.create_students()
		timeslot_list = formatter.create_timeslots()

		rooms_list                = formatter.set_capacities(rooms_list, room_capacities)
		event_list, students_list = formatter.set_attendance(event_list, students_list, student_event)
		rooms_list, features_list = formatter.set_features(rooms_list, features_list, room_feature)
		event_list, features_list = formatter.set_requirements(event_list, features_list, event_feature)
		event_list, timeslot_list = formatter.set_possible_timeslots(event_list, timeslot_list, event_timeslot)
		event_list                = formatter.set_precedence(event_list, event_event)


		"""
		for room in rooms_list:
			print(room.capacity) 
		"""

if __name__ == "__main__":
    main()