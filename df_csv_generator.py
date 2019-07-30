# -*- coding: utf-8 -*-

import io
import sys
import json
from pprint import pprint

import df_csv_funcs as funcs

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
    #self.__load_json(self.parsed_data, '_parsed_data.json')
    self.__load_json(self.data_flows, '_data_flows.json')
    self.__load_json(self.log_ids, '_log_ids.json')
    self.__load_log()

  def __load_json(self, dest, name):
    with open(self.pkg+name, 'r') as f:
      dest.update(json.load(f))

  def __load_log(self):
    self.log = {
      'source': {},
      'sink': {},
    }
    with io.open(self.pkg+'_log.txt', 'r', encoding='utf-8', errors='ignore') as f:
      data = f.read().split('\n')
    for d in data:
      if (d.startswith('source: {')):
        lid, val = self.__load_data(d, len('source: {'))
        self.__add_log(self.log['source'], lid, val)
      if (d.startswith('sink: {')):
        lid, val = self.__load_data(d, len('sink: {'))
        self.__add_log(self.log['sink'], lid, val)

  def __load_data(self, d, s):
    splitter = d.find(': ', s)
    return d[s:splitter], d[splitter+2:-1]

  def __add_log(self, dest, lid, val):
    if (lid not in dest.keys()):
      dest[lid] = []
    dest[lid].append(val)

  def df_to_csv(self, df):
    dtc = funcs.DfToCsv(df, self.log_ids, self.log)
    csv = dtc.run()
    self.csvs.append(csv)

  def df_sink_to_csv(self, df):
    dtc = funcs.DfToCsv(df, self.log_ids, self.log)
    csv = dtc.run()
    self.csvs_sink.append(csv)

if __name__ == '__main__':
  pkg = sys.argv[1]
  DCG = DfCsvGenerator(pkg)

  # Generate csv
  for cp, cpval in DCG.data_flows.items():
    for m, mval in cpval.items():
      for l, lval in mval.items():
        # Source
        #DCG.df_to_csv(lval)
        # Sink
        for sink in lval['sinks']:
          DCG.df_sink_to_csv(sink)

  # Save csv
  for i in range(len(DCG.csvs)):
    with open(pkg+'_df_'+str(i)+'.csv', 'w') as f:
      f.write(DCG.csvs[i])
  for i in range(len(DCG.csvs_sink)):
    with open(pkg+'_df_rev_'+str(i)+'.csv', 'w') as f:
      f.write(DCG.csvs_sink[i])
  print('Done!')

