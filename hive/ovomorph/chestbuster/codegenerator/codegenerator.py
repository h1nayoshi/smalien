# -*- coding: utf-8 -*-
# Called by chestbuster.py

from pprint import pprint
import copy

from . import codegencore as cgcore
from . import codegenformates as cgfm

class CodeGenerator(cgcore.CGCore, cgfm.CGFMates):
  def __init__(self, parsed_data, data_flows, ppe):
    self.parsed_data = parsed_data
    self.data_flows = data_flows
    self.codes_def = []
    self.def_class = 'Lsmalienlog;'
    self.codes_ins = {}
    self.replaces = {}
    self.generated = {}
    self.tag_cntr = 0
    self.cmp_cntr = 0
    self.sl_cntr = 0
    self.log_def = False
    self.log_call = ''
    self.log_ids = {}
    self.ppe = ppe

    self.init_generator()

  def generate(self):
    for class_path, cval in self.data_flows.items():
      for method, mval in cval.items():
        for flow in mval.values():
          # Generate Logging method if haven't done yet
          if (not self.log_def):
            self.generate_logging_method(flow['flow'])
            self.log_def = True
          # Generate for sinks
          for sink in flow['sinks']:
            self.generate_for_a_sink(sink)
          # Generate for a flow
          self.generate_for_a_flow(flow['flow'], None)
          # Generate for sinks
          #for sink in flow['sinks']:
          #  self.generate_for_a_sink(sink)
          if (self.ppe):
            # Generate for mates
            self.generate_for_mates(flow['comp_mates'])
    #pprint(self.generated)
    self.generate_final_code()
    return self.def_class, self.codes_def, self.codes_ins, self.replaces, self.log_ids

