# -*- coding: utf-8 -*-

import os
import sys

from . import xenomorph
from .ovomorph.smalihugger import smalihugger

host_dest = os.path.abspath('.')+'/hive/workspace/'

def activate_queen(host, keystore):
  print(' [+] Target host: '+host)

  ret = xenomorph.init_hive(host, host_dest)
  if (not ret):
    print('[-!-] Failed to init the hive')
    sys.exit()

  ret, parsed_data, data_flows = smalihugger.run(host_dest, keystore)
  if (not ret):
    print('[-!-] Failed to hatch the egg')

  print(' [*] All analysis done')

  return parsed_data, data_flows

#if __name__ == '__main__':
#  host_source = os.path.abspath('.')+'/../spaceship/'
#  print('[*] Collecting the host')
#  host = xenomorph.collect_host(host_source)

#  if (host is not None):
#    activate_queen(host)

