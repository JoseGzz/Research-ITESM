from optparse import OptionParser as OP


def init():
	"""This function initializes all the inital settings and values that the program may need when it starts."""

	# set the parse to accept the collect data option to true
	parser = OP()
	# collect data
	parser.add_option("-c", "--collect", action="store_true", dest="collect_data", default=False)
	# set debugging to true
	parser.add_option("-d", "--debug", action="store_true", dest="debug", default=False)
	# set trace display to false, since it is a default option
	parser.add_option("-t", "--trace", action="store_true", dest="trace", default=False)

	global options
	(options, _) = parser.parse_args()