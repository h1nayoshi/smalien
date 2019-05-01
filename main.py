# -*- coding: utf-8 -*-

import sys
import json
from hive.queen import activate_queen

fname_pd = 'parsed_data.json'
fname_df = 'data_flows.json'

# Load keystore info
with open('keystore_conf.txt', 'r') as f:
  keystore = f.read().split('\n')

def output_to_file(fname, data):
  r = json.dumps(data)
  with open(fname, 'w') as f:
    f.write(r)

if __name__ == '__main__':
  if (len(sys.argv) == 2):
    print('[*] Activating Smalien')
    parsed_data, data_flows = activate_queen(sys.argv[1], keystore)
    print('[*] Writing the results to files')
    output_to_file(fname_pd, parsed_data)
    output_to_file(fname_df, data_flows)
    print('[*] Done!')
  else:
    print('[*] Usage: python '+__file__+' <apk_path>')

