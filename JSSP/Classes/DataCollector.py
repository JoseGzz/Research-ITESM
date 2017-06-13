class DataCollector:
	def __init__(self, filename, file_type="csv"):
		"""Default constructor"""
		self._filename = filename
		self._file_type = file_type
		self._data_added = False

		# open file to store data
		self._file = open(self._filename, "w")

	def __init__(self, filename, file_type="csv", cols=None):
		"""Constructor with column names defined"""
		self.__init__(filename, file_type)

		if cols:
			for colname in cols:
				self._file.write(str(colname).rstrip('\n'))
				self._file.write(", ".rstrip('\n'))

	def new_entry(self):
		"""This method should be called each time a new entry or line
		must be written. It merely writes a newline in the file."""
		self._file.write("")

	def add_data(self, data):
		"""Calling this method adds one data element in the next column of the entry,
		notice it adds one extra comma at the end of the line, so for the last column you should
		call instead add_last_data method"""
		self._file.write(str(data).rstrip('\n'))
		self._file.write(", ".rstrip('\n'))

	def add_last_data(self, data):
		"""Calling this method adds the last data element of the entry,
		notice that it should only be called once at the end of the entry, once all other data
		has been collected"""
		self._file.write(str(data))

	def close_file(self):
		"""Calling this method closes the file if it is open to free program resources"""
		if not self._file.closed:
			self._file.close()
