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
    'Ljava/lang/StringBuilder;',
  ]

  def check_type(self, vtype):
    if (vtype in CGFuncs.target_types or (vtype[0] == '[' and vtype.find('unknown') < 0)):
      return True
    return False

  def generate_tag_for_static(self, flow, prev_tag):
    v = flow['var']
    vtype = flow['type']
    line = flow['line']
    cp = v.split('->')[0]
    if (v in self.generated[cp]['static'].keys()):
      if (line in self.generated[cp]['static'][v].keys()):
        return cp+'->'+self.generated[cp]['static'][v][line]['tag']
    else:
      self.generated[cp]['static'][v] = {}
    tag = 'Tag_'+v.split('->')[-1].split(':')[0]+'_'+str(line)+'_'+str(self.tag_cntr)+':C'
    code = []
    # Define a tag
    self.__define_tag(code, tag)
    # Define a tagging method
    self.__define_tagging_method(code, cp, tag, prev_tag)
    # Define a untagging method
    self.__define_untagging_method(code, cp, tag)
    utg_place = []
    self.__untagging_static(cp, v, utg_place)
    self.generated[cp]['static'][v][line] = {
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

  def generate_tag_for_non_static(self, f, prev_tag):
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
      mstart = self.parsed_data[cp]['methods'][m]['start']
      utg_place.append(mstart+1)
    self.__untagging_non_static(cp, m, areas, v, utg_place)
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
      'tagging': {
        'name': cp+'->tagging'+tag.split(':')[0]+'()V\n',
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

  def generate_tag_for_non_static_bad_type(self, f, prev_tag):
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
      mstart = self.parsed_data[cp]['methods'][m]['start']
      utg_place.append(mstart+1)
    self.__untagging_non_static(cp, m, areas, v, utg_place)
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

  def __untagging_static(self, cp, v, untag):
    for ucp, ucpval in self.parsed_data[cp]['static_vars'][v]['put'].items():
      for um, umval in ucpval.items():
        for uline, uval in umval.items():
          if (uval['sourced'] == 'no'):
            if ([ucp, uline+1] not in untag):
              untag.append([ucp, uline+1])

  def __untagging_non_static(self, cp, m, areas, v, untag):
    for area in areas:
      if (area['subseq'] == -1):
        chk_ret = self.__check_ret(cp, m, area['end'], v)
        if (chk_ret is None):
          if (area['end']+1 not in untag):
            untag.append(area['end']+1)
        elif (chk_ret == 'ret line'):
          if (area['end'] not in untag):
            untag.append(area['end'])
          

  def __check_ret(self, cp, m, end, v):
    ret = None
    for r in self.parsed_data[cp]['methods'][m]['ret']:
      if (r['line'] == end and r['var'] == v):
        return 'returned'
      elif (r['line'] == end):
        ret = 'ret line'
    return ret

