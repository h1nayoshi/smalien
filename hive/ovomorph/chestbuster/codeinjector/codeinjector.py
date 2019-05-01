# -*- coding: utf-8 -*-
# Called by chestbuster.py

class CodeInjector():
  def __init__(self, parsed_data, generated_codes, generated_replaces, src_codes):
    self.parsed_data = parsed_data
    self.generated_codes = generated_codes
    self.generated_replaces = generated_replaces
    self.src_codes = src_codes

  def inject(self):
    for smali, svalue in self.parsed_data.items():
      final_code = ''
      code = self.src_codes[svalue['file_path']]
      for i in range(svalue['linage']):
        if (i in self.generated_codes[smali].keys()):
          final_code += self.generated_codes[smali][i]
        if (i not in self.generated_replaces[smali]):
          final_code += code[i] + '\n'
      # Write to a file
      with open(svalue['file_path'], 'w') as f:
        f.write(final_code)

