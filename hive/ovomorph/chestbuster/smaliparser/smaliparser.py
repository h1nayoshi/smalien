# -*- coding: utf-8 -*-
# Called by chestbuster.py

import io
import re
from pprint import pprint

from .methodparser import methodparser as mparser

class SmaliParser(mparser.MethodParser):
  def __init__(self, smalis, activities):
    # Init SmaliParser
    self.smalis = smalis
    self.activities = activities
    self.src_codes = {}
    self.parsed_data = {
      'classes': {},
      'containers': {},
    }
    self.__init_containers()

    # Init MethodParser
    super(SmaliParser, self).__init__()

  def parse(self):
    # Load source codes
    #print('   [*] Loading src codes')
    self.__load_src_codes()
    
    #print('   [*] Getting basic info')
    # Get smali basic info
    self.__get_smali_info()

    #print('   [*] Parsing method')
    # Parse each method
    self.parse_methods()

    return self.src_codes, self.parsed_data

  def __init_containers(self):
    self.parsed_data['containers'] = {
      'bundle': {},
      'preference': {},
      'jsonobj': {},
    }
    for con in self.parsed_data['containers'].values():
      con['put'] = {}
      con['get'] = {}

  def __load_src_codes(self):
    for smali in self.smalis:
      with io.open(smali, 'r', encoding='utf-8') as f:
        self.src_codes[smali] = f.read().split('\n')

  def __get_smali_info(self):
    for smali in self.smalis:
      class_path = self.__get_class_path(smali)
      # If a class exists
      if (class_path):
        self.parsed_data['classes'][class_path] = {
          'linage': len(self.src_codes[smali]),
          'file_path': smali,
        }
        self.__get_static_vars(class_path, smali)
        self.__get_instances(class_path, smali)

  def __get_class_path(self, smali):
    c = self.src_codes[smali][0]
    if (c.find('.class') > -1):
      return c.split(' ')[-1]
    else:
      return False

  def __get_static_vars(self, class_path, smali):
    self.parsed_data['classes'][class_path]['static_vars'] = {}
    start, end = self.__get_range(smali, '# static fields')
    if (start is None):
      return
    for c in self.src_codes[smali][start:end]:
      if (re.search(r'^.field ', c) is not None and c.find(' static ') > -1):
        var = self.__extract_var(c)
        if (var):
          self.parsed_data['classes'][class_path]['static_vars'][class_path + '->' + var] = {
            'name': var.split(':')[0],
            'type': var.split(':')[1],
            'class_path': class_path,
            'put': {},
            'get': {},
          }

  def __get_instances(self, class_path, smali):
    self.parsed_data['classes'][class_path]['instances'] = {}
    start, end = self.__get_range(smali, '# instance fields')
    if (start is None):
      return
    for c in self.src_codes[smali][start:end]:
      if (re.search(r'^.field ', c) is not None):
        var = self.__extract_var(c)
        if (var):
          self.parsed_data['classes'][class_path]['instances'][class_path + '->' + var] = {
            'name': var.split(':')[0],
            'type': var.split(':')[1],
            'class_path': class_path,
            'put': {},
            'get': {},
          }

  def __extract_var(self, c):
    items = c.split(' ')
    for item in items:
      if (item.find(':') > -1):
        return item
    return False

  def __get_range(self, smali, target):
    for i in range(len(self.src_codes[smali])):
      c = self.src_codes[smali][i]
      if (c.find(target) > -1):
        start = i+1
        for j in range(start, len(self.src_codes[smali])):
          c = self.src_codes[smali][j]
          if (re.search(r'^\# *', c) is not None):
            return start, j
        return start, len(self.src_codes[smali])
    return None, None

