# -*- coding: utf-8 -*-

import sys
import json
from pprint import pprint
#from SuperMarkdown import SuperMarkdown

dest_cc = 'output_class_calls.md'
dest_df = 'output_data_flows.md'

def generate_mermaid(parsed_data, data_flows):
  print('[*] Generating...')
  #supermd = SuperMarkdown.SuperMarkdown()
  #supermd.export_url = export_url
  output = '```mermaid\n'
  output += 'graph LR\n'
  output_df = '```mermaid\n'
  output_df += 'graph LR\n'

  cp_cntr = 0
  m_cntr = 0
  method_id = {}
  # Method calls
  # Currently unused due to an amount of methods
  """
  for cp, cval in parsed_data.items():
    #added = False
    cp = cp[1:-1].replace('/', '.')
    output += '    '+cp+'\n'
    #print cp
    #for m, mval in cval['methods'].items():
    #  if (mval['target'] == True):
    #    if (not added):
    #      output += '    subgraph '+cp+'\n'
    #      cp_cntr += 1
    #      added = True
    #    #print ' ', m
    #    output += '    '+str(m_cntr)+'["'+m+'"]\n'
    #    method_id[m] = m_cntr
    #    m_cntr += 1
    #if (added):
    #  output += '    end\n'
  """

  # Class calls
  cntr = 0
  for cp, cval in parsed_data.items():
    scp = cp[1:-1].replace('/', '.')
    sourced = False
    sinked = False
    for m, mval in cval['methods'].items():
      if (mval['target'] == True):
        for call in mval['calls']:
          cntr += 1
          dcp = call['class_path'][1:-1].replace('/', '.')
          output += '    '+scp+'-.->'+dcp+';\n'
        #if (not sourced and mval['sources'] != {}):
        #  output += '    style '+scp+' fill:#f00,stroke:#fff,stroke-width:4px\n'
        #  sourced = True
        #if (not sinked and mval['sinks'] != {}):
        #  output += '    style '+scp+' fill:#0f0,stroke:#fff,stroke-width:4px\n'
        #  sinked = True
        #  #print cntr, ' adding a call', cp, m, call['method']
        #  #output += '    '+str(method_id[m])+'-->'+str(method_id[call['method']])+';\n'

  # Data flows
  for cp, cval in data_flows.items():
    scp = cp[1:-1].replace('/', '.')
    for m, mval in cval.items():
      for fline, fval in mval.items():
        df_temp = []
        walk_df(fval['flow'], scp, df_temp)
        for dfo in df_temp:
          output += dfo
          output_df += dfo
        output += '    style '+scp+' fill:#f00,stroke:#fff,stroke-width:4px\n'
        output_df += '    style '+scp+' fill:#f00,stroke:#fff,stroke-width:4px\n'

  print(' [+] Calls: '+str(cntr))
  print('[*] Done! Please use markdown viewer such as Haroopad to check the graphs.')

  output += '```'
  output_df += '```'

  #supermd.add_content(text=output)
  #supermd.export()

  with open(dest_cc, 'w') as f:
    f.write(output)
  with open(dest_df, 'w') as f:
    f.write(output_df)

def walk_df(flows, prev_cp, df_temp):
  dcp = flows['class_path'][1:-1].replace('/', '.')
  if (prev_cp != dcp):
    df_temp.extend([
      '    '+prev_cp+'==>'+dcp+'\n',
      '    style '+dcp+' fill:#f80,stroke:#fff,stroke-width:4px\n',
    ])
  for n in flows['next']:
    walk_df(n, dcp, df_temp)

if __name__ == '__main__':
  if (len(sys.argv) == 3):
    with open(sys.argv[1], 'r') as f:
      parsed_data = json.load(f)
    with open(sys.argv[2], 'r') as f:
      data_flows = json.load(f)
    generate_mermaid(parsed_data, data_flows)
  else:
    print('[*] Usage: python '+__file__+' parsed_data.txt data_flows.txt')

