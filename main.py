# -*- coding: utf-8 -*-

import sys
import json
from hive.queen import activate_queen

fname_pd = '_parsed_data.json'
fname_df = '_data_flows.json'
fname_lid = '_log_ids.json'

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
    pkg, parsed_data, data_flows, log_ids = activate_queen(sys.argv[1], keystore)
    print('[*] Writing the results to files')
    output_to_file(pkg+fname_pd, parsed_data)
    output_to_file(pkg+fname_df, data_flows)
    output_to_file(pkg+fname_lid, log_ids)
    print('[*] Done!')
  else:
    print('[*] Usage: python '+__file__+' <apk_path>')

