# -*- coding: utf-8 -*-
# Called by dataflowanalyzer.py

from pprint import pprint

class DFFuncs():
  def find_cmp_mates(self, cp, m, line):
    df = self.data_flows[cp][m][line]
    # Get all implicit vars
    imps_all = self.__get_all_imps(df['implicits'])
    # Get all sink vars
    sinks_all = self.__get_all_sinks(df['sinks'])

    # Find same time pairs
    mates = self.__find_same_type_mates(imps_all, sinks_all)
    # Counting total number of mates
    #for cval in mates.values():
    #  for mval in cval.values():
    #    total += len(mval['mates'])
    #print('total:', total)
    self.data_flows[cp][m][line]['comp_mates'] = mates

  def __get_all_imps(self, imps):
    ret = {}
    self.__init_ret(ret)
    for imp in imps:
      # Add an implicit var
      self.__add_imp(imp, imp['var'], ret, False, 'var')
      # Add const vars
      for const in imp['consts']:
        self.__add_imp(const, imp['var'], ret, True, 'const')
      # Add subs
      for sub in imp['subs']:
        self.__add_imp(sub, imp['var'], ret, True, 'var')
    return ret

  def __add_imp(self, vval, ivar, ret, byref, kind):
    if (vval['var'].find('->') > -1):
      return
    if (vval['line'] not in ret[vval['class_path']].keys()):
      ret[vval['class_path']][vval['line']] = {}
    if (vval['var'] not in ret[vval['class_path']][vval['line']].keys()):
      if (byref):
        vval['ivar'] = [ivar]
        vval['kind'] = kind
        vval['selected'] = False
        ret[vval['class_path']][vval['line']][vval['var']] = vval
      else:
        ret[vval['class_path']][vval['line']][vval['var']] = {
          'var': vval['var'],
          'line': vval['line'],
          'method': vval['method'],
          'class_path': vval['class_path'],
          'type': vval['type'],
          'kind': kind,
          'ivar': [ivar],
          'selected': False,
        }
    else:
      ret[vval['class_path']][vval['line']][vval['var']]['ivar'].append(ivar)

  def __get_all_sinks(self, sinks):
    ret = {}
    self.__init_ret(ret)
    for sink in sinks:
      # Add a sink var
      self.__add_sink(sink, sink['var'], ret, False)
      # Add subs
      for sub in sink['subs']:
        self.__add_sink(sub, sink['var'], ret, True)
    return ret

  def __init_ret(self, ret):
    for class_path in self.parsed_data.keys():
      ret[class_path] = {}

  def __add_sink(self, vval, svar, ret, byref):
    if (vval['var'].find('->') > -1):
      return
    # If not static
    if (vval['line'] not in ret[vval['class_path']].keys()):
      ret[vval['class_path']][vval['line']] = {}
    if (vval['var'] not in ret[vval['class_path']][vval['line']].keys()):
      if (byref):
        vval['svar'] = [svar]
        vval['selected'] = False
        ret[vval['class_path']][vval['line']][vval['var']] = vval
      else:
        ret[vval['class_path']][vval['line']][vval['var']] = {
          'var': vval['var'],
          'line': vval['line'],
          'method': vval['method'],
          'class_path': vval['class_path'],
          'type': vval['type'],
          'svar': [svar],
          'selected': False,
        }
    else:
      ret[vval['class_path']][vval['line']][vval['var']]['svar'].append(svar)

  def __find_same_type_mates(self, iall, sall):
    ret = {}
    # For each sink
    for svals in sall.values():
      for slval in svals.values():
        for svval in slval.values():
          # For each implicit
          for ivals in iall.values():
            for ilval in ivals.values():
              for ival in ilval.values():
                # If they have same type
                if (svval['type'] == ival['type']):
                  self.__add_mate(svval, ival, ret)
    return ret

  def __add_mate(self, sval, ival, ret):
    sval['selected'] = True
    ival['selected'] = True
    if (sval['class_path'] not in ret):
      ret[sval['class_path']] = {}
    if (sval['line'] not in ret[sval['class_path']]):
      ret[sval['class_path']][sval['line']] = {}
    if (sval['var'] not in ret[sval['class_path']][sval['line']]):
      ret[sval['class_path']][sval['line']][sval['var']] = {
        'var': sval['var'],
        'line': sval['line'],
        'method': sval['method'],
        'class_path': sval['class_path'],
        'type': sval['type'],
        'svar': sval['svar'],
        'mates': [ival],
      }
    else:
      ret[sval['class_path']][sval['line']][sval['var']]['mates'].append(ival)

