# -*- coding: utf-8 -*-

import os
import sys

from . import xenomorph
from .ovomorph.smalihugger import smalihugger

def activate_queen(host, keystore, smalien_path):
  print(' [+] Target host: '+host)

  if (smalien_path is not None):
    host_dest = smalien_path+'/hive/workspace/'
  else:
    host_dest = os.path.abspath('.')+'/hive/workspace/'

  ret = xenomorph.init_hive(host, host_dest)
  if (not ret):
    print('[-!-] Failed to init the hive')
    sys.exit()

  ret, pkg, parsed_data, data_flows, log_ids = smalihugger.run(host_dest, keystore)
  if (not ret):
    print('[-!-] Failed to hatch the egg')

  print(' [*] All analysis done')

  return pkg, parsed_data, data_flows, log_ids

#if __name__ == '__main__':
#  host_source = os.path.abspath('.')+'/../spaceship/'
#  print('[*] Collecting the host')
#  host = xenomorph.collect_host(host_source)

#  if (host is not None):
#    activate_queen(host)

