import numpy as np

def main():
	file_name  = "comp-2007-2-1.tim"
	count      = len(open(file_name).readlines())

	with open(file_name, 'r+') as f:
		no_elements = f.readline().split()
		events    = int(no_elements[0])
		rooms     = int(no_elements[1])
		features  = int(no_elements[2])
		students  = int(no_elements[3])
		timeslots = (count - (1 + rooms + events * students + rooms * features + events * features + events * events)) / events
		room_capacities = np.array([next(f).strip() for _ in xrange(rooms)])
		student_event   = np.array([next(f).strip() for _ in xrange(events * students)])
		room_feature    = np.array([next(f).strip() for _ in xrange(rooms  * features)])
		event_feature   = np.array([next(f).strip() for _ in xrange(events * features)])
		event_timeslot  = np.array([next(f).strip() for _ in xrange(events * timeslots)])
		event_event     = np.array([next(f).strip() for _ in xrange(events * events)])
		
		student_event  = np.reshape(student_event , (students, events))
		room_feature   = np.reshape(room_feature  , (rooms,    features))
		event_feature  = np.reshape(event_feature , (events,   features))
		event_timeslot = np.reshape(event_timeslot, (events,   timeslots))
		event_event    = np.reshape(event_event   , (events,   events))

if __name__ == "__main__":
    main()