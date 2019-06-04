# -*- coding: utf-8 -*-
# Called by dataflowanalyzer.py

from pprint import pprint

class DFSFinder():
  subs = []
  sink_added = {}
  area_analyzed_rev = {}
  global_var_analyzed = []

  def find_sinks(self, cp, m, line):
    DFSFinder.sink_added = {}
    df = self.data_flows[cp][m][line]
    self.__walk_df(df['flow'], df['sinks'])
    # Get untagged sinks
    self.__find_untagged_sinks(df['sinks'])

  def __walk_df(self, dfval, sinks):
    for sline, sval in self.parsed_data[dfval['class_path']]['methods'][dfval['method']]['sinks'].items():
      #print 'sink', sline, sval
      # Check each area
      for area in dfval['area']:
        #print area
        if (sline > area['start'] and sline < area['end'] and dfval['var'] in sval['vars']):
          # Add sink to dfval
          if ('sink' not in dfval.keys()):
            dfval['sink'] = []
          dfval['sink'].append(sline)
          # Check has sink added already
          chk = self.__has_sink_added_already(dfval['class_path'], sline)
          if (not chk):
            # Find sink substances
            self.__find_sink_subs(dfval['class_path'], dfval['method'], sline, dfval['var'])
            # Add a sink var
            sinks.append({
              'var': dfval['var'],
              'line': sline,
              'method': dfval['method'],
              'class_path': dfval['class_path'],
              'type': dfval['type'],
              'subs': DFSFinder.subs,
              'tag': True,
            })
          else:
            break
    for n in dfval['next']:
      self.__walk_df(n, sinks)

  def __has_sink_added_already(self, cp, line):
    if (cp in DFSFinder.sink_added.keys()):
      if (line in DFSFinder.sink_added[cp]):
        return True
      else:
        DFSFinder.sink_added[cp].append(line)
        return False
    else:
      DFSFinder.sink_added[cp] = [line]
      return False

  def __find_sink_subs(self, cp, m, line, v):
    DFSFinder.subs = []
    area = []
    nexts = []
    self.__init_df_rev()
    # Find sink's data flow in reverse
    self.__find_df_of_var_rev(cp, m, line, v, area, nexts)
    # Get subs from sink's data flow
    self.__generate_subs_from_df(nexts)
    return DFSFinder.subs

  def __init_df_rev(self):
    DFSFinder.area_analyzed_rev = {}
    DFSFinder.global_var_analyzed = []

  def __find_df_of_var_rev(self, cp, m, end, v, area, nexts):
    # Check if a var is a part of source flows
    chk = self.__is_source(cp, m, end, v)
    if (chk):
      return 'killall'
    # If a var is global
    if (v.find('->') > -1 and v.split('->')[0] in self.parsed_data.keys()):
      if (v not in DFSFinder.global_var_analyzed):
        DFSFinder.global_var_analyzed.append(v)
        put_dests = self.__get_global_put_dests(v)
        if (put_dests is None):
          return
        for scp, scpval in put_dests.items():
          for sm, smval in scpval.items():
            for sl, slval in smval.items():
              self.__add_flow(nexts, scp, sm, sl, slval['src'], sl)
            next_rm = []
            for n in nexts:
              ret = self.__find_df_of_var_rev(n['class_path'], n['method'], n['line'], n['var'], n['area'], n['next'])
              if (ret == 'killall'):
                next_rm.append(n)
            for nr in next_rm:
              nexts.remove(nr)
            if (next_rm != [] and nexts == []):
              return 'killall'
    # If a var is local
    else:
      # Get all area that a var relates
      tarea = []
      bvals = self.parsed_data[cp]['methods'][m]['blocks']
      self.__get_target_area(bvals, end, -1, tarea)
      # Analyze target area
      ta = tarea.pop(0)
      self.__analyze_area_rev(cp, m, v, ta, tarea, area, nexts)
      # Analyze next area
      next_rm = []
      for n in nexts:
        ret = self.__find_df_of_var_rev(n['class_path'], n['method'], n['line'], n['var'], n['area'], n['next'])
        if (ret == 'killall'):
          next_rm.append(n)
      for nr in next_rm:
        nexts.remove(nr)
      if (next_rm != [] and nexts == []):
        return 'killall'

  def __get_global_put_dests(self, v):
    if (v in self.parsed_data[v.split('->')[0]]['static_vars'].keys()):
      return self.parsed_data[v.split('->')[0]]['static_vars'][v]['put']
    elif (v in self.parsed_data[v.split('->')[0]]['instances'].keys()):
      return self.parsed_data[v.split('->')[0]]['instances'][v]['put']
    return None

  def __is_source(self, cp, m, end, v):
    # Check if the var is source
    for class_path, cval in self.data_flows.items():
      if (cp == class_path):
        for method, mval in cval.items():
          if (m == method):
            for fval in mval.values():
              sv = fval['flow']['var']
              if (sv == v):
                areas = fval['flow']['area']
                for area in areas:
                  if (end >= area['start'] and end <= area['end']):
                    return True
    return False

  def __get_target_area(self, bvals, end, subseq, tarea):
    for block, bval in bvals.items():
      if (end >= bval['start'] and end <= bval['end']):
        # Add tarea if hasn't done yet
        if ('line' in bval['from'].keys()):
          prev = bval['from']['line']
        else:
          prev = bval['from']['range']
        ta = {
          'prev': prev,
          'start': bval['start'],
          'end': end,
          'subseq': subseq,
        }
        done = self.__add_tarea(tarea, ta)
        if (done):
          # Find sub blocks
          for sblock, sbval in bvals.items():
            if (sbval['to']['line'] >= bval['start'] and sbval['to']['line'] <= end):
              self.__get_target_area(bvals, sbval['end'], sbval['to']['line'], tarea)
          # Find prev blocks
          if ('line' in bval['from'].keys() and bval['from']['line'] != -1):
            self.__get_target_area(bvals, bval['from']['line'], bval['start'], tarea)
          elif ('range' in bval['from'].keys()):
            for prev in bval['from']['range']:
              if (prev['end'] != -1):
                self.__get_target_area(bvals, prev['end'], bval['start'], tarea)

  def __add_tarea(self, tarea, new):
    for ta in tarea:
      if (ta['start'] == new['start'] and ta['end'] == new['end']):
        return False
    tarea.append(new)
    return True

  def __analyze_area_rev(self, cp, m, v, ta, tarea, area, nexts):
    s, acts = self.__find_df_in_area(cp, m, v, ta, nexts)
    if (cp not in DFSFinder.area_analyzed_rev.keys()):
      DFSFinder.area_analyzed_rev[cp] = {}
    if (m not in DFSFinder.area_analyzed_rev[cp].keys()):
      DFSFinder.area_analyzed_rev[cp][m] = {}
    if (v not in DFSFinder.area_analyzed_rev[cp][m].keys()):
      DFSFinder.area_analyzed_rev[cp][m][v] = []
    DFSFinder.area_analyzed_rev[cp][m][v].append([acts, ta['end']])
    # Add target area to area
    if (ta['start'] != acts):
      ta['start'] = acts
      ta['prev'] = -1
    area.append(ta)
    # Find area to that jump from this area
    narea = []
    for i in range(len(tarea)):
      if (tarea[i]['subseq'] <= ta['end'] and tarea[i]['subseq'] >= s):
        narea.append(tarea[i])
    # Remove next area in target area
    for i in range(len(narea)):
      tarea.remove(narea[i])
    # Analyze next area
    for i in range(len(narea)):
      self.__analyze_area_rev(cp, m, v, narea[i], tarea, area, nexts)

  def __find_df_in_area(self, cp, m, v, ta, nexts):
    start, end, actstart = self.__is_area_analyzed(cp, m, v, ta)
    dested = False
    for i in range(end-1, start-1, -1):
      if (i in self.parsed_data[cp]['methods'][m]['vars'][v]['state'].keys()):
        for state in self.parsed_data[cp]['methods'][m]['vars'][v]['state'][i]:
          if (state['role'] == 'dest'):
            dested = True
            # If global
            if (state['src'].find('->') > -1):
              self.__add_flow(nexts, cp, m, state['sline'], state['src'], i)
            # If method ret
            elif (state['src'] == 'method ret'):
              cll, cllend, v = self.__get_ret_of_call(cp, m, i, v)
              self.__add_flow(nexts, cll['class_path'], cll['method'], cllend, v, i)
            # If param
            elif (state['src'] == 'param'):
              vindex = int(v[1:])
              for cllr in self.parsed_data[cp]['methods'][m]['callers']:
                self.__add_flow(nexts, cllr['class_path'], cllr['method'], cllr['line'], cllr['params'][vindex], i)
            # IF propagates to a local var
            elif (state['src'] not in ['define', 'literal', 'init']):
              self.__add_flow(nexts, cp, m, state['sline'], state['src'], i)
        if (dested):
          return i, i
    return start, actstart

  def __add_flow(self, nexts, cp, m, start, v, sline):
    if (v == 'none' or self.parsed_data[cp]['methods'][m]['target'] == False):
      return
    vtype = self.parsed_data[cp]['methods'][m]['vars'][v]['state'][start][0]['type']
    nexts.append({
      'var': v,
      'type': vtype,
      'line': start,
      'dline': sline,
      'area': [],
      'method': m,
      'class_path': cp,
      'next': [],
    })
    """
    DFSFinder.subs.append({
      'var': v,
      'type': vtype,
      'line': start,
      'method': m,
      'class_path': cp,
    })
    """

  def __is_area_analyzed(self, cp, m, v, ta):
    start = ta['start']
    end = ta['end']
    actstart = start
    if (cp not in DFSFinder.area_analyzed_rev.keys()):
      return start, end, actstart
    if (m not in DFSFinder.area_analyzed_rev[cp].keys()):
      return start, end, actstart
    if (v not in DFSFinder.area_analyzed_rev[cp][m].keys()):
      return start, end, actstart
    for area in DFSFinder.area_analyzed_rev[cp][m][v]:
      if (end > area[0] and end <= area[1]):
        return -1, -1, area[0]
      elif (start >= area[0] and start < area[1]):
        start = area[1] + 1
        actstart = area[0]
    return start, end, actstart

  def __get_ret_of_call(self, cp, m, line, v):
    for cll in self.parsed_data[cp]['methods'][m]['calls']:
      if (cll['ret']['line'] == line):
        v = self.parsed_data[cll['class_path']]['methods'][cll['method']]['ret'][0]['var']
        e = self.parsed_data[cll['class_path']]['methods'][cll['method']]['ret'][0]['line']
        return cll, e, v

  def __find_untagged_sinks(self, sinks):
    for class_path, cval in self.parsed_data.items():
      for method, mval in cval['methods'].items():
        if ('sinks' in mval.keys()):
          for sline, sval in mval['sinks'].items():
            # Check has sink added already
            chk = self.__has_sink_added_already(class_path, sline)
            if (not chk):
              for v in sval['vars']:
                # Find sink substances
                self.__find_sink_subs(class_path, method, sline, v)
                # Add a sink var
                sinks.append({
                  'var': v,
                  'line': sline,
                  'method': method,
                  'class_path': class_path,
                  'type': sval['type'],
                  'subs': DFSFinder.subs,
                  'tag': False,
                })

  def __generate_subs_from_df(self, nexts):
    for n in nexts:
      DFSFinder.subs.append({
        'var': n['var'],
        'type': n['type'],
        'line': n['line'],
        'method': n['method'],
        'class_path': n['class_path'],
      })
      self.__generate_subs_from_df(n['next'])

