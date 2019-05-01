# -*- coding: utf-8 -*-
# Called by methodparser.py

import re
from pprint import pprint

from .sources import sources as srcs
from .implicits import implicits as imps
from .sinks import sinks

class SisParser():
  mval = ''
  src_code = ''
  def find_sis(self, mval, src_code):
    SisParser.mval = mval
    SisParser.src_code = src_code
    mval['sources'] = {}
    mval['implicits'] = {}
    mval['sinks'] = {}

    for i in range(mval['start'], mval['end']):
      c = src_code[i]
      self.__find_sources(i, c)
      self.__find_implicits(i, c)
      self.__find_sinks(i, c)

  def __find_sources(self, i, c):
    for src in srcs:
      if (c.find(src['code']) > -1):
        dest, dline = self.__get_invoke_dest(i+2)
        SisParser.mval['sources'][i] = {
          'method': src['code'],
          'type': src['type'],
          'data': src['data'],
          'dest': dest,
          'dest_line': dline,
          'code': c,
        }

  def __get_invoke_dest(self, i):
    c = SisParser.src_code[i]
    while (c.find('    :') > -1 or c.find('    .') > -1 or c == ''):
      i += 1
      c = SisParser.src_code[i]
    return c.split(' ')[-1], i

  def __find_implicits(self, i, c):
    for imp in imps:
      if (c.find(imp['code']) > -1):
        if (imp['group'] == 0):
          vs = ''.join(c.split(' ')[5:-1]).split(',')[:-1]
        elif (imp['group'] == 1):
          vs = [c.split(', ')[0].split(' ')[-1]]
        elif (imp['group'] == 2):
          vs = ''.join(c.split(' ')[-2:]).split(',')
        elif (imp['group'] == 3):
          vs = [c.split(' ')[-1]]
        elif (imp['group'] == 4):
          params = self.__get_params(c)
          if (c.find(' invoke-static') > -1):
            vs = params
          else:
            vs = params[1:]
        elif (imp['group'] == 4):
          vs = self.__get_params(c)
        SisParser.mval['implicits'][i] = {
          'method': imp['code'],
          'group': imp['group'],
          'vars': vs,
          'code': c,
        }

  def __find_sinks(self, i, c):
    for sink in sinks:
      if (c.find(sink['code']) > -1):
        params = self.__get_params(c)
        params = self.__find_sink_params(params, sink['svars'])
        SisParser.mval['sinks'][i] = {
          'method': sink['code'],
          'line': i,
          'vars': params,
          'code': c,
          'type': sink['type'],
        }

  def __get_params(self, c):
    params = c[c.find('{')+1:c.find('}')]
    if (params == ''):
      return []
    elif (params.find(' .. ') > -1):
      prefix = params.split(' ')[0][0]
      start = int(params.split(' ')[0][1:])
      end = int(params.split(' ')[-1][1:])
      ret = []
      for i in range(start, end+1):
        ret.append(prefix+str(i))
      return ret
    else:
      return params.split(', ')

  def __find_sink_params(self, params, svars):
    ret = []
    for s in svars:
      ret.append(params[s])
    return ret

