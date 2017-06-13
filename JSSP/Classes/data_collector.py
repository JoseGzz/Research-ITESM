class DataCollector:
    def __init__(self):
        """The default constructor of the class.
        
        entries: a list that stores the information for each entry.
        columns: a set that stores all columns seen to that moment.
        current_entry: an integer that points to the current entry
            index in the entries list."""
        self._entries = []
        self._columns = set()
        self._current_entry = -1

    def new_entry(self):
        """This method creates a new space for an entry. It should always be called
        before the add_data method or the data might get corrupted"""
        self._current_entry += 1
        self._entries.append({})
    
    def add_data(self, key, data):
        """Calling this method adds one data element in the next column of the entry,
        notice it adds one extra comma at the end of the line, so for the last column you should
        call instead add_last_data method"""
        try:
            self._columns.add(key)
            self._entries[self._current_entry][key] = data
        except:
            raise UserWarning("A new entry must be created before calling add_data.")
    
    def write_to_file(self, filename):
        """Calling this method writes the stored data into the specified file and then
        closes it to free program resources."""
        self._write_to_file(filename)

    def append_to_file(self, filename):
        """Calling this method appends the stored data into the specified file (if it does not
         exists it just creates a new one) and then closes it to free program resources."""
        self._write_to_file(filename, "a")

    def _write_to_file(self, filename, mode="w"):
        """adds the stored data into the specified file via the specified open mode
        and then closes it to free program resources. Note that it adds an extra column
        for the index."""
        with open(filename, mode) as file:
            # write the column names in the first line of the file
            file.write("index".rstrip('\n'))
            file.write(", ".rstrip('\n'))
            
            for column in self._columns:
                file.write(str(column).rstrip('\n'))
                file.write(", ".rstrip('\n'))
            file.write("\n")
        
            # for each entry, write its content in the column order speified above
            index = 0
            for entry in self._entries:
                file.write(str(index).rstrip('\n'))
                file.write(", ".rstrip('\n'))
                index += 1
                
                for column in self._columns:
                    if column in entry:
                        file.write(str(entry[column]).rstrip('\n'))
                        file.write(", ".rstrip('\n'))
                    else:
                        file.write(", ".rstrip('\n'))
                file.write("\n")
