# -*- coding: utf-8 -*-
# Called by dalvikbytecodeparser.py

import re
import pprint

from .dalvikbytecodes import invoke_kind as ik

class DBCFuncs():
  # Target method's value and src code
  mv = {}
  sc = ''

  def set_mv_and_sc(self, mval, src_code):
    DBCFuncs.mv = mval
    DBCFuncs.sc = src_code

  def get_local_num(self):
    c = DBCFuncs.sc[DBCFuncs.mv['start']+1]
    if (c.find('    .locals ') > -1):
      DBCFuncs.mv['var_num']['local'] = int(DBCFuncs.sc[DBCFuncs.mv['start']+1].split(' ')[-1])
    else:
      DBCFuncs.mv['var_num']['local'] = 0

  def get_params(self):
    # Add first param
    DBCFuncs.mv['vars']['p0'] = {
      'attr': 'param',
      'state': {},
    }
    self.add_state('p0', DBCFuncs.mv['start'], DBCFuncs.mv['start'], 'this', 'dest', 'param')
    DBCFuncs.mv['params']['p0'] = {}
    # Find other params
    cnt = 1
    ptypes = self.get_ptypes_from_method_def(DBCFuncs.sc[DBCFuncs.mv['start']])
    for ptype in ptypes:
      p = 'p'+str(cnt)
      DBCFuncs.mv['vars'][p] = {
        'attr': 'param',
        'state': {},
      }
      self.add_state(p, DBCFuncs.mv['start'], DBCFuncs.mv['start'], 'type', 'dest', 'param')
      DBCFuncs.mv['params'][p] = {}
      cnt += 1
      if (ptype in ['J', 'D']): # If a type is long or double, ignore next var
        p = 'p'+str(cnt)
        DBCFuncs.mv['vars'][p] = {
          'attr': 'param',
          'state': {},
        }
        self.add_state(p, DBCFuncs.mv['start'], DBCFuncs.mv['start'], 'type', 'dest', 'param')
        DBCFuncs.mv['params'][p] = {}
        cnt += 1
    DBCFuncs.mv['var_num']['param'] = cnt
    #print ' params', cnt

  def init_local_and_static(self):
    for i in range(DBCFuncs.mv['var_num']['local']):
      DBCFuncs.mv['vars']['v'+str(i)] = {
        'attr': 'local',
        'state': {},
      }
    for class_path, cval in self.parsed_data.items():
      for s in cval['static_vars'].keys():
        DBCFuncs.mv['vars'][s] = {
          'attr': 'static',
          'state': {},
        }

  def add_state(self, v, key, line, vtype, role, peer):
    if (v not in DBCFuncs.mv['vars'].keys()):
        if (v.find('->') > -1):
          attr = 'static'
        else:
          attr = 'local'
        DBCFuncs.mv['vars'][v] = {
          'attr': attr,
          'state': {},
        }
    if (key not in DBCFuncs.mv['vars'][v]['state'].keys()):
      DBCFuncs.mv['vars'][v]['state'][key] = []
    if (role == 'src'):
      DBCFuncs.mv['vars'][v]['state'][key].append({
        'dline': line,
        'type': vtype,
        'role': role,
        'dest': peer,
      })
    else:
      DBCFuncs.mv['vars'][v]['state'][key].append({
        'sline': line,
        'type': vtype,
        'role': role,
        'src': peer,
      })

  def update_get_of_static_var(self, vs, class_path, method, line, stype):
    self.parsed_data[vs[1].split('->')[0]]['static_vars'][vs[1]]['get'].append({
      'class_path': class_path,
      'method': method,
      'line': line,
      'type': stype,
      'dest': vs[0],
    })

  def update_put_of_static_var(self, vs, class_path, method, line, stype):
    if (class_path not in self.parsed_data[vs[1].split('->')[0]]['static_vars'][vs[1]]['put'].keys()):
      self.parsed_data[vs[1].split('->')[0]]['static_vars'][vs[1]]['put'][class_path] = {}
    if (method not in self.parsed_data[vs[1].split('->')[0]]['static_vars'][vs[1]]['put'][class_path].keys()):
      self.parsed_data[vs[1].split('->')[0]]['static_vars'][vs[1]]['put'][class_path][method] = {}
    self.parsed_data[vs[1].split('->')[0]]['static_vars'][vs[1]]['put'][class_path][method][line] = {
      'type': stype,
      'src': vs[0],
      'sourced': 'no',
    }

  def get_stype(self, oprnds, c, line):
    #if (DBCFuncs.mv['vars'][oprnds[1]]['attr'] == 'static'): # If static
    if (oprnds[1].find('->') > -1): # If static
      stype = c.split(':')[-1]
    else: # If local
      stype = self.get_stype_from_states(oprnds[1], line)
    return stype

  def get_dtype(self, dalvik, stype, oprnds):
    if ('dtype' in dalvik.keys()):
      if (dalvik['dtype'] == 'stype'):
        dtype = stype
      elif (dalvik['dtype'] == 'src_elem'):
        if (stype == 'unknown'):
          dtype = 'unknown'
        else:
          dtype = stype[1:]
      elif (dalvik['dtype'] == 'oprnd'):
        dtype = oprnds[-1]
      else:
        dtype = dalvik['dtype']
    else:
      dtype = 'unknown'
    return dtype

  def get_stype_from_states(self, var, line):
    tarea = []
    vtype = self.__get_vtype_in_tarea(var, line, tarea)
    return vtype

  def __get_vtype_in_tarea(self, var, line, tarea):
    vtype = 'unknown'
    for block, bval in DBCFuncs.mv['blocks'].items():
      if (line >= bval['start'] and line <= bval['end']):
        # Add area if hasn't done yet
        done = self.__add_tarea(tarea, [line, bval['start']])
        if (done):
          # Check the area
          vtype = self.__get_vtype_in_area(var, [line, bval['start']])
          if (vtype != 'unknown'):
            return vtype
          else:
            # Find sub blocks
            for nblock, nbval in DBCFuncs.mv['blocks'].items():
              if (nbval['to']['line'] <= line and nbval['to']['line'] >= bval['start']):
                vtype = self.__get_vtype_in_tarea(var, nbval['end'], tarea)
                if (vtype != 'unknown'):
                  return vtype
            # Find previous block
            if ('line' in bval['from'].keys() and bval['from']['line'] != -1):
              vtype = self.__get_vtype_in_tarea(var, bval['from']['line'], tarea)
              if (vtype != 'unknown'):
                return vtype
            elif ('range' in bval['from'].keys()):
              for r in bval['from']['range']:
                vtype = self.__get_vtype_in_tarea(var, r['end'], tarea)
                if (vtype != 'unknown'):
                  return vtype
    return vtype

  def __add_tarea(self, tarea, new):
    for ta in tarea:
      if (ta[0] == new[0] and ta[1] == new[1]):
        return False
    tarea.append(new)
    return True

  def __get_vtype_in_area(self, var, area):
    if (var in DBCFuncs.mv['vars'].keys()):
      for i in range(area[0], area[1], -1):
        if (i in DBCFuncs.mv['vars'][var]['state'].keys()):
          return DBCFuncs.mv['vars'][var]['state'][i][-1]['type']
    return 'unknown'

  """
  def get_stype_from_states_old(self, var, line):
    print('getting stype')
    tarea = []
    self.__get_target_area(line, tarea)
    vtype = self.__get_vtype_in_area(var, tarea)
    print('done')
    return vtype

  def __get_target_area(self, line, tarea):
    print(tarea)
    for block, bval in DBCFuncs.mv['blocks'].items():
      if (line >= bval['start'] and line <= bval['end']):
        # Add tarea if hasn't done yet
        done = self.__add_tarea(tarea, [line, bval['start']])
        if (done):
          # Find sub blocks
          for nblock, nbval in DBCFuncs.mv['blocks'].items():
            if (nbval['to']['line'] <= line and nbval['to']['line'] >= bval['start']):
              self.__get_target_area(nbval['end'], tarea)
          # Find previous block
          if ('line' in bval['from'].keys() and bval['from']['line'] != -1):
            self.__get_target_area(bval['from']['line'], tarea)
          elif ('range' in bval['from'].keys()):
            for r in bval['from']['range']:
              self.__get_target_area(r['end'], tarea)

  def __add_tarea(self, tarea, new):
    for ta in tarea:
      if (ta[0] == new[0] and ta[1] == new[1]):
        return False
    tarea.append(new)
    return True

  def __get_vtype_in_area(self, var, tarea):
    for ta in tarea:
      for i in range(ta[0], ta[1], -1):
        if (var in DBCFuncs.mv['vars'].keys()):
          if (i in DBCFuncs.mv['vars'][var]['state'].keys()):
            return DBCFuncs.mv['vars'][var]['state'][i][-1]['type']
    return 'unknown'
  """

  def get_invoke(self, i):
    c = DBCFuncs.sc[i]
    j = 0
    while (c.find('    :') > -1 or c.find('    .') > -1):
      j += 1
      c = DBCFuncs.sc[i-j]
    return c, i-j

  def get_params_from_method_call(self, c):
    params = c[c.find('{')+1:c.find('}')]
    if (len(params) < 1):
      return []
    elif (params.find(' .. ') > -1):
      attr = params.split(' ')[0][0]
      start = int(params.split(' ')[0][1:])
      end = int(params.split(' ')[-1][1:])
      ret = []
      for i in range(start, end+1):
        ret.append(attr+str(i))
      return ret
    else:
      return params.split(', ')

  def get_ptypes_from_method_def(self, c):
    ptypes = []
    pstart = c.find('(') + 1
    pend = c.find(')')
    params = c[pstart:pend]
    iterator = re.finditer(r'\[*[VZBSCIJFD](?![a-z])|\[*L[a-z]', params)
    offset = 0
    for match in iterator:
      ptype = match.group()
      if (len(ptype) > 1 and re.match(r'^\[*L', ptype)):
        ptype = params[match.start():match.start()+params[match.start():].find(';')+1]
      if (offset <= match.start()):
        ptypes.append(ptype)
        offset += len(ptype)
    return ptypes

  def get_ptypes_from_method_call(self, c):
    if (c.split(' ')[4] in ik[0]):
      ptypes = [c.split('->')[0].split(' ')[-1]]
    elif (c.split(' ')[4] in ik[1]):
      ptypes = []
    elif (c.split(' ')[4] in ik[2]):
      ptypes = ['unknown', c.split('}, ')[1].split(';')[0]+';']
    else:
      return []
    ptypes.extend(self.get_ptypes_from_method_def(c))
    return ptypes

  def is_api(self, class_path, method, line):
    calls = self.parsed_data[class_path]['methods'][method]['calls']
    for call in calls:
      if (line == call['line']):
        return False
    return True

  def is_there_ret(self, i):
    c = DBCFuncs.sc[i]
    while (c.find('    :') > -1 or c.find('    .') > -1):
      i += 1
      c = DBCFuncs.sc[i]
    c = DBCFuncs.sc[i+1]
    if (c.find(' move-result') > -1):
      return True
    return False

