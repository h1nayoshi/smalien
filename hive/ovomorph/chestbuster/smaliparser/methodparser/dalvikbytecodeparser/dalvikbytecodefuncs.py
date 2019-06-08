# -*- coding: utf-8 -*-
# Called by dalvikbytecodeparser.py

import re
import pprint

from .dalvikbytecodes import invoke_kind as ik
from .containermethods import container_methods as cms

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
      self.add_state(p, DBCFuncs.mv['start'], DBCFuncs.mv['start'], ptype, 'dest', 'param')
      DBCFuncs.mv['params'][p] = {}
      cnt += 1
      if (ptype in ['J', 'D']): # If a type is long or double, ignore next var
        p = 'p'+str(cnt)
        DBCFuncs.mv['vars'][p] = {
          'attr': 'param',
          'state': {},
        }
        self.add_state(p, DBCFuncs.mv['start'], DBCFuncs.mv['start'], ptype, 'dest', 'param')
        DBCFuncs.mv['params'][p] = {}
        cnt += 1
    DBCFuncs.mv['var_num']['param'] = cnt
    #print ' params', cnt

  def is_var(self, v):
    if (v.find('->') > -1 or v[0] in ['v', 'p']):
      return True
    return False

  def add_state(self, v, key, line, vtype, role, peer):
    if (v not in DBCFuncs.mv['vars'].keys()):
        if (v.find('->') > -1):
          attr = 'global'
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

  def update_get_of_static_var(self, vs, class_path, method, line):
    vs_cp = vs[1].split('->')[0]
    vs_var = vs[1].split('->')[1]
    stype = vs_var.split(':')[1]
    # Check vs_cp is known
    if (vs_cp not in self.parsed_data['classes'].keys()):
      return
    # If the static var hasn't been initialized, init it first
    if (vs[1] not in self.parsed_data['classes'][vs_cp]['static_vars'].keys()):
      self.parsed_data['classes'][vs_cp]['static_vars'][vs[1]] = {
        'name': vs_var.split(':')[0],
        'type': vs_var.split(':')[1],
        'class_path': vs_cp,
        'put': {},
        'get': {},
      }
    # Update get
    if (class_path not in self.parsed_data['classes'][vs_cp]['static_vars'][vs[1]]['get'].keys()):
      self.parsed_data['classes'][vs_cp]['static_vars'][vs[1]]['get'][class_path] = {}
    if (method not in self.parsed_data['classes'][vs_cp]['static_vars'][vs[1]]['get'][class_path].keys()):
      self.parsed_data['classes'][vs_cp]['static_vars'][vs[1]]['get'][class_path][method] = {}
    self.parsed_data['classes'][vs_cp]['static_vars'][vs[1]]['get'][class_path][method][line] = {
      'type': stype,
      'dest': vs[0],
    }

  def update_get_of_instance(self, vs, class_path, method, line):
    i_cp = vs[1].split('->')[0]
    i_var = vs[1].split('->')[1]
    stype = i_var.split(':')[1]
    # Check i_cp is known
    if (i_cp not in self.parsed_data['classes'].keys()):
      return
    # If the instance hasn't been initialized, init it first
    if (vs[1] not in self.parsed_data['classes'][i_cp]['instances'].keys()):
      self.parsed_data['classes'][i_cp]['instances'][vs[1]] = {
        'name': i_var.split(':')[0],
        'type': i_var.split(':')[1],
        'class_path': i_cp,
        'put': {},
        'get': {},
      }
    # Update get
    if (class_path not in self.parsed_data['classes'][i_cp]['instances'][vs[1]]['get'].keys()):
      self.parsed_data['classes'][i_cp]['instances'][vs[1]]['get'][class_path] = {}
    if (method not in self.parsed_data['classes'][i_cp]['instances'][vs[1]]['get'][class_path].keys()):
      self.parsed_data['classes'][i_cp]['instances'][vs[1]]['get'][class_path][method] = {}
    self.parsed_data['classes'][i_cp]['instances'][vs[1]]['get'][class_path][method][line] = {
      'type': stype,
      'dest': vs[0],
    }

  def update_put_of_static_var(self, vs, class_path, method, line):
    vs_cp = vs[1].split('->')[0]
    vs_var = vs[1].split('->')[1]
    stype = vs_var.split(':')[1]
    # Check vs_cp is known
    if (vs_cp not in self.parsed_data['classes'].keys()):
      return
    # If the static var hasn't been initialized, init it first
    if (vs[1] not in self.parsed_data['classes'][vs_cp]['static_vars'].keys()):
      self.parsed_data['classes'][vs_cp]['static_vars'][vs[1]] = {
        'name': vs_var.split(':')[0],
        'type': vs_var.split(':')[1],
        'class_path': vs_cp,
        'put': {},
        'get': {},
      }
    # Update put
    if (class_path not in self.parsed_data['classes'][vs_cp]['static_vars'][vs[1]]['put'].keys()):
      self.parsed_data['classes'][vs_cp]['static_vars'][vs[1]]['put'][class_path] = {}
    if (method not in self.parsed_data['classes'][vs_cp]['static_vars'][vs[1]]['put'][class_path].keys()):
      self.parsed_data['classes'][vs_cp]['static_vars'][vs[1]]['put'][class_path][method] = {}
    self.parsed_data['classes'][vs_cp]['static_vars'][vs[1]]['put'][class_path][method][line] = {
      'type': stype,
      'src': vs[0],
      'sourced': 'no',
    }

  def update_put_of_instance(self, vs, class_path, method, line):
    i_cp = vs[1].split('->')[0]
    i_var = vs[1].split('->')[1]
    stype = i_var.split(':')[1]
    # Check i_cp is known
    if (i_cp not in self.parsed_data['classes'].keys()):
      return
    # If the instance hasn't been initialized, init it first
    if (vs[1] not in self.parsed_data['classes'][i_cp]['instances'].keys()):
      self.parsed_data['classes'][i_cp]['instances'][vs[1]] = {
        'name': i_var.split(':')[0],
        'type': i_var.split(':')[1],
        'class_path': i_cp,
        'put': {},
        'get': {},
      }
    # Update put
    if (class_path not in self.parsed_data['classes'][i_cp]['instances'][vs[1]]['put'].keys()):
      self.parsed_data['classes'][i_cp]['instances'][vs[1]]['put'][class_path] = {}
    if (method not in self.parsed_data['classes'][i_cp]['instances'][vs[1]]['put'][class_path].keys()):
      self.parsed_data['classes'][i_cp]['instances'][vs[1]]['put'][class_path][method] = {}
    self.parsed_data['classes'][i_cp]['instances'][vs[1]]['put'][class_path][method][line] = {
      'type': stype,
      'src': vs[0],
      'sourced': 'no',
    }

  def get_stype(self, oprnds, c, line):
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

  def get_invoke(self, i):
    c = DBCFuncs.sc[i]
    while (c.find('    :') > -1 or c.find('    .') > -1 or c == ''):
      i -= 1
      c = DBCFuncs.sc[i]
    return c, i

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
    calls = self.parsed_data['classes'][class_path]['methods'][method]['calls']
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

  def check_container_method(self, cp, m, l, c, params, ptypes, dest, dtype, dline):
    for cm in cms:
      if (c.find(cm['code']) > -1):
        if ((cm['class'] == 0 and len(params) < 3) or (cm['class'] == 1 and len(params) < 2)):
          return False
        ks = self.__get_key_string(cp, m, l, params[1])
        # Set container type
        if (cm['group'] == 0): # SharedPreferences
          con_type = 'preference'
        elif (cm['group'] == 1): # Bundle, Intent
          con_type = 'bundle'
        elif (cm['group'] == 2): # JsonObject
          con_type = 'jsonobject'
        # Update and add state
        if (cm['class'] == 0): # Put
          self.__update_put_of_con(self.parsed_data['containers'][con_type]['put'], cp, m, l, params, ptypes, ks)
          self.add_state(params[1], l, l, ptypes[1], 'src', con_type+'_key')
          self.add_state(params[2], l, l, ptypes[2], 'src', con_type+'_val_put')
        elif (cm['class'] == 1): # Get
          self.__update_get_of_con(self.parsed_data['containers'][con_type]['get'], cp, m, l, params, dest, dtype, dline, ks)
          self.add_state(params[1], l, l, ptypes[1], 'src', con_type+'_key')
          if (dest is not None):
            self.add_state(dest, dline, l, dtype, 'dest', con_type+'_val_get')
        return True
    return False

  def __update_put_of_con(self, con, cp, m, l, params, ptypes, ks):
    if (cp not in con.keys()):
      con[cp] = {}
    if (m not in con[cp].keys()):
      con[cp][m] = {}
    con[cp][m][l] = {
      'key': {
        'var': params[1],
        'string': ks,
      },
      'src': params[2],
      'type': ptypes[2],
      'sourced': 'no',
    }

  def __update_get_of_con(self, con, cp, m, l, params, dest, dtype, dline, ks):
    if (cp not in con.keys()):
      con[cp] = {}
    if (m not in con[cp].keys()):
      con[cp][m] = {}
    con[cp][m][l] = { # Line of ret
      'key': {
        'var': params[1],
        'string': ks,
      },
      'dest': dest,
      'dline': dline,
      'type': dtype,
    }

  def __get_key_string(self, cp, m, l, v):
    vstates = self.parsed_data['classes'][cp]['methods'][m]['vars'][v]['state']
    mstart = self.parsed_data['classes'][cp]['methods'][m]['start']
    state = self.__get_prev_state(vstates, l, mstart)
    if (state is not None and state['src'] == 'literal'):
      return DBCFuncs.sc[state['sline']].split(', ')[-1]
    return None

  def __get_prev_state(self, vstates, s, e):
    for i in range(s, e, -1):
      if (i in vstates.keys()):
        for state in vstates[i]:
          if (state['role'] == 'dest'):
            return state
    return None

