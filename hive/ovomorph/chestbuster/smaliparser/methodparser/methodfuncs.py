# -*- coding: utf-8 -*-
# Called by methodparser.py

import re
import sys
from pprint import pprint

class MethodFuncs(object):
  def __init__(self):
    self.crnt_block_id = 0
    self.gotoes = ['goto', 'goto/16', 'goto/32']
    self.rets = ['return', 'return-void', 'return-wide', 'return-object']
    self.mpaths = []

  def find_methods(self, class_path, cval):
    cval['methods'] = {}
    src_code = self.src_codes[cval['file_path']]
    i = 0
    while i < cval['linage']:
      c = src_code[i]
      if (re.search(r'^\.method', c) is not None):
        # i is a start line of a method
        mname = c.split(' ')[-1]
        mend = self.__get_mend(i, src_code, cval['linage'])
        cval['methods'][mname] = {
          'start': i,
          'end': mend,
          'callers': [],
          'target': False,
        }
        self.__get_ret_vars(cval['methods'][mname], src_code, mname.split(')')[-1])
        i = mend+1
      else:
        i+=1

  def __get_mend(self, mstart, src_code, linage):
    for i in range(mstart, linage):
      c = src_code[i]
      if (re.search('^\.end method', c) is not None):
        break
    return i

  def __get_ret_vars(self, mval, src_code, ret_type):
    mval['ret'] = []
    for i in range(mval['start']+1, mval['end']):
      c = src_code[i]
      if (c != '' and c.split(' ')[4] in ['return-object', 'return-wide', 'return']):
        mval['ret'].append({
          'line': i,
          'var': c.split(' ')[-1],
          'type': ret_type,
        })
      if (c.find(' return-void') > -1):
        mval['ret'].append({
          'line': i,
          'var': 'none',
          'type': ret_type,
        })
    if (mval['ret'] == []):
      mval['ret'].append({
        'line': mval['end'],
        'var': 'none',
        'type': ret_type,
      })

  def generate_method_paths(self):
    self.mpaths = {}
    for class_path, cval in self.parsed_data.items():
      for method in cval['methods'].keys():
        target = ['L']
        subs = class_path[1:].split('/')
        for sub in subs[:-1]:
          target.append(sub+'/')
        target.append(subs[-1])
        self.__mpath_append(self.mpaths, target, class_path+'->'+method)

  def __mpath_append(self, mps, target, m):
    d = target.pop(0)
    if (len(target) == 1):
      if (d not in mps.keys()):
        mps[d] = {target[0]: [m]}
      elif (target[0] not in mps[d].keys()):
        mps[d][target[0]] = [m]
      else:
        mps[d][target[0]].append(m)
    else:
      if (d not in mps.keys()):
        mps[d] = {}
      self.__mpath_append(mps[d], target, m)

  def find_method_calls(self, tcp, tm, mval, src_code):
    mval['calls'] = []
    # Parse a method
    for i in range(mval['start']+1, mval['end']):
      c = src_code[i]
      if (c == ''):
        pass
      elif (c.find(' invoke-') > -1):
        path = self.__get_invoked_method(c.split('}, ')[1], '', self.mpaths)
        if (path is not None):
          cp = path.split('->')[0]
          m = path.split('->')[1]
          params = self.__get_params(c)
          ret = self.__get_ret_var(src_code, i+2)
          # Add call
          mval['calls'].append({
            'line': i,
            'code': c,
            'method': m,
            'class_path': cp,
            'params': params,
            'ret': ret,
          })
          # Add caller
          self.parsed_data[cp]['methods'][m]['callers'].append({
            'class_path': tcp,
            'method': tm,
            'line': i,
            'params': params,
            'ret': {
              'line': ret['line'],
              'var': ret['var'],
              'type': m.split(')')[-1],
            },
          })

  def __get_invoked_method(self, c, path, mps):
    m = None
    for mp, mpval in mps.items():
      if (type(mpval) == list):
        for pv in mpval:
          if (c.startswith(pv)):
            return pv
      elif (c.startswith(path+mp)):
        m = self.__get_invoked_method(c, path+mp, mpval)
    return m

  def __get_params(self, c):
    params = c[c.find('{')+1:c.find('}')]
    if (params.find(' .. ') > -1):
      attr = params.split(' ')[0][0]
      start = int(params.split(' ')[0][1:])
      end = int(params.split(' ')[-1][1:])
      ret = []
      for i in range(start, end+1):
        ret.append(attr+str(i))
      return ret
    else:
      return params.split(', ')

  def __get_ret_var(self, src_code, i):
    c = src_code[i]
    while (c.find('    :') > -1 or c.find('    .') > -1 or c == ''):
      i += 1
      c = src_code[i]
    ret = {
      'var': None,
      'line': None,
    }
    if (c.find(' move-result') > -1):
      ret['var'] = c.split(' ')[-1]
      ret['line'] = i
    return ret

  def detect_target_methods(self, mval):
    if (mval['target'] == False):
      cntr = 1
      mval['target'] = True
      for call in mval['calls']:
        nmval = self.parsed_data[call['class_path']]['methods'][call['method']]
        cntr += self.detect_target_methods(nmval)
      return cntr
    return 0

  def construct_blocks(self, mval, src_code):
    mval['blocks'] = {}
    self.crnt_block_id = 0
    bfrom = { # First block's origin
      'blocks': [],
      'line': -1,
      'opcode': 'method call',
    }
    #print '  mval start, end', mval['start'], mval['end']
    bend, bto_line = self.__get_block_end_and_to(mval, mval['start']+1, src_code)
    bto = { # First blocks' dest
      'blocks': [],
      'line': bto_line,
    }
    # Analyze control flows and find blocks
    self.__find_blocks(mval, bfrom, mval['start'], bend, bto, src_code)

    # Find blocks' origin blocks
    self.__find_origin_blocks(mval['blocks'])

    # Find blocks' dest blocks
    self.__find_dest_blocks(mval['blocks'])

  def __find_blocks(self, mval, bfrom, crnt_start, crnt_end, bto, src_code):
    mval['blocks'][self.crnt_block_id] = {
      'from': bfrom,
      'start': crnt_start,
      'end': crnt_end,
      'to': bto
    }

    for i in range(crnt_start, crnt_end):
      c = src_code[i]
      # if-kinds
      if (c.find(', :cond_') > -1): # Find new block's origin
        cond = '    ' + c.split(' ')[-1]
        new_from_line = i
        for j in range(mval['start'], mval['end']): # Find new block's start
          c = src_code[j]
          if (c.find(cond) > -1):
            chk = self.__is_block_new(mval, j)
            if (chk):
              new_start = j
              new_end, new_to_line = self.__get_block_end_and_to(mval, new_start, src_code)
              new_from = {
                'line': new_from_line,
                'opcode': 'if'
              }
              new_to = { 'line': new_to_line }
              self.crnt_block_id += 1
              self.__find_blocks(mval, new_from, new_start, new_end, new_to, src_code)
            else:
              self.crnt_block_id += 1
              mval['blocks'][self.crnt_block_id] = {
                'from': bfrom,
                'start': crnt_start,
                'end': new_from_line,
                'to': { 'line': j },
              }
            break
      # switch-kinds
      elif (c.find(' packed-switch ') > -1 or c.find(' sparse-switch ') > -1 ): # Find new block's origin
        slabels, switch_end = self.__get_switch_labels(c, i, mval['end'], src_code)
        new_from_line = i
        for sl in slabels:
          for j in range(i+1, switch_end): # Find new block's start
            c = src_code[j]
            if (c.find(sl) > -1):
              chk = self.__is_block_new(mval, j)
              if (chk):
                new_start = j
                new_end, new_to_line = self.__get_block_end_and_to(mval, new_start, src_code)
                new_from = {
                  'line': new_from_line,
                  'opcode': 'switch'
                }
                new_to = { 'line': new_to_line }
                self.crnt_block_id += 1
                self.__find_blocks(mval, new_from, new_start, new_end, new_to, src_code)
              break
      # try-catch
      elif (c.find(' :try_start_') > -1): # Find new block's origin range start
        new_from_range_start = i
        end_label = ':try_end_'+str(c.split('_')[-1])
        for j in range(i+1, mval['end']): # Find new block's origin range end
          c = src_code[j]
          if (c.find(end_label) > -1):
            new_from_range_end = j
            catch_label = '    '+src_code[j+1].split(' ')[-1]
            for k in range(mval['start'], mval['end']): # Find new block's start
              c = src_code[k]
              if (c == catch_label):
                chk, bval = self.__is_block_new_for_try_catch(mval, k, new_from_range_start)
                if (chk == 'new block'):
                  new_start = k
                  new_end, new_to_line = self.__get_block_end_and_to(mval, new_start, src_code)
                  new_from = {
                    'range': [{
                      'start': new_from_range_start,
                      'end': new_from_range_end,
                    }],
                    'opcode': 'try-catch'
                  }
                  new_to = { 'line': new_to_line }
                  self.crnt_block_id += 1
                  self.__find_blocks(mval, new_from, new_start, new_end, new_to, src_code)
                elif (chk == 'new range'):
                  bval['from']['range'].append({
                    'start': new_from_range_start,
                    'end': new_from_range_end,
                  })
                break
            break

  def __get_block_end_and_to(self, mval, new_start, src_code):
    for k in range(new_start, mval['end']): # Find new block's end
      c = src_code[k]
      if (c != '' and c.split(' ')[4] in self.gotoes):
        new_end = k
        goto = '    ' + c.split(' ')[-1]
        for l in range(mval['start'], mval['end']): # Find new block's dest
          c = src_code[l]
          if (c == goto):
            return new_end, l
      elif (c != '' and c.split(' ')[4] in self.rets):
        return k, -1
        break
    return mval['end'], -1

  def __is_block_new(self, mval, new_start):
    for block, bval in mval['blocks'].items():
      if (bval['start'] == new_start):
        return False
    return True

  def __is_block_new_for_try_catch(self, mval, new_start, new_from_range_start):
    for block, bval in mval['blocks'].items():
      if (bval['start'] == new_start):
        for r in bval['from']['range']:
          if (r['start'] == new_from_range_start):
            return 'not new', None
        return 'new range', bval
    return 'new block', None

  def __get_switch_labels(self, c, start, mend, src_code):
    slabels = []
    code = c.split(' ')[4]
    data = c.split(', ')[-1]
    end_mark = '.end '+code
    for i in range(start+1, mend):
      c = src_code[i]
      if (c.find(data) > -1):
        lstart = i + 2
        for j in range(lstart, mend):
          c = src_code[j]
          if (c.find(end_mark) > -1):
            lend = j
            for k in range(lstart, lend):
              slabels.append(src_code[k].split(' ')[-1])
    return slabels, lstart-2

  def __find_origin_blocks(self, blocks):
    for block, bval in blocks.items():
      if (bval['from']['opcode'] != 'method call'):
        bval['from']['blocks'] = []
        for chk_block, chk_bval in blocks.items():
          if (bval['from']['opcode'] in ['if', 'switch']):
            if (bval['from']['line'] >= chk_bval['start'] and bval['from']['line'] <= chk_bval['end']):
              bval['from']['blocks'].append(chk_block)
          elif (bval['from']['opcode'] == 'try-catch'):
            for r in bval['from']['range']:
              if (r['start'] >= chk_bval['start'] and r['start'] <= chk_bval['end']):
                bval['from']['blocks'].append(chk_block)
              elif (r['end'] >= chk_bval['start'] and r['end'] <= chk_bval['end']):
                bval['from']['blocks'].append(chk_block)

  def __find_dest_blocks(self, blocks):
    for block, bval in blocks.items():
      bval['to']['blocks'] = []
      if (bval['to']['line'] != -1):
        for chk_block, chk_bval in blocks.items():
          if (bval['to']['line'] >= chk_bval['start'] and bval['to']['line'] <= chk_bval['end']):
            bval['to']['blocks'].append(chk_block)

