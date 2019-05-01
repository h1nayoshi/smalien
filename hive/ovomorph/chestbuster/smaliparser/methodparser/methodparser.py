# -*- coding: utf-8 -*-
# Called by smaliparser.py

import sys
import time
from pprint import pprint

from . import methodfuncs as mfuncs
from .dalvikbytecodeparser import dalvikbytecodeparser as dbcparser
from .sisparser import sisparser as sisparser

class MethodParser(mfuncs.MethodFuncs, dbcparser.DBCParser, sisparser.SisParser):
  def parse_methods(self):
    # Find methods in each smali
    start = time.time()
    print('    [*] Finding methods')
    total_methods = 0
    total_statics = 0
    for class_path, cval in self.parsed_data.items():
      total_statics += len(cval['static_vars'].keys())
      self.find_methods(class_path, cval)
      total_methods += len(cval['methods'].keys())

    print('     [+] Total: '+str(total_methods))
    print('     [*] Done in '+str(round(time.time() - start, 3)))

    # Find method calls in each method
    print('    [*] Finding method calls')
    #cntr = 0
    start = time.time()
    self.generate_method_paths()
    for class_path, cval in self.parsed_data.items():    
      src_code = self.src_codes[cval['file_path']]
      for method, mval in cval['methods'].items():
        self.find_method_calls(class_path, method, mval, src_code)
        #cntr += 1
        #print cntr, '/', total_methods
    print('     [*] Done in ', time.time() - start)

    print('    [*] Detecting target methods')
    total_target = 0
    start = time.time()
    for act in self.activities:
      for class_path, cval in self.parsed_data.items():
        if (class_path == act or class_path.find(act[:-1]+'$') > -1):
          for method, mval in cval['methods'].items():
            total_target += self.detect_target_methods(mval)
    print('      [+]Target: '+str(total_target))
    print('     [*] Done in '+str(round(time.time() - start, 3)))

    print('    [*] Finding control flow blocks')
    #cntr = 0
    start = time.time()
    # Find control flow blocks in each method
    for class_path, cval in self.parsed_data.items():
      src_code = self.src_codes[cval['file_path']]
      for method, mval in cval['methods'].items():
        if (mval['target'] == True):
          self.construct_blocks(mval, src_code)
        #cntr += 1
        #print '  ', cntr, '/', total_methods
    print('     [*]Done in '+str(round(time.time() - start, 3)))

    print('    [*] Parsing Dalvik bytecode')
    #cntr = 0
    start = time.time()
    # Find vars in each methods
    for class_path, cval in self.parsed_data.items():
      src_code = self.src_codes[cval['file_path']]
      for method, mval in cval['methods'].items():
        if (mval['target'] == True):
          self.parse_dalvik(class_path, method, mval, src_code)
        #cntr += 1
        #print '  ', cntr, '/', total_methods
    print('     [*] Done in '+str(round(time.time() - start, 3)))

    print('    [*] Finding sources, implicits, and sinks')
    source_cntr = 0
    implicit_cntr = 0
    sink_cntr = 0
    start = time.time()
    # Find sources, implicits, and sinks in each method
    for class_path, cval in self.parsed_data.items():
      src_code = self.src_codes[cval['file_path']]
      for method, mval in cval['methods'].items():
        if (mval['target'] == True):
          self.find_sis(mval, src_code)
          source_cntr += len(mval['sources'].keys())
          implicit_cntr += len(mval['implicits'].keys())
          sink_cntr += len(mval['sinks'].keys())
        #cntr += 1
        #print '  ', cntr, '/', total_methods
    print('       [+] Sources: '+str(source_cntr))
    print('       [+] Implicits: '+str(implicit_cntr))
    print('       [+] Sinks: '+str(sink_cntr))
    print('      [*] Done in '+str(round(time.time() - start, 3)))

