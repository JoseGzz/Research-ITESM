class Event():
	def __init__(self, event_id=0, before=None, after=None):
		self.student_list = []
		self.required_features = []
		self.possible_time_slots = []
		self.event_id = event_id
		self.before = before
		self.after = after
