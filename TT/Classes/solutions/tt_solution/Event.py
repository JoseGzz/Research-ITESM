class Event:
    @property
    def day(self):
        return self._day
    
    @property
    def start_time(self):
        return self._start_time
    
    @property
    def duration(self):
        return self._duration
    
    @property
    def instructor(self):
        return self._instructor
    
    @property
    def room(self):
        return self._room
    
    @property
    def uid(self):
        return self._class_id
    
    def __init__(self, day, start_time, duration, room, uid, instructor=None):
        self._day = day
        self._start_time = start_time
        self._duration = duration
        self._room = room
        self._instructor = instructor
        self._class_id = uid
