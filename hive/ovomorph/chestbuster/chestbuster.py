# -*- coding: utf-8 -*-
# Called by smalihugger.py

import time
from pprint import pprint

from .smaliparser import smaliparser as sparser
from .dataflowanalyzer import dataflowanalyzer as dfanalyzer
from .codegenerator import codegenerator as cgenerator
from .codeinjector import codeinjector as cinjector

def run(smalis, activities):
  start = time.time()
  # Parse
  print('   [*] Parsing the smalis')
  SP = sparser.SmaliParser(smalis, activities)
  src_codes, parsed_data = SP.parse()
  print('    [*] Parsing done in '+str(round(time.time() - start, 3)))
  #pprint(parsed_data)

  print('   [*] Analyzing data flows')
  # Analyze
  start = time.time()
  DFA = dfanalyzer.DataFlowAnalyzer(parsed_data)
  data_flows = DFA.analyze()
  print('    [*] DF analysis done in '+str(round(time.time() - start, 3)))
  #pprint(data_flows)

  # Generate codes
  print('   [*] Generating bytecode')
  CG = cgenerator.CodeGenerator(parsed_data, data_flows)
  generated_codes, generated_replaces = CG.generate()
  #pprint(generated_codes)

  # Inject
  # Under construction
  print('   [*] Instrumenting bytecode')
  CI = cinjector.CodeInjector(parsed_data, generated_codes, generated_replaces, src_codes)
  CI.inject()

  return True, parsed_data, data_flows

if __name__ == '__main__':
  smalis = [
    '../workspace/FragmentManagerImpl.smali',
  ]
  activities = [
    'Landroid/support/v4/app/FragmentManagerImpl;',
  ]
  run(smalis, activities)

