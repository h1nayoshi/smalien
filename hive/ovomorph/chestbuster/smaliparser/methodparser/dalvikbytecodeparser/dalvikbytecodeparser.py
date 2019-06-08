# -*- coding: utf-8 -*-
# Called by methodparser.py

import re
from pprint import pprint

from . import dalvikbytecodefuncs as dbcfuncs
from .dalvikbytecodes import dalvik_byte_codes as dalviks, invoke_kind as ik

class DBCParser(dbcfuncs.DBCFuncs):
  def parse_dalvik(self, class_path, method, mval, src_code):
    # Get method basic info
    self.__get_basic_info(mval, src_code)

    # Parse dalvik byte code
    self.__parse(class_path, method, mval, src_code)

  def __get_basic_info(self, mval, src_code):
    mval['vars'] = {}
    mval['var_num'] = {}
    mval['params'] = {}

    # Set target method's value and src_code
    self.set_mv_and_sc(mval, src_code)
    # Get a number of local vars
    self.get_local_num()
    # Get params
    self.get_params()

  def __parse(self, class_path, method, mval, src_code):
    for i in range(mval['start'], mval['end']):
      c = src_code[i]
      for dalvik in dalviks:
        if (c.find(dalvik['code']) > -1):
          if (dalvik['group'] == 0): # Group 0: opcode x1, x2, ..., xn
            oprnds = ''.join(c.split(' ')[5:]).split(',')
            params = oprnds
            if (dalvik['class'] == 0): # Class 0: opcode dest, lit
              self.add_state(oprnds[0], i, i, dalvik['type'], 'dest', 'literal')
            elif (dalvik['class'] == 1): # Class 1: opcode dest, type
              # Find dest type
              dtype = self.get_dtype(dalvik, None, oprnds)
              # Add state
              self.add_state(oprnds[0], i, i, dtype, 'dest', 'define')
            elif (dalvik['class'] == 2): # Class 2: opcode dest, src
              # If static
              if (oprnds[1].find('->') > -1):
                self.update_get_of_static_var(oprnds, class_path, method, i)
              # If an instance
              if ((len(oprnds) == 3) and (oprnds[2].find('->') > -1)):
                oprnds[1] = oprnds[2]
                self.update_get_of_instance(oprnds, class_path, method, i)
              # Find src type
              chk = self.is_var(oprnds[1])
              # If the second oprnd is not a var
              if (not chk):
                continue
              # Get src type
              stype = self.get_stype(oprnds, c, i)
              # Get dest type
              if (stype == 'unknown'):
                dtype = self.get_dtype(dalvik, stype, oprnds)
              else:
                dtype = stype
              # Add states
              self.add_state(oprnds[1], i, i, stype, 'src', oprnds[0])
              self.add_state(oprnds[0], i, i, dtype, 'dest', oprnds[1])
            elif (dalvik['class'] == 3): # Class 3: opcode dest_src, src
              # Add states
              for j in range(0, 2):
                vtype = dalvik['type']
                self.add_state(oprnds[j], i, i, vtype, 'src', oprnds[0])
                self.add_state(oprnds[0], i, i, vtype, 'dest', oprnds[j])
            elif (dalvik['class'] == 4): # Class 4: opcode dest, src, src
              # Find src and dest types
              stype = self.get_stype_from_states(oprnds[1], i)
              dtype = self.get_dtype(dalvik, stype, oprnds)
              # Add states
              for j in range(1, 3):
                if (oprnds[j] in mval['vars'].keys()):
                  stype = self.get_stype_from_states(oprnds[j], i)
                  self.add_state(oprnds[j], i, i, stype, 'src', oprnds[0])
                  self.add_state(oprnds[0], i, i, dtype, 'dest', oprnds[j])
            elif (dalvik['class'] == 5): # Class 5: src, dest
              stype = self.get_stype_from_states(oprnds[0], i)
              # If static
              if (oprnds[1].find('->') > -1):
                stype = oprnds[1].split(':')[1]
                self.update_put_of_static_var(oprnds, class_path, method, i)
              # If an instance
              if (len(oprnds) == 3):
                oprnds[1] = oprnds[2]
                stype = oprnds[1].split(':')[1]
                self.update_put_of_instance(oprnds, class_path, method, i)
              # Add states
              self.add_state(oprnds[0], i, i, stype, 'src', oprnds[1])
              self.add_state(oprnds[1], i, i, stype, 'dest', oprnds[0])
            elif (dalvik['class'] == 6): # Class 6: opcode src, src_dest, src
              # Get src and dest types
              stype = self.get_stype_from_states(oprnds[0], i)
              if (dalvik['dtype'] == 'array_dest'):
                dtype = '['+stype
              else:
                dtype = stype
              # Add States
              # 0 -> 1
              self.add_state(oprnds[0], i, i, stype, 'src', oprnds[1])
              # 1 <- 0
              self.add_state(oprnds[1], i, i, dtype, 'dest', oprnds[0])
              # 1 <- 1
              self.add_state(oprnds[1], i, i, dtype, 'src', oprnds[1])
              self.add_state(oprnds[1], i, i, dtype, 'dest', oprnds[1])
              # 1 <- 2
              self.add_state(oprnds[1], i, i, dtype, 'dest', oprnds[2])
              # 2 -> 1
              stype = self.get_stype_from_states(oprnds[2], i)
              self.add_state(oprnds[2], i, i, stype, 'src', oprnds[1])
          elif (dalvik['group'] == 1): # Group 1: move result
            dest = c.split(' ')[-1]
            invoke, iline = self.get_invoke(i-2)
            srcs = self.get_params_from_method_call(invoke)
            # If an array
            if (invoke.find(' filled-new-array') > -1):
              # Get src and dest types
              dtype = invoke.split(' ')[-1]
              stype = dtype[1:]
              for src in srcs:
                self.add_state(src, iline, i, stype, 'src', dest)
                self.add_state(dest, i, iline, dtype, 'dest', src)
            # If an invoke-kind
            else:
              chk = self.is_api(class_path, method, iline)
              stypes = self.get_ptypes_from_method_call(invoke)
              dtype = invoke[invoke.find(')')+1:]
              # Check if container method
              chk_cm = self.check_container_method(class_path, method, iline, invoke, srcs, stypes, dest, dtype, i)
              if (chk_cm):
                continue
              elif (chk): # If a method is API
                cntr = 0
                for stype in stypes:
                  self.add_state(srcs[cntr], iline, i, stype, 'src', dest)
                  self.add_state(dest, i, iline, dtype, 'dest', srcs[cntr])
                  cntr += 1
                  if (stype == 'J' or stype == 'D'):
                    cntr += 1
              else: # If a method is not API
                if (c.split(' ')[4] in ik[3]): # If invoke-custom
                  self.add_state(dest, i, iline, 'unknown', 'dest', 'method ret')
                else:
                  if (srcs == []): # If no src
                    self.add_state(dest, i, iline, dtype, 'dest', 'method ret')
                  else:
                    cntr = 0
                    self.add_state(dest, i, iline, dtype, 'dest', 'method ret')
                    for stype in stypes:
                      self.add_state(srcs[cntr], iline, i, stype, 'src', 'method param')
                      #self.add_state(dest, i, iline, dtype, 'dest', 'method ret')
                      cntr += 1
                      if (stype == 'J' or stype == 'D'):
                        cntr += 1
          elif (dalvik['group'] == 2): # Group 2: return
            src = c.split(' ')[-1]
            stype = self.get_stype_from_states(src, i)
            self.add_state(src, i, 'unknown', stype, 'src', 'return')
          elif (dalvik['group'] == 3): # Group 3: invoke {dest, src, ..., src}, method
            chk1 = self.is_api(class_path, method, i)
            chk2 = self.is_there_ret(i+1)
            if (not chk2): # If no ret
              params = self.get_params_from_method_call(c)
              ptypes = self.get_ptypes_from_method_call(c)
              # Check if container method
              chk_cm = self.check_container_method(class_path, method, i, c, params, ptypes, None, None, None)
              if (chk_cm):
                continue
              elif (chk1): # If API
                if (len(params) > 1):
                  # Check if init with params
                  dtype = ptypes[0]
                  if (c.find("<init>") > -1):
                    ptypes[0] = 'uninitialized'
                  cntr = 0
                  for ptype in ptypes:
                    self.add_state(params[cntr], i, i, ptype, 'src', params[0])
                    self.add_state(params[0], i, i, dtype, 'dest', params[cntr])
                    if (ptype == 'J' or ptype == 'D'):
                      cntr += 1
                    cntr += 1
                else: # If init
                  self.add_state(params[0], i, i, ptypes[0], 'dest', 'init')
              else: # If not API
                cntr = 0
                for ptype in ptypes:
                  self.add_state(params[cntr], i, -1, ptype, 'src', 'method param')
                  if (ptype == 'J' or ptype == 'D'):
                    cntr += 1
                  cntr += 1
          elif (dalvik['group'] == 4): # Group 4: invoke {src_dest, src_dest, ..., src_dest}, method
            #chk1 = self.is_api(class_path, method, i)
            chk2 = self.is_there_ret(i+1)
            if (not chk2): # If not api and no ret
            #if (chk1 and not chk2): # If not api and no ret
              params = self.get_params_from_method_call(c)
              ptypes = self.get_ptypes_from_method_call(c)
              if (params != []):
              #if (len(params) > 1):
                cntr = 0
                for stype in ptypes:
                  j = 0
                  for dtype in ptypes:
                    self.add_state(params[cntr], i, i, stype, 'src', params[j])
                    self.add_state(params[j], i, i, dtype, 'dest', params[cntr])
                    if (dtype == 'J' or dtype == 'D'):
                      j += 1
                    j += 1
                  if (stype == 'J' or stype == 'D'):
                    cntr += 1
                  cntr += 1
          elif (dalvik['group'] == 5): # Group 5: do nothing
            pass

