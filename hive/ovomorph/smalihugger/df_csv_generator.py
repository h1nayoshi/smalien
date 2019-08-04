# -*- coding: utf-8 -*-

import io
import sys
import json
from pprint import pprint

from . import df_csv_funcs as funcs

class DfCsvGenerator():
  def __init__(self, pkg):
    self.pkg = pkg
    self.parsed_data = {}
    self.data_flows = {}
    self.log_ids = {}
    self.log = {
      'source': {},
      'sink': {},
    }

    self.csvs = []
    self.csvs_sink = []
    self.output_file = pkg+'_data_flows_csv.json'

    self.__load_files()

  def __load_files(self):
    self.__load_json(self.data_flows, '_data_flows.json')

  def __load_json(self, dest, name):
    with open(self.pkg+name, 'r') as f:
      dest.update(json.load(f))

  def __load_data(self, d, s):
    splitter = d.find(': ', s)
    return d[s:splitter], d[splitter+2:-1]

  def __add_log(self, dest, lid, val):
    if (lid not in dest.keys()):
      dest[lid] = []
    dest[lid].append(val)

  def df_to_csv(self, df, sinks):
    dtc = funcs.DfToCsv(df, sinks)
    csv = dtc.run()
    self.csvs.append(csv)

  def df_sink_to_csv(self, df):
    dtc = funcs.DfToCsv(df, [])
    csv = dtc.run()
    self.csvs_sink.append(csv)

def run_csv_generator(pkg):
  print(' [*] Generating CSV files')
  DCG = DfCsvGenerator(pkg)

  # Generate csv
  for cp, cpval in DCG.data_flows.items():
    for m, mval in cpval.items():
      for l, lval in mval.items():
        # Source
        DCG.df_to_csv(lval, lval['sinks'])
        # Sink
        for sink in lval['sinks']:
          DCG.df_sink_to_csv(sink)

  # Save csv
  csv_files = {'source': [], 'sink': []}
  for i in range(len(DCG.csvs)):
    csv_files['source'].append(pkg+'_df_'+str(i)+'.csv')
    with open(pkg+'_df_'+str(i)+'.csv', 'w') as f:
      f.write(DCG.csvs[i])
  for i in range(len(DCG.csvs_sink)):
    csv_files['sink'].append(pkg+'_df_rev_'+str(i)+'.csv')
    with open(pkg+'_df_rev_'+str(i)+'.csv', 'w') as f:
      f.write(DCG.csvs_sink[i])
  with open(pkg+'csvlist.json', 'w') as f:
    json.dump(csv_files, f)
  print('  [+] CSV files are generated.')

if __name__ == '__main__':
  pkg = sys.argv[1]
  run_csv_generator(pkg)

