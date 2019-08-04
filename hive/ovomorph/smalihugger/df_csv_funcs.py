# -*- coding: utf-8 -*-

from pprint import pprint

class DfToCsv():
  def __init__(self, df, sinks):
    self.df = df
    if ('flow' in df.keys()):
      self.flow = df['flow']
    else:
      self.flow = df
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
    self.sinks = {
      'sinks': sinks,
      'node': [],
    }

  def run(self):
    self.__walk_flow(self.flow)
    self.__output_csv()
    return self.csv

  def __walk_flow(self, flow):
    src_id = self.__add_node(flow['class_path'], flow['method'], flow['var'], flow['line'])
    self.__check_sink(flow, src_id)
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
    # Output sinks
    for s in self.sinks['node']:
      self.csv += str(offset_v+s)+'\n'

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

  def __check_sink(self, flow, src_id):
    for s in self.sinks['sinks']:
      if (s['class_path'] == flow['class_path'] and s['method'] == flow['method']):
        if (s['var'] == flow['var']):
          ret = self.__check_contain(s['line'], flow['area'])
          if (ret):
            self.sinks['node'].append(src_id)

  def __check_contain(self, l, area):
    for a in area:
      if (a['start'] <= l and a['end'] >= l):
        return True
    return False

