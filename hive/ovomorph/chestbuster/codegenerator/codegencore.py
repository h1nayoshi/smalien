# -*- coding: utf-8 -*-
# Called by codegenerator.py

from pprint import pprint

from . import codegenfuncs as cgfuncs

class CGCore(cgfuncs.CGFuncs):
  def init_generator(self):
    for class_path, cval in self.parsed_data['classes'].items():
      self.codes_ins[class_path] = {}
      self.replaces[class_path] = {}
      self.generated[class_path] = {
        'global': {},
        'methods': {},
      }
      for method in cval['methods'].keys():
        self.generated[class_path]['methods'][method] = {}
    self.__init_def_class()

  def __init_def_class(self):
    self.codes_def.extend([
      '.class public Lsmalienlog;\n',
      '.super Ljava/lang/Object;\n',
      '\n',
    ])

  def generate_logging_method(self, flow):
    self.codes_def.extend([
      '.method public static SmalienLog(Ljava/lang/String;Ljava/lang/String;)V\n',
      #'.method public static SmalienLog(Ljava/lang/String;)V\n',
      '  .locals 4\n',
      #'  .locals 1\n',
      '  const-string v0, "SmalienLog"\n',
      '  const-string v1, ": "\n',
      '  const-string v2, "}"\n',
      '  new-instance v3, Ljava/lang/StringBuilder;\n',
      '  invoke-direct {v3}, Ljava/lang/StringBuilder;-><init>()V\n',
      '  invoke-virtual {v3, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;\n',
      '  move-result-object v3\n',
      '  invoke-virtual {v3, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;\n',
      '  move-result-object v3\n',
      '  invoke-virtual {v3, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;\n',
      '  move-result-object v3\n',
      '  invoke-virtual {v3, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;\n',
      '  move-result-object v3\n',
      '  invoke-virtual {v3}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;\n',
      '  move-result-object v3\n',
      '  invoke-static {v0, v3}, Landroid/util/Log;->i(Ljava/lang/String;Ljava/lang/String;)I\n',
      '  return-void\n',
      '.end method\n',
    ])
    #self.log_call = '      invoke-static {v0, p1}, '+flow['class_path']+'->SmalienLog(Ljava/lang/String;Ljava/lang/String;)V\n'
    self.log_call = '      invoke-static {v0, v1}, '+self.def_class+'->SmalienLog(Ljava/lang/String;Ljava/lang/String;)V\n'

  def generate_for_a_flow(self, flow, prev_tag):
    # Check if the method is native
    unhandle = self.parsed_data['classes'][flow['class_path']]['methods'][flow['method']]['unhandle']
    if (unhandle):
      return
    # If a var is global
    if (flow['var'].find('->') > -1):
      # Generate a tag for a var
      tag = self.generate_tag_for_global(flow, prev_tag)
    # If a var is local
    else:
      # Check its type
      chk_type = self.check_type(flow['type'])
      if (chk_type):
        # Generate a tag for a var with checking/logging method
        tag = self.generate_tag_for_local(flow, prev_tag)
      else:
        # Generate a tag for a var without checking/logging method
        tag = self.generate_tag_for_local_bad_type(flow, prev_tag)
    #pprint(self.generated)

    if (flow['next'] != []):
      for n in flow['next']:
        self.generate_for_a_flow(n, tag)

  def generate_for_a_sink(self, sink):
    # Check if var is global
    if (sink['var'].find('->') < 0):
      chk_type = self.check_type(sink['type'])
      if (chk_type):
        self.logging_sink(sink)
    # Log for subs
    for sub in sink['subs']:
      if (sub['var'].find('->') < 0):
        chk_type = self.check_type(sub['type'])
        if (chk_type):
          self.logging_sink(sub)

  def generate_final_code(self):
    #pprint(self.generated)
    for cp, cpval in self.generated.items():
      # global
      for sv, svval in cpval['global'].items():
        for sline, sval in svval.items():
          # Definitions
          self.codes_def.extend(sval['code'])
          # Untaggings
          for ut in sval['untagging']['place']:
            if (ut[1] not in self.codes_ins[ut[0]].keys()):
              self.codes_ins[ut[0]][ut[1]] = ''
            self.codes_ins[ut[0]][ut[1]] += 'invoke-static {}, '+sval['untagging']['name']
          # Taggings
          for tl in sval['tagging']['place']:
            if (tl not in self.codes_ins[cp].keys()):
              self.codes_ins[cp][tl] = ''
            self.codes_ins[cp][tl] += 'invoke-static {}, '+sval['tagging']['name']
      # local
      for m, mval in cpval['methods'].items():
        for v, vval in mval.items():
          for vline, val in vval.items():
            # Definitions
            if ('code' in val.keys()):
              self.codes_def.extend(val['code'])
            if ('tagging' in val.keys()):
              for tl in val['tagging']['place']:
                if (tl not in self.codes_ins[cp].keys()):
                  self.codes_ins[cp][tl] = ''
                self.codes_ins[cp][tl] += 'invoke-static {}, '+val['tagging']['name']
            if ('tagging_log' in val.keys()):
              for tl in val['tagging_log']['place']:
                if (tl not in self.codes_ins[cp].keys()):
                  self.codes_ins[cp][tl] = ''
                if (val['type'] in ['J', 'D']):
                  v_2 = v[0]+str(int(v[1:])+1)
                  self.codes_ins[cp][tl] += 'invoke-static/range {'+v+' .. '+v_2+'}, '+val['tagging_log']['name']
                else:
                  self.codes_ins[cp][tl] += 'invoke-static/range {'+v+' .. '+v+'}, '+val['tagging_log']['name']
            # Checking
            if ('checking' in val.keys()):
              for chk in val['checking']['place']:
                if (chk not in self.codes_ins[cp].keys()):
                  self.codes_ins[cp][chk] = ''
                self.codes_ins[cp][chk] += 'invoke-static/range {'+v+' .. '+v+'}, '+val['checking']['name']
                if (val['type'] in ['Z', 'B', 'S', 'C', 'I', 'F']):
                  self.codes_ins[cp][chk] += 'move-result '+v+'\n'
                elif (val['type'] in ['J', 'D']):
                  self.codes_ins[cp][chk] += 'move-result-wide '+v+'\n'
                elif (val['type'] in ['Ljava/lang/String;', 'Ljava/lang/StringBuilder;'] or  val['type'][0] == '['):
                  self.codes_ins[cp][chk] += 'move-result-object '+v+'\n'
            # Data Saving
            if ('saving' in val.keys()):
              if (vline not in self.codes_ins[cp].keys()):
                self.codes_ins[cp][vline] = ''
              self.codes_ins[cp][vline] += 'invoke-static/range {'+v+' .. '+v+'}, '+val['saving']
            # Data Logging
            if ('logging' in val.keys()):
              if (vline not in self.codes_ins[cp].keys()):
                self.codes_ins[cp][vline] = ''
              self.codes_ins[cp][vline] += val['logging']
            # Data Comparison
            if ('comparison' in val.keys()):
              if (vline not in self.codes_ins[cp].keys()):
                self.codes_ins[cp][vline] = ''
              for cmpc in val['comparison']:
                self.codes_ins[cp][vline] += cmpc

      # Untaggings
      for m, mval in cpval['methods'].items():
        for v, vval in mval.items():
          for vline, val in vval.items():
            if ('untagging' in val.keys()):
              for ul in val['untagging']['place']:
                if (ul not in self.codes_ins[cp].keys()):
                  self.codes_ins[cp][ul] = ''
                self.codes_ins[cp][ul] += 'invoke-static {}, '+val['untagging']['name']


