# -*- coding: utf-8 -*-
# Called by dataflowanalyzer.py

from pprint import pprint

class DFIFinder():
  imp_added = {}
  const_added = []

  def find_imps(self, cp, m, line):
    DFIFinder.imp_added = {}
    df = self.data_flows[cp][m][line]
    self.__walk_df(df['flow'], df['implicits'], [])

  def __walk_df(self, dfval, imps, subs):
    for iline, ival in self.parsed_data['classes'][dfval['class_path']]['methods'][dfval['method']]['implicits'].items():
      # Check each area
      for area in dfval['area']:
        if (iline > area['start'] and iline < area['end'] and dfval['var'] in ival['vars']):
          # Check has implicit added already
          chk = self.__has_imp_added_already(dfval['class_path'], iline)
          if (not chk):
            # Get consts in each implicit blocks
            consts = []
            self.__find_consts(consts, dfval['class_path'], dfval['method'], iline, dfval['var'])
            # Add an implicit var
            imps.append({
              'var': dfval['var'],
              'line': iline,
              'method': dfval['method'],
              'class_path': dfval['class_path'],
              'type': dfval['type'],
              'consts': consts,
              'subs': subs,
            })
          else:
            break
    if (dfval['next'] != []):
      # Add a df to subs
      subs.append({
        'var': dfval['var'],
        'line': dfval['line'],
        'method': dfval['method'],
        'class_path': dfval['class_path'],
        'type': dfval['type'],
      })
      # Walk next dfs
      for n in dfval['next']:
        self.__walk_df(n, imps, list(subs))

  def __has_imp_added_already(self, cp, line):
    if (cp in DFIFinder.imp_added.keys()):
      if (line in DFIFinder.imp_added[cp]):
        return True
      else:
        DFIFinder.imp_added[cp].append(line)
        return False
    else:
      DFIFinder.imp_added[cp] = [line]
      return False

  def __find_consts(self, consts, cp, m, line, ivar):
    DFIFinder.const_added = []
    tbs = self.__get_target_blocks(cp, m, line)
    for tb in tbs:
      for var, vval in self.parsed_data['classes'][cp]['methods'][m]['vars'].items():
        for i in range(tb['start'], tb['end']):
          if (i in vval['state'].keys()):
            for state in vval['state'][i]:
              if (state['role'] == 'dest' and state['src'] == 'literal'):
                chk = self.__has_const_added_already(i)
                if (not chk):
                  # Get const var's type
                  ctype = self.__get_const_type(i, tb['end'], vval['state'])
                  if (ctype != 'unknown'):
                    consts.append({
                      'var': var,
                      'type': ctype,
                      'line': i,
                      'method': m,
                      'class_path': cp,
                      #'ivar': ivar,
                    })

  def __get_target_blocks(self, cp, m, line):
    ret = []
    bend = self.__get_block_end(cp, m, line)
    ret.append({
      'start': line,
      'end': bend,
    })
    for block in self.parsed_data['classes'][cp]['methods'][m]['blocks'].values():
      if ('line' in block['from'].keys() and block['from']['line'] == line):
        ret.append({
          'start': block['start'],
          'end': block['end'],
        })
    return ret

  def __get_block_end(self, cp, m, line):
    for block in self.parsed_data['classes'][cp]['methods'][m]['blocks'].values():
      if (line >= block['start'] and line <= block['end']):
        return block['end']

  def __has_const_added_already(self, line):
    if line in DFIFinder.const_added:
      return True
    DFIFinder.const_added.append(line)
    return False

  def __get_const_type(self, start, end, states):
    for i in range(start+1, end):
      if (i in states.keys()):
        for s in states[i]:
          if (s['role'] == 'dest'):
            return 'unknown'
          if (s['type'] not in ['unknown', 'const']):
            return s['type']
    return 'unknown'

