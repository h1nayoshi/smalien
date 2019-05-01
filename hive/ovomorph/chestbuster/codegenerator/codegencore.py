# -*- coding: utf-8 -*-
# Called by codegenerator.py

from pprint import pprint

from . import codegenfuncs as cgfuncs

class CGCore(cgfuncs.CGFuncs):
  def init_generator(self):
    for class_path, cval in self.parsed_data.items():
      self.codes[class_path] = {}
      self.replaces[class_path] = {}
      self.generated[class_path] = {
        'static': {},
        'methods': {},
      }
      for method in cval['methods'].keys():
        self.generated[class_path]['methods'][method] = {}

  def generate_logging_method(self, flow):
    self.generated[flow['class_path']]['logging'] = [
      '.method public static SmalienLog(Ljava/lang/String;Ljava/lang/String;)V\n',
      #'.method public static SmalienLog(Ljava/lang/String;)V\n',
      '  .locals 3\n',
      #'  .locals 1\n',
      '  const-string v0, "SmalienLog"\n',
      '  const-string v1, " : "\n',
      '  new-instance v2, Ljava/lang/StringBuilder;\n',
      '  invoke-direct {v2}, Ljava/lang/StringBuilder;-><init>()V\n',
      '  invoke-virtual {v2, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;\n',
      '  move-result-object v2\n',
      '  invoke-virtual {v2, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;\n',
      '  move-result-object v2\n',
      '  invoke-virtual {v2, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;\n',
      '  move-result-object v2\n',
      '  invoke-virtual {v2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;\n',
      '  move-result-object v2\n',
      '  invoke-static {v0, v2}, Landroid/util/Log;->i(Ljava/lang/String;Ljava/lang/String;)I\n',
      '  return-void\n',
      '.end method\n',
    ]
    #self.log_call = '      invoke-static {v0, p1}, '+flow['class_path']+'->SmalienLog(Ljava/lang/String;Ljava/lang/String;)V\n'
    self.log_call = '      invoke-static {v0, v1}, '+flow['class_path']+'->SmalienLog(Ljava/lang/String;Ljava/lang/String;)V\n'

  def generate_for_a_flow(self, flow, prev_tag):
    # If a var is static
    if (flow['var'].find('->') > -1):
      # Generate a tag for a var
      tag = self.generate_tag_for_static(flow, prev_tag)
    # If a var is not static
    else:
      # Check its type
      chk_type = self.check_type(flow['type'])
      if (chk_type):
        # Generate a tag for a var with checking-method
        tag = self.generate_tag_for_non_static(flow, prev_tag)
      else:
        # Generate a tag for a var without checking-method
        tag = self.generate_tag_for_non_static_bad_type(flow, prev_tag)
    #pprint(self.generated)

    if (flow['next'] != []):
      for n in flow['next']:
        self.generate_for_a_flow(n, tag)

  def generate_final_code(self):
    #pprint(self.generated)
    for cp, cpval in self.generated.items():
      if (3 not in self.codes[cp].keys()):
        self.codes[cp][3] = ''
      # Logging method
      if ('logging' in cpval.keys()):
        for c in self.generated[cp]['logging']:
          self.codes[cp][3] += c
      # Static
      for sv, svval in cpval['static'].items():
        for sline, sval in svval.items():
          # Definitions
          for c in sval['code']:
            self.codes[cp][3] += c
          # Untaggings
          for ut in sval['untagging']['place']:
            if (ut[1] not in self.codes[ut[0]].keys()):
              self.codes[ut[0]][ut[1]] = ''
            self.codes[ut[0]][ut[1]] += 'invoke-static {}, '+sval['untagging']['name']
          # Taggings
          for tl in sval['tagging']['place']:
            if (tl not in self.codes[cp].keys()):
              self.codes[cp][tl] = ''
            self.codes[cp][tl] += 'invoke-static {}, '+sval['tagging']['name']
      # Non static
      for m, mval in cpval['methods'].items():
        for v, vval in mval.items():
          for vline, val in vval.items():
            # Definitions
            if ('code' in val.keys()):
              for c in val['code']:
                self.codes[cp][3] += c
            if ('tagging' in val.keys()):
              for tl in val['tagging']['place']:
                if (tl not in self.codes[cp].keys()):
                  self.codes[cp][tl] = ''
                self.codes[cp][tl] += 'invoke-static {}, '+val['tagging']['name']
            # Checking
            if ('checking' in val.keys()):
              for chk in val['checking']['place']:
                if (chk not in self.codes[cp].keys()):
                  self.codes[cp][chk] = ''
                self.codes[cp][chk] += 'invoke-static/range {'+v+' .. '+v+'}, '+val['checking']['name']
                if (val['type'] in ['Z', 'B', 'S', 'C', 'I', 'F']):
                  self.codes[cp][chk] += 'move-result '+v+'\n'
                elif (val['type'] in ['J', 'D']):
                  self.codes[cp][chk] += 'move-result-wide '+v+'\n'
                elif (val['type'] in ['Ljava/lang/String;', 'Ljava/lang/StringBuilder;'] or  val['type'][0] == '['):
                  self.codes[cp][chk] += 'move-result-object '+v+'\n'
            # Data Saving
            if ('saving' in val.keys()):
              if (vline not in self.codes[cp].keys()):
                self.codes[cp][vline] = ''
              self.codes[cp][vline] += 'invoke-static/range {'+v+' .. '+v+'}, '+val['saving']
            # Data Logging
            if ('logging' in val.keys()):
              if (vline not in self.codes[cp].keys()):
                self.codes[cp][vline] = ''
              self.codes[cp][vline] += val['logging']
            # Data Comparison
            if ('comparison' in val.keys()):
              if (vline not in self.codes[cp].keys()):
                self.codes[cp][vline] = ''
              for cmpc in val['comparison']:
                self.codes[cp][vline] += cmpc

      # Untaggings
      for m, mval in cpval['methods'].items():
        for v, vval in mval.items():
          for vline, val in vval.items():
            if ('untagging' in val.keys()):
              for ul in val['untagging']['place']:
                if (ul not in self.codes[cp].keys()):
                  self.codes[cp][ul] = ''
                self.codes[cp][ul] += 'invoke-static {}, '+val['untagging']['name']


