# -*- coding: utf-8 -*-
# Called by codegenerator.py

import time
from pprint import pprint

class CGFMates():
  cmp_target_types = [
    'Z',
    'B',
    'S',
    'C',
    'I',
    'J',
    'F',
    'D',
    'Ljava/lang/String;',
  ]

  def __check_type(self, vtype):
    if (vtype in CGFMates.cmp_target_types):
      return True
    return False

  def generate_for_mates(self, mates):
    # Get total
    total = 0
    for cval in mates.values():
      for mval in cval.values():
        for vval in mval.values():
          total += len(vval['mates'])
    print('total: '+str(total))
    cntr = 1
    start = time.time()
    for cp, cpval in mates.items():
      for line, sval in cpval.items():
        for v, vval in sval.items():
          chk = self.__check_type(vval['type'])
          if (not chk):
            continue
          # For each implicits
          for mate in vval['mates']:
            print('mate: '+str(cntr)+'/'+str(total))
            cntr += 1
            # Get implicit's cmp method
            cmp_method = self.__define_mate(mate)
            # Define comparison at a sink
            self.__comparing_mate(cp, vval['method'], line, vval['var'], vval['type'], cmp_method)
    print('mates done in'+str(time.time() - start))

  def __define_mate(self, mate):
    cp = mate['class_path']
    m = mate['method']
    v = mate['var']
    line = mate['line']+1
    vtype = mate['type']
    if (v in self.generated[cp]['methods'][m].keys()):
      if (line in self.generated[cp]['methods'][m][v].keys()):
        if ('cmethod' in self.generated[cp]['methods'][m][v][line].keys()):
          return self.generated[cp]['methods'][m][v][line]['cmethod']
      else:
        self.generated[cp]['methods'][m][v][line] = {'code': []}
    else:
      self.generated[cp]['methods'][m][v] = {line: {'code': []}}
    code = []
    # Define a static var for data saving
    dvar = self.__define_data_var(code, v, line, vtype, self.cmp_cntr)
    # Define a static var for memorize saving action
    mvar = self.__define_mem_var(code, v, line, self.cmp_cntr)
    # Get tag var of a mate
    tpath = self.__get_tag_var(mate)
    # Define data-saving method
    self.__define_data_saving_method(code, vtype, dvar, mvar, cp, tpath)
    self.generated[cp]['methods'][m][v][line]['saving'] = cp+'->Save'+dvar.split(':')[0]+'('+vtype+')V\n'
    #self.__define_data_saving_method(code, vtype, dvar, mvar, cp, tcp, tvar)
    # Define data-comparison method
    cmethod = self.__define_cmp_method(code, vtype, dvar, mvar, cp)
    self.generated[cp]['methods'][m][v][line]['cmethod'] = cmethod
    self.generated[cp]['methods'][m][v][line]['code'].extend(code)
    self.cmp_cntr += 1
    return cmethod

  def __get_tag_var(self, mate):
    v = mate['var']
    if (mate['kind'] == 'const'):
      v = mate['ivar'][0]
    for line, tval in self.generated[mate['class_path']]['methods'][mate['method']][v].items():
      if ('tpath' in tval.keys()):
        return tval['tpath']
    return None

  def __comparing_mate(self, cp, m, line, sv, vtype, cmp_method):
    if (sv not in self.generated[cp]['methods'][m].keys()):
      self.generated[cp]['methods'][m][sv] = {}
    if (line not in self.generated[cp]['methods'][m][sv].keys()):
      self.generated[cp]['methods'][m][sv][line] = {'comparison': []}
    elif ('comparison' not in self.generated[cp]['methods'][m][sv][line].keys()):
      self.generated[cp]['methods'][m][sv][line]['comparison'] = []
    cmp_place = self.generated[cp]['methods'][m][sv][line]['comparison']
    cmp_place += 'invoke-static/range {'+sv+' .. '+sv+'}, '+cmp_method
    if (vtype in ['Z', 'B', 'S', 'C', 'I', 'F']):
      cmp_place += 'move-result '+sv+'\n'
    elif (vtype in ['J', 'D']):
      cmp_place += 'move-result-wide '+sv+'\n'
    elif (vtype == 'Ljava/lang/String;'):
      cmp_place += 'move-result-object '+sv+'\n'

  def __define_data_var(self, code, v, line, vtype, num):
    dvar = 'iData_'+v+'_'+str(line)+'_'+str(num)+':'+vtype
    code.append(
      '.field public static '+dvar+'\n'
    )
    return dvar

  def __define_mem_var(self, code, v, line, num):
    mvar = 'isSaved_'+v+'_'+str(line)+'_'+str(num)+':C'
    code.append(
      '.field public static '+mvar+'\n'
    )
    return mvar

  def __define_data_saving_method(self, code, vtype, dvar, mvar, cp, tpath):
  #def __define_data_saving_method(self, code, vtype, dvar, mvar, cp, tcp, tvar):
    if (tpath is not None):
      code.extend([
        '.method public static Save'+dvar.split(':')[0]+'('+vtype+')V\n',
        '  .locals 1\n',
        '  sget-char v0, '+tpath+'\n',
        '  if-eqz v0, :pass\n',
        '    const/4 v0, 0x7\n',
        '    sput-char v0, '+cp+'->'+mvar+'\n',
      ])
    else:
      code.extend([
        '.method public static Save'+dvar.split(':')[0]+'('+vtype+')V\n',
        '  .locals 1\n',
        '    const/4 v0, 0x7\n',
        '    sput-char v0, '+cp+'->'+mvar+'\n',
      ])
    if (vtype == 'Z'):
      code.append(
        '    sput-boolean p0, '+cp+'->'+dvar+'\n',
      )
    if (vtype == 'I'):
      code.append(
        '    sput p0, '+cp+'->'+dvar+'\n',
      )
    if (vtype == 'B'):
      code.append(
        '    sput-byte p0, '+cp+'->'+dvar+'\n',
      )
    if (vtype == 'S'):
      code.append(
        '    sput-short p0, '+cp+'->'+dvar+'\n',
      )
    if (vtype == 'C'):
      code.append(
        '    sput-char p0, '+cp+'->'+dvar+'\n',
      )
    if (vtype == 'F'):
      code.append(
        '    sput p0, '+cp+'->'+dvar+'\n',
      )
    if (vtype in ['J', 'D']):
      code.append(
        '    sput-wide p0, '+cp+'->'+dvar+'\n',
      )
    elif (vtype == 'Ljava/lang/String;'):
      code.append(
        '    sput-object p0, '+cp+'->'+dvar+'\n',
      )
    code.extend([
      '  :pass\n',
      '  return-void\n',
      '.end method\n',
    ])

  def __define_cmp_method(self, code, vtype, dvar, mvar, cp):
    cmethod = 'Cmp'+dvar.split(':')[0]+'('+vtype+')'+vtype+'\n'
    # ToDo: two arguments
    #cmethod = 'Cmp'+dvar.split(':')[0]+'('+vtype+'Ljava/lang/String;)'+vtype+'\n'
    code.extend([
      '.method public static '+cmethod,
      '  .locals 2\n',
      '  const/4 v0, 0x7\n',
      '  sget-char v1, '+cp+'->'+mvar+'\n',
      '  if-ne v0, v1, :pass\n',
    ])
    if (vtype == 'Z'):
      code.extend([
        '    sget-boolean v0, '+cp+'->'+dvar+'\n',
        '    if-ne v0, p0, :pass\n',
        '      const-string v0, "'+dvar+'"\n',
        self.log_call,
        '      const p0, 0x0\n',
        '  :pass\n',
        '  return p0\n',
      ])
    elif (vtype == 'I'):
      code.extend([
        '    sget v0, '+cp+'->'+dvar+'\n',
        '    if-ne v0, p0, :pass\n',
        '      const-string v0, "'+dvar+'"\n',
        self.log_call,
        '      const p0, 0x0\n',
        '  :pass\n',
        '  return p0\n',
      ])
    elif (vtype == 'B'):
      code.extend([
        '    sget-byte v0, '+cp+'->'+dvar+'\n',
        '    if-ne v0, p0, :pass\n',
        '      const-string v0, "'+dvar+'"\n',
        self.log_call,
        '      const/4 p0, 0x0\n',
        '  :pass\n',
        '  return p0\n',
      ])
    elif (vtype == 'S'):
      code.extend([
        '    sget-short v0, '+cp+'->'+dvar+'\n',
        '    if-ne v0, p0, :pass\n',
        '      const-string v0, "'+dvar+'"\n',
        self.log_call,
        '      const/4 p0, 0x0\n',
        '  :pass\n',
        '  return p0\n',
      ])
    elif (vtype == 'C'):
      code.extend([
        '    sget-char v0, '+cp+'->'+dvar+'\n',
        '    if-ne v0, p0, :pass\n',
        '      const-string v0, "'+dvar+'"\n',
        self.log_call,
        '      const/4 p0, 0x0\n',
        '  :pass\n',
        '  return p0\n',
      ])
    elif (vtype == 'F'):
      code.extend([
        '    sget v0, '+cp+'->'+dvar+'\n',
        '    cmpl-float v0, p0, v0\n',
        '    if-nez v0, :pass\n',
        '      const-string v0, "'+dvar+'"\n',
        self.log_call,
        '      const/high16 p0, 0x0\n',
        '  :pass\n',
        '  return p0\n',
      ])
    elif (vtype == 'J'):
      code.extend([
        '    sget-wide v0, '+cp+'->'+dvar+'\n',
        '    cmp-long v0, p0, v0\n',
        '    if-nez v0, :pass\n',
        '      const-string v0, "'+dvar+'"\n',
        self.log_call,
        '      const-wide p0, 0x0\n',
        '  :pass\n',
        '  return p0\n',
      ])
    elif (vtype == 'D'):
      code.extend([
        '    sget-wide v0, '+cp+'->'+dvar+'\n',
        '    cmpl-double v0, p0, v0\n',
        '    if-nez v0, :pass\n',
        '      const-string v0, "'+dvar+'"\n',
        self.log_call,
        '      const-wide p0, 0x0\n',
        '  :pass\n',
        '  return p0\n',
      ])
    elif (vtype == 'Ljava/lang/String;'):
      code.extend([
        '    sget-object v0, '+cp+'->'+dvar+'\n',
        '    invoke-virtual {v0, p0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z\n',
        '    move-result v0\n',
        '    if-eqz v0, :pass\n',
        '      const-string v0, "'+dvar+'"\n',
        self.log_call,
        '      const-string p0, "*"\n',
        '  :pass\n',
        '  return-object p0\n',
      ])
    code.append(
      '.end method\n\n'
    )
    return cp+'->'+cmethod

