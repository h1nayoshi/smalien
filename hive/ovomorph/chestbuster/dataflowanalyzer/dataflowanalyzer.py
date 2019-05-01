# -*- coding: utf-8 -*-
# Called by chestbuster.py

from pprint import pprint

from . import dataflowfuncs as dffuncs
from . import dataflowfinder as dffinder
from . import dataflowimpfinder as dfifinder
from . import dataflowsinkfinder as dfsfinder

class DataFlowAnalyzer(dffuncs.DFFuncs, dffinder.DFFinder, dfifinder.DFIFinder, dfsfinder.DFSFinder):
  def __init__(self, parsed_data):
    self.parsed_data = parsed_data

    self.data_flows = {}
    self.__init_data_flows()

  def __init_data_flows(self):
    for class_path, cval in self.parsed_data.items():
      self.data_flows[class_path] = {}
      for method, mval in cval['methods'].items():
        self.data_flows[class_path][method] = {}

  def analyze(self):
    # Find data flows
    for class_path, cval in self.parsed_data.items():
      for method, mval in cval['methods'].items():
        if ('sources' in mval.keys()):
          for line, sval in mval['sources'].items():
            #Find data flows
            self.find_df(class_path, method, line, sval)
            # Find implicits
            self.find_imps(class_path, method, line)
            # Find sinks
            self.find_sinks(class_path, method, line)
            # Find comparison mates
            self.find_cmp_mates(class_path, method, line)
    return self.data_flows

