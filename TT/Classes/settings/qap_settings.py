# -*- coding: utf-8 -*-
from optparse import OptionParser as Op
from data_collector import DataCollector

options = None


def init():
    """This function initializes all the inital settings and values that the program may need when it starts."""
    
    # set the parse to accept the collect data option to true
    parser = Op()
    # collect data
    parser.add_option("-c", "--collect", action="store_true", dest="collect_data", default=False)
    # set debugging to true
    parser.add_option("-d", "--debug", action="store_true", dest="debug", default=False)
    # set trace display to false, since it is a default option
    parser.add_option("-t", "--trace", action="store_true", dest="trace", default=False)
    # set search function to use
    parser.add_option("--func", action="store", type="string", dest="function", default="RANDOM")
    # set file to which the input data should be obtained
    parser.add_option("--df", action="store", type="string", dest="data_filename")
    # set file to which the collected data should be stored
    parser.add_option("--cf", action="store", type="string", dest="collect_filename")
    parser.add_option("--seed", action="store", type="long", dest="seed", default=123456789)
    parser.add_option("--special", action="store_true", dest="special", default=False)
    parser.add_option("-k", action="store", dest="k", type="long", default=3)
    parser.add_option("--temp", action="store", dest="temp_rate", type="float", default=0.9)
    parser.add_option("--iters", action="store", dest="iters", type="float", default=100)
    parser.add_option("--max_t", action="store", dest="max_temp", type="float", default=100)
    parser.add_option("--min_t", action="store", dest="min_temp", type="float", default=0.5)
    parser.add_option("--hh", action="store", type="string", dest="hh")
    
    global options
    (options, _) = parser.parse_args()

# data collector configuration
global collector
collector = DataCollector()
