# -*- coding: utf-8 -*-
# Called by chestbuster.py

import io
import os

class CodeInjector():
  def __init__(self, parsed_data, def_class, gen_codes_def, gen_codes_ins, gen_replaces, src_codes, new_dex_dir):
    self.parsed_data = parsed_data
    self.def_class = def_class
    self.gen_codes_def = gen_codes_def
    self.gen_codes_ins = gen_codes_ins
    self.gen_replaces = gen_replaces
    self.src_codes = src_codes
    self.new_dex_dir = new_dex_dir
    self.__create_dex_dir()

  def __create_dex_dir(self):
    os.mkdir(self.new_dex_dir)

  def inject(self):
    self.__inject_definitions()
    self.__inject_to_original_files()

  def __inject_definitions(self):
    final_code = ''
    for c in self.gen_codes_def:
      final_code += c
    with io.open(self.new_dex_dir+'/'+self.def_class[1:-1]+'.smali', 'w', encoding='utf-8') as f:
      f.write(final_code)

  def __inject_to_original_files(self):
    for smali, svalue in self.parsed_data['classes'].items():
      final_code = ''
      code = self.src_codes[svalue['file_path']]
      for i in range(svalue['linage']):
        if (i in self.gen_codes_ins[smali].keys()):
          final_code += self.gen_codes_ins[smali][i]
        if (i not in self.gen_replaces[smali]):
          final_code += code[i] + '\n'
      # Write to a file
      with io.open(svalue['file_path'], 'w', encoding='utf-8') as f:
        f.write(final_code)

