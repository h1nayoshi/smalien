# -*- coding: utf-8 -*-
# Called by codegencore.py

from pprint import pprint

class CGFuncs():
  target_types = [
    'Z',
    'B',
    'S',
    'C',
    'I',
    'J',
    'F',
    'D',
    'Ljava/lang/String;',
    #'Ljava/lang/StringBuilder;',
  ]

  def check_type(self, vtype):
    if (vtype in CGFuncs.target_types):
      return True
    return False

  def generate_tag_for_global(self, flow, prev_tag):
    v = flow['var']
    vtype = flow['type']
    line = flow['line']
    cp = v.split('->')[0]
    if (v in self.generated[cp]['global'].keys()):
      if (line in self.generated[cp]['global'][v].keys()):
        return cp+'->'+self.generated[cp]['global'][v][line]['tag']
    else:
      self.generated[cp]['global'][v] = {}
    tag = 'Tag_'+v.split('->')[-1].split(':')[0]+'_'+str(line)+'_'+str(self.tag_cntr)+':C'
    code = []
    # Define a tag
    self.__define_tag(code, tag)
    # Define a tagging method
    self.__define_tagging_method(code, cp, tag, prev_tag)
    # Define a untagging method
    self.__define_untagging_method(code, cp, tag)
    utg_place = []
    self.__untagging_global(cp, v, utg_place)
    self.generated[cp]['global'][v][line] = {
      'tag': tag,
      'tpath': cp+'->'+tag,
      'code': code,
      'type': vtype,
      'tagging': {
        'name': cp+'->tagging'+tag.split(':')[0]+'()V\n',
        'place': [line+1],
      },
      'untagging': {
        'name': cp+'->untagging'+tag.split(':')[0]+'()V\n',
        'place': utg_place,
      },
    }
    self.tag_cntr += 1
    return cp+'->'+tag

  def generate_tag_for_local(self, f, prev_tag):
    cp = f['class_path']
    m = f['method']
    v = f['var']
    line = f['line']
    vtype = f['type']
    areas = f['area']
    if (v in self.generated[cp]['methods'][m].keys()):
      if (line in self.generated[cp]['methods'][m][v].keys()):
        return cp+'->'+self.generated[cp]['methods'][m][v][line]['tag']
    else:
      self.generated[cp]['methods'][m][v] = {}
    tag = 'Tag_'+v.split('->')[-1].split(':')[0]+'_'+str(line)+'_'+str(self.tag_cntr)+':C'
    code = []
    # Define a tag
    self.__define_tag(code, tag)
    # Define a tagging method
    self.__define_tagging_method_with_log(code, cp, vtype, tag, prev_tag)
    self.__save_log_id(cp, m, v, line, tag)
    # Define a untagging method
    self.__define_untagging_method(code, cp, tag)
    # Untag at a method start if not a param
    utg_place = []
    if (v[0] != 'p'):
      mstart = self.parsed_data['classes'][cp]['methods'][m]['start']
      utg_place.append(mstart+1)
    self.__untagging_local(cp, m, areas, v, utg_place)
    #Define a checking method
    self.__define_checking_method(code, cp, vtype, tag)
    if ('sink' in f.keys()):
      chk_place = f['sink']
    else:
      chk_place = []
    self.generated[cp]['methods'][m][v][line] = {
      'tag': tag,
      'tpath': cp+'->'+tag,
      'code': code,
      'type': vtype,
      'tagging_log': {
        'name': cp+'->tagging'+tag.split(':')[0]+'('+vtype+')V\n',
        'place': [line+1],
      },
      'untagging': {
        'name': cp+'->untagging'+tag.split(':')[0]+'()V\n',
        'place': utg_place,
      },
      'checking': {
        'name': cp+'->checking'+tag.split(':')[0]+'('+vtype+')'+vtype+'\n',
        'place': chk_place,
      },
    }
    self.tag_cntr += 1
    return cp+'->'+tag

  def generate_tag_for_local_bad_type(self, f, prev_tag):
    cp = f['class_path']
    m = f['method']
    v = f['var']
    line = f['line']
    vtype = f['type']
    areas = f['area']
    if (v in self.generated[cp]['methods'][m].keys()):
      if (line in self.generated[cp]['methods'][m][v].keys()):
        return cp+'->'+self.generated[cp]['methods'][m][v][line]['tag']
    else:
      self.generated[cp]['methods'][m][v] = {}
    tag = 'Tag_'+v.split('->')[-1].split(':')[0]+'_'+str(line)+'_'+str(self.tag_cntr)+':C'
    code = []
    # Define a tag
    self.__define_tag(code, tag)
    # Define a tagging method
    self.__define_tagging_method(code, cp, tag, prev_tag)
    # Define a untagging method
    self.__define_untagging_method(code, cp, tag)
    # Untag at a method start if not a param
    utg_place = []
    if (v[0] != 'p'):
      mstart = self.parsed_data['classes'][cp]['methods'][m]['start']
      utg_place.append(mstart+1)
    self.__untagging_local(cp, m, areas, v, utg_place)
    self.generated[cp]['methods'][m][v][line] = {
      'tag': tag,
      'code': code,
      'type': vtype,
      'tagging': {
        'name': cp+'->tagging'+tag.split(':')[0]+'()V\n',
        'place': [line+1],
      },
      'untagging': {
        'name': cp+'->untagging'+tag.split(':')[0]+'()V\n',
        'place': utg_place,
      },
    }
    self.tag_cntr += 1
    return cp+'->'+tag

  def __define_tag(self, code, tag):
    code.append(
      '.field public static '+tag+'\n'
    )

  def __define_tagging_method_with_log(self, code, cp, vtype, tag, prev_tag):
    code.extend([
      '.method public static tagging'+tag.split(':')[0]+'('+vtype+')V\n',
      '  .locals 2\n',
      '  const-string v1, "source: {'+tag+'"\n',
    ])
    if (prev_tag is None):
      code.append(
        '  const/4 v0, 0x1\n'
      )
    else:
      code.append(
        '  sget-char v0, '+prev_tag+'\n'
      )
    code.extend([
      '  sput-char v0, '+cp+'->'+tag+'\n',
      '  if-eqz v0, :pass\n',
    ])
    if (vtype == 'Z'):
      code.extend([
        '    invoke-static {p0}, Ljava/lang/String;->valueOf(Z)Ljava/lang/String;\n',
        '    move-result-object v0\n',
        self.log_call,
      ])
    elif (vtype == 'I'):
      code.extend([
        '    invoke-static {p0}, Ljava/lang/String;->valueOf(I)Ljava/lang/String;\n',
        '    move-result-object v0\n',
        self.log_call,
      ])
    elif (vtype == 'B'):
      code.extend([
        '    invoke-static {p0}, Ljava/lang/String;->valueOf(B)Ljava/lang/String;\n',
        '    move-result-object v0\n',
        self.log_call,
      ])
    elif (vtype == 'S'):
      code.extend([
        '    invoke-static {p0}, Ljava/lang/String;->valueOf(S)Ljava/lang/String;\n',
        '    move-result-object v0\n',
        self.log_call,
      ])
    elif (vtype == 'C'):
      code.extend([
        '    invoke-static {p0}, Ljava/lang/String;->valueOf(C)Ljava/lang/String;\n',
        '    move-result-object v0\n',
        self.log_call,
      ])
    elif (vtype == 'F'):
      code.extend([
        '    invoke-static {p0}, Ljava/lang/String;->valueOf(F)Ljava/lang/String;\n',
        '    move-result-object v0\n',
        self.log_call,
      ])
    elif (vtype == 'J'):
      code.extend([
        '    invoke-static {p0}, Ljava/lang/String;->valueOf(J)Ljava/lang/String;\n',
        '    move-result-object v0\n',
        self.log_call,
      ])
    elif (vtype == 'D'):
      code.extend([
        '    invoke-static {p0}, Ljava/lang/String;->valueOf(D)Ljava/lang/String;\n',
        '    move-result-object v0\n',
        self.log_call,
      ])
    elif (vtype == 'Ljava/lang/String;'):
      code.extend([
        '  move-object v0, p0\n',
        self.log_call,
      ])
    code.extend([
      '  :pass\n',
      '  return-void\n',
      '.end method\n',
    ])

  def __define_tagging_method(self, code, cp, tag, prev_tag):
    code.extend([
      '.method public static tagging'+tag.split(':')[0]+'()V\n',
      '  .locals 1\n',
    ])
    if (prev_tag is None):
      code.append(
        '  const/4 v0, 0x1\n'
      )
    else:
      code.append(
        '  sget-char v0, '+prev_tag+'\n'
      )
    code.extend([
      '  sput-char v0, '+cp+'->'+tag+'\n',
      '  return-void\n',
      '.end method\n',
    ])

  def __define_untagging_method(self, code, cp, tag):
    code.extend([
      '.method public static untagging'+tag.split(':')[0]+'()V\n',
      '  .locals 1\n',
      '  const/4 v0, 0x0\n',
      '  sput-char v0, '+cp+'->'+tag+'\n',
      '  return-void\n',
      '.end method\n',
    ])

  def __define_checking_method(self, code, cp, vtype, tag):
    code.extend([
      '.method public static checking'+tag.split(':')[0]+'('+vtype+')'+vtype+'\n',
      '  .locals 1\n',
      '  sget-char v0, '+cp+'->'+tag+'\n',
      '  if-eqz v0, :pass\n',
    ])
    if (vtype in ['Z', 'I']):
      code.extend([
        '  const p0, 0x0\n',
        '  :pass\n',
        '  return p0\n',
      ])
    elif (vtype in ['B', 'S', 'C']):
      code.extend([
        '  const/4 p0, 0x0\n',
        '  :pass\n',
        '  return p0\n',
      ])
    elif (vtype == 'F'):
      code.extend([
        '  const/high16 p0, 0x0\n',
        '  :pass\n',
        '  return p0\n',
      ])
    elif (vtype in ['J', 'D']):
      code.extend([
        '  const-wide p0, 0x0\n',
        '  :pass\n',
        '  return-wide p0\n',
      ])
    elif (vtype == 'Ljava/lang/String;'):
      code.extend([
        '  const-string p0, "*"\n',
        '  :pass\n',
        '  return-object p0\n',
      ])
    elif (vtype[0] == '['):
      code.extend([
        '  const/4 v0, 0x1\n',
        '  new-array p0, v0, '+vtype+'\n',
        '  :pass\n',
        '  return-object p0\n',
      ])
    elif (vtype == 'Ljava/lang/StringBuilder;'):
      code.extend([
        '  new-instance v0, Ljava/lang/StringBuilder;\n',
        '  invoke-direct {v0}, Ljava/lang/StringBuilder;-><init>()V\n',
        '  return-object v0\n',
        '  :pass\n',
        '  return-object p0\n',
      ])
    code.append(
      '.end method\n\n'
    )

  def __untagging_global(self, cp, v, untag):
    put_dests = self.__get_global_put_dests(v)
    if (put_dests is None):
      return
    for ucp, ucpval in put_dests.items():
      for um, umval in ucpval.items():
        for uline, uval in umval.items():
          if (uval['sourced'] == 'no'):
            if ([ucp, uline+1] not in untag):
              untag.append([ucp, uline+1])

  def __get_global_put_dests(self, v):
    if (v in self.parsed_data['classes'][v.split('->')[0]]['static_vars'].keys()):
      return self.parsed_data['classes'][v.split('->')[0]]['static_vars'][v]['put']
    elif (v in self.parsed_data['classes'][v.split('->')[0]]['instances'].keys()):
      return self.parsed_data['classes'][v.split('->')[0]]['instances'][v]['put']
    return None

  def __untagging_local(self, cp, m, areas, v, untag):
    mend = self.parsed_data['classes'][cp]['methods'][m]['end']
    for area in areas:
      if (area['subseq'] == -1):
        chk_ret = self.__check_ret(cp, m, area['end'], v)
        if (chk_ret is None):
          end = area['end']+1
          if (end > mend):
            end = mend
          if (end not in untag):
            untag.append(end)
        elif (chk_ret == 'ret line'):
          if (area['end'] not in untag):
            untag.append(area['end'])

  def __check_ret(self, cp, m, end, v):
    ret = None
    for r in self.parsed_data['classes'][cp]['methods'][m]['ret']:
      if (r['line'] == end and r['var'] == v):
        return 'returned'
      elif (r['line'] == end):
        ret = 'ret line'
    return ret

  # This func is same as one for mates. Need to refactor.
  def __save_log_id(self, cp, m, v, line, log_id):
    if (cp not in self.log_ids.keys()):
      self.log_ids[cp] = {}
    if (m not in self.log_ids[cp].keys()):
      self.log_ids[cp][m] = {}
    if (v not in self.log_ids[cp][m].keys()):
      self.log_ids[cp][m][v] = {}
    self.log_ids[cp][m][v][line] = log_id

  # This func is same as one for mates. Need to refactor.
  def logging_sink(self, sink):
    cp = sink['class_path']
    m = sink['method']
    line = sink['line']
    sv = sink['var']
    vtype = sink['type']
    log_method = self.__define_sink_log_method(cp, m, line, sv, vtype)
    log_sink = 'invoke-static/range {'+sv+' .. '+sv+'}, '+log_method
    if (line not in self.generated[cp]['methods'][m][sv].keys()):
      self.generated[cp]['methods'][m][sv][line] = {'logging': log_sink}
    elif ('logging' not in self.generated[cp]['methods'][m][sv][line].keys()):
      self.generated[cp]['methods'][m][sv][line]['logging'] = log_sink

  # This func is same as one for mates. Need to refactor
  def __define_sink_log_method(self, cp, m, line, sv, vtype):
    if (sv not in self.generated[cp]['methods'][m].keys()):
      self.generated[cp]['methods'][m][sv] = {}
    if (line not in self.generated[cp]['methods'][m][sv].keys()):
      self.generated[cp]['methods'][m][sv][line] = {'code': []}
    if ('slmethod' in self.generated[cp]['methods'][m][sv][line].keys()):
      return self.generated[cp]['methods'][m][sv][line]['slmethod_call']
    sid = sv+'_'+str(line)+'_'+str(self.sl_cntr)
    # Save sid to log_ids for dynamic analysis
    self.__save_log_id(cp, m, sv, line, sid)
    slmethod = 'SinkLog_'+sid+'('+vtype+')V'
    # Define a log method
    code = []
    code.extend([
      '.method public static '+slmethod+'\n',
      '  .locals 2\n',
      '  const-string v1, "sink: {'+sid+'"\n',
    ])
    if (vtype == 'Z'):
      code.extend([
        '    invoke-static {p0}, Ljava/lang/String;->valueOf(Z)Ljava/lang/String;\n',
        '    move-result-object v0\n',
        self.log_call,
      ])
    elif (vtype == 'I'):
      code.extend([
        '    invoke-static {p0}, Ljava/lang/String;->valueOf(I)Ljava/lang/String;\n',
        '    move-result-object v0\n',
        self.log_call,
      ])
    elif (vtype == 'B'):
      code.extend([
        '    invoke-static {p0}, Ljava/lang/String;->valueOf(B)Ljava/lang/String;\n',
        '    move-result-object v0\n',
        self.log_call,
      ])
    elif (vtype == 'S'):
      code.extend([
        '    invoke-static {p0}, Ljava/lang/String;->valueOf(S)Ljava/lang/String;\n',
        '    move-result-object v0\n',
        self.log_call,
      ])
    elif (vtype == 'C'):
      code.extend([
        '    invoke-static {p0}, Ljava/lang/String;->valueOf(C)Ljava/lang/String;\n',
        '    move-result-object v0\n',
        self.log_call,
      ])
    elif (vtype == 'F'):
      code.extend([
        '    invoke-static {p0}, Ljava/lang/String;->valueOf(F)Ljava/lang/String;\n',
        '    move-result-object v0\n',
        self.log_call,
      ])
    elif (vtype == 'J'):
      code.extend([
        '    invoke-static {p0}, Ljava/lang/String;->valueOf(J)Ljava/lang/String;\n',
        '    move-result-object v0\n',
        self.log_call,
      ])
    elif (vtype == 'D'):
      code.extend([
        '    invoke-static {p0}, Ljava/lang/String;->valueOf(D)Ljava/lang/String;\n',
        '    move-result-object v0\n',
        self.log_call,
      ])
    elif (vtype == 'Ljava/lang/String;'):
      code.extend([
        '  move-object v0, p0\n',
        self.log_call,
      ])
    code.append(
      '  return-void\n'
      '.end method\n\n'
    )
    self.generated[cp]['methods'][m][sv][line]['code'].extend(code)
    # Invocation
    slmethod_call = cp+'->'+slmethod+'\n'
    self.sl_cntr += 1
    self.generated[cp]['methods'][m][sv][line]['slmethod_call'] = slmethod_call
    return slmethod_call

