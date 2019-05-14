# -*- coding: utf-8 -*-
# Called by dataflowanalyzer.py

from pprint import pprint

class DFFinder():
  area_analyzed = {}

  def find_df(self, cp, m, line, sval):
    # Source
    flow = {
      'var': sval['dest'],
      'type': sval['type'],
      'line': sval['dest_line'],
      'sline': line,
      'area': [],
      'method': m,
      'class_path': cp,
      'next': [],
    }
    self.__init_df(cp, m, line, sval, flow)

    self.__find_df_of_var(cp, m, sval['dest_line'], sval['dest'], flow['area'], flow['next'])

  def __init_df(self, cp, m, line, sval, flow):
    self.data_flows[cp][m][line] = {
      'source': sval,
      'flow': flow,
      'implicits': [],
      'sinks': [],
    }

    DFFinder.area_analyzed = {}

  def __find_df_of_var(self, cp, m, start, v, area, nexts):
    # If a var is static
    if (v.find('->') > -1 and v.split('->')[0] in self.parsed_data.keys()):
      if (self.parsed_data[v.split('->')[0]]['static_vars'][v]['put'][cp][m][start]['sourced'] == 'no'):
        self.parsed_data[v.split('->')[0]]['static_vars'][v]['put'][cp][m][start]['sourced'] = 'yes'
        for sn in self.parsed_data[v.split('->')[0]]['static_vars'][v]['get']:
          self.__add_flow(nexts, sn['class_path'], sn['method'], sn['line'], sn['dest'], sn['line'])
        for n in nexts:
          self.__find_df_of_var(n['class_path'], n['method'], n['line'], n['var'], n['area'], n['next'])
    # If a var is not static
    else:
      # Get all area that a var relates
      tarea = []
      bvals = self.parsed_data[cp]['methods'][m]['blocks']
      self.__get_target_area(bvals, start, -1, tarea)
      # Analyze target area
      ta = tarea.pop(0)
      self.__analyze_area(cp, m, v, ta, tarea, area, nexts)
      # Analyze next area
      for n in nexts:
        self.__find_df_of_var(n['class_path'], n['method'], n['line'], n['var'], n['area'], n['next'])

  def __get_target_area(self, bvals, start, prev, tarea):
    for block, bval in bvals.items():
      if (start >= bval['start'] and start <= bval['end']):
        # Add tarea if hasn't done yet
        ta = {
          'prev': prev,
          'start': start,
          'end': bval['end'],
          'subseq': bval['to']['line'],
        }
        done = self.__add_tarea(tarea, ta)
        if (done):
          # Find sub blocks
          for sblock, sbval in bvals.items():
            if ('line' in sbval['from'].keys()):
              if (sbval['from']['line'] >= start and sbval['from']['line'] <= bval['end']):
                self.__get_target_area(bvals, sbval['start'], sbval['from']['line'], tarea)
            elif ('range' in sbval['from'].keys()):
              for r in sbval['from']['range']:
                if (r['start'] <= bval['end'] and start <= r['end']):
                  self.__get_target_area(bvals, sbval['start'], r, tarea)
          # Find next block
          if (bval['to']['line'] != -1):
            self.__get_target_area(bvals, bval['to']['line'], bval['end'], tarea)

  def __add_tarea(self, tarea, new):
    for ta in tarea:
      if (ta['start'] == new['start'] and ta['end'] == new['end']):
        return False
    tarea.append(new)
    return True

  def __analyze_area(self, cp, m, v, ta, tarea, area, nexts):
    e, acte = self.__find_df_in_area(cp, m, v, ta, nexts)
    if (cp not in DFFinder.area_analyzed.keys()):
      DFFinder.area_analyzed[cp] = {}
    if (m not in DFFinder.area_analyzed[cp].keys()):
      DFFinder.area_analyzed[cp][m] = {}
    if (v not in DFFinder.area_analyzed[cp][m].keys()):
      DFFinder.area_analyzed[cp][m][v] = []
    DFFinder.area_analyzed[cp][m][v].append([ta['start'], acte])
    # Add target area to area
    if (ta['end'] != acte):
      ta['end'] = acte
      ta['subseq'] = -1
    area.append(ta)
    # Find area that this area goes to
    narea = []
    for i in range(len(tarea)):
      """ Changed tarea prev type from list to dict
      if (type(tarea[i]['prev']) == list):
        for prev in tarea[i]['prev']:
          if (prev['start'] <= e and prev['end'] >= ta['start']):
            narea.append(tarea[i])
            break
      """
      if (type(tarea[i]['prev']) == dict):
        if (tarea[i]['prev']['start'] <= e and tarea[i]['prev']['end'] >= ta['start']):
          narea.append(tarea[i])
      else:
        if (tarea[i]['prev'] >= ta['start'] and tarea[i]['prev'] <= e):
          narea.append(tarea[i])
    # Remove next area in target area
    for i in range(len(narea)):
      tarea.remove(narea[i])
    # Analyze next area
    for i in range(len(narea)):
      self.__analyze_area(cp, m, v, narea[i], tarea, area, nexts)

  def __find_df_in_area(self, cp, m, v, ta, nexts):
    start, end, actend = self.__is_area_analyzed(cp, m, v, ta)
    dested = False
    for i in range(start+1, end+1):
      if (i in self.parsed_data[cp]['methods'][m]['vars'][v]['state'].keys()):
        for state in self.parsed_data[cp]['methods'][m]['vars'][v]['state'][i]:
          if (state['role'] == 'src'):
            # If static
            if (state['dest'].find('->') > -1):
              self.__add_flow(nexts, cp, m, state['dline'], state['dest'], i)
            # If method param
            elif (state['dest'] == 'method param'):
              dest, dline, p = self.__get_dest_of_call(cp, m, i, v)
              self.__add_flow(nexts, dest['class_path'], dest['method'], dline, p, i)
            # If return
            elif (state['dest'] == 'return'):
              for cllr in self.parsed_data[cp]['methods'][m]['callers']:
                if (cllr['ret']['line'] is not None):
                  self.__add_flow(nexts, cllr['class_path'], cllr['method'], cllr['ret']['line'], cllr['ret']['var'], i)
            # IF propagates to a local var
            else:
              self.__add_flow(nexts, cp, m, state['dline'], state['dest'], i)
          elif (state['role'] == 'dest'):
            actend = i
            dested = True
        if (dested):
          return i, actend
    return end, actend

  def __add_flow(self, nexts, cp, m, start, v, sline):
    if (self.parsed_data[cp]['methods'][m]['target'] == False):
      return
    vtype = self.parsed_data[cp]['methods'][m]['vars'][v]['state'][start][-1]['type']
    nexts.append({
      'var': v,
      'type': vtype,
      'line': start,
      'sline': sline,
      'area': [],
      'method': m,
      'class_path': cp,
      'next': [],
    })

  def __is_area_analyzed(self, cp, m, v, ta):
    start = ta['start']
    end = ta['end']
    actend = end
    if (cp not in DFFinder.area_analyzed.keys()):
      return start, end, actend
    if (m not in DFFinder.area_analyzed[cp].keys()):
      return start, end, actend
    if (v not in DFFinder.area_analyzed[cp][m].keys()):
      return start, end, actend
    for area in DFFinder.area_analyzed[cp][m][v]:
      if (start >= area[0] and start < area[1]):
        return -1, -1, area[1]
      elif (end > area[0] and end <= area[1]):
        end = area[0] - 1
        actend = area[1]
    # Update area_analyzed
    return start, end, actend

  def __get_dest_of_call(self, cp, m, line, v):
    for cll in self.parsed_data[cp]['methods'][m]['calls']:
      if (cll['line'] == line):
        pnum = cll['params'].index(v)
        s = self.parsed_data[cll['class_path']]['methods'][cll['method']]['start']
        return cll, s, 'p'+str(pnum)

