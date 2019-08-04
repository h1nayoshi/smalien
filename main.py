# -*- coding: utf-8 -*-

import os
import sys
import json
import subprocess
from hive.queen import activate_queen

def load_keystore():
  # Load keystore info
  with open('keystore_conf.txt', 'r') as f:
    return f.read().split('\n')

def load_options(argv):
  ppe = False
  smalien_path = None
  i = 1
  while i < len(argv)-1:
    if (argv[i] == '-ppe'):
      ppe = True
      i += 1
    elif (argv[i] == '-path'):
      smalien_path = sys.argv[i+1]
      os.chdir(smalien_path)
      i += 2
  return ppe, smalien_path

if __name__ == '__main__':
  if (len(sys.argv) > 1):
    ppe, smalien_path = load_options(sys.argv)
    keystore = load_keystore()
    print('[*] Activating Smalien')
    pkg, parsed_data, data_flows, log_ids, host_dest = activate_queen(sys.argv[-1], keystore, smalien_path, ppe)
    print('[*] Application generated')
    print(' [+] '+host_dest+'implanted_'+pkg+'.apk')
  else:
    print('[*] Usage: python '+__file__+' <apk_path>')

