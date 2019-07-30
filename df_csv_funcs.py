# -*- coding: utf-8 -*-

from pprint import pprint

class DfToCsv():
  def __init__(self, df, log_ids, log):
    self.df = df
    if ('flow' in df.keys()):
      self.flow = df['flow']
    else:
      self.flow = df
    self.log_ids = log_ids
    self.log = log
    self.csv = ''
    self.node = {
      'class_path': {
        'node': [],
        'num': 0,
        'children': {},
      },
      'method': {
        'node': [],
        'num': 0,
        'children': {},
      },
      'var': {
        'node': {},
        'num': 0,
      },
    }
    self.edge = []
    self.sensitive_data = {}

  def run(self):
    self.__walk_flow(self.flow)
    self.__output_csv()
    return self.csv

  def __walk_flow(self, flow):
    src_id = self.__add_node(flow['class_path'], flow['method'], flow['var'], flow['line'])
    self.__add_sensitive_data(src_id, flow['class_path'], flow['method'], flow['var'], flow['line'], flow['area'])
    for n in flow['next']:
      dest_id = self.__add_node(n['class_path'], n['method'], n['var'], n['line'])
      self.edge.append([src_id, dest_id])
      self.__walk_flow(n)

  def __output_csv(self):
    offset_m = self.node['class_path']['num']
    offset_v = offset_m+self.node['method']['num']
    # Output ndoes
    cntr = 0
    for cp in self.node['class_path']['node']:
      self.csv += str(cntr)+','+cp+'\n'
      cntr += 1
    for m in self.node['method']['node']:
      self.csv += str(cntr)+','+m+'\n'
      cntr += 1
    for cp, cpval in self.node['var']['node'].items():
      for m, mval in cpval.items():
        for v, vval in mval.items():
          self.csv += str(cntr+vval)+','+v+'\n'
    self.csv += '\n'
    # Output group relations
    for cp, children in self.node['class_path']['children'].items():
      for ch in children:
        self.csv += str(offset_m+self.node['method']['node'].index(ch))+','+str(self.node['class_path']['node'].index(cp))+'\n'
    for m, children in self.node['method']['children'].items():
      for ch in children:
        self.csv += str(offset_v+ch)+','+str(offset_m+self.node['method']['node'].index(m))+'\n'
    self.csv += '\n'
    # Output edges
    for e in self.edge:
      self.csv += str(offset_v+e[0])+','+str(offset_v+e[1])+'\n'
    self.csv += '\n'
    # Output sensitive data
    for vid, sdval in self.sensitive_data.items():
      for sd in sdval:
        self.csv += str(offset_v+vid)+','+sd+'\n'

  def __add_node(self, cp, m, v, l):
    self.__add_class_path(cp, m)
    vid = self.__add_var(cp, m, v, l)
    self.__add_method(m, vid)
    return vid

  def __add_class_path(self, cp, m):
    if (cp not in self.node['class_path']['node']):
      self.node['class_path']['node'].append(cp)
      self.node['class_path']['num'] += 1
    if (cp not in self.node['class_path']['children'].keys()):
      self.node['class_path']['children'][cp] = []
    if (m not in self.node['class_path']['children'][cp]):
      self.node['class_path']['children'][cp].append(m)

  def __add_method(self, m, v):
    if (m not in self.node['method']['node']):
      self.node['method']['node'].append(m)
      self.node['method']['num'] += 1
    if (m not in self.node['method']['children'].keys()):
      self.node['method']['children'][m] = []
    if (v not in self.node['method']['children'][m]):
      self.node['method']['children'][m].append(v)

  def __add_var(self, cp, m, v, l):
    vnode = v+'_'+str(l)
    if (cp not in self.node['var']['node'].keys()):
      self.node['var']['node'][cp] = {}
    if (m not in self.node['var']['node'][cp].keys()):
      self.node['var']['node'][cp][m] = {}
    if (vnode not in self.node['var']['node'][cp][m].keys()):
      self.node['var']['node'][cp][m][vnode] = self.node['var']['num']
      self.node['var']['num'] += 1
    return self.node['var']['node'][cp][m][vnode] 

  def __add_sensitive_data(self, src_id, cp, m, v, l, area):
    if (cp not in self.log_ids.keys()):
      return
    if (m not in self.log_ids[cp].keys()):
      return
    if (v not in self.log_ids[cp][m].keys()):
      return
    for data_l, data_tag in self.log_ids[cp][m][v].items():
      is_contained = self.__check_contain(int(data_l), area)
      if (is_contained and data_tag in self.log['source']):
        data = list(set(self.log['source'][data_tag]))
        if src_id not in self.sensitive_data.keys():
          self.sensitive_data[src_id] = []
        self.sensitive_data[src_id].extend(data)
      elif (is_contained and data_tag in self.log['sink']):
        data = list(set(self.log['sink'][data_tag]))
        if src_id not in self.sensitive_data.keys():
          self.sensitive_data[src_id] = []
        self.sensitive_data[src_id].extend(data)

  def __check_contain(self, l, area):
    for a in area:
      if (a['start'] <= l and a['end'] >= l):
        return True
    return False

