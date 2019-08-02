# -*- coding: utf-8 -*-

import os
import sys
import subprocess

from . import xenomorph
from .ovomorph.smalihugger import smalihugger

def activate_queen(host, keystore, smalien_path, ppe):
  print(' [+] Target host: '+host)
  print('  [*] PPE:', ppe)

  if (smalien_path is not None):
    host_dest = smalien_path+'/hive/workspace/'
  else:
    host_dest = os.path.abspath('.')+'/hive/workspace/'

  ret = xenomorph.init_hive(host, host_dest)
  if (not ret):
    print('[-!-] Failed to init the hive')
    sys.exit()

  ret, pkg, parsed_data, data_flows, log_ids = smalihugger.run(host_dest, keystore, ppe)
  if (not ret):
    print('[-!-] Failed to hatch the egg')

  print(' [*] All server-side analysis done')

  return pkg, parsed_data, data_flows, log_ids, host_dest

def install(pkg, host_dest):
  print(' [*] Installing the application')
  try:
    subprocess.check_call('adb install -r -g '+host_dest+'implanted_'+pkg+'.apk > /dev/null', shell=True)
  except:
    print('[-!-] Failed to install the app')
    sys.exit()
  print('  [+] Done!')

def logging():
  print(' [*] Start logging')
  cmd = 'adb logcat -c'
  subprocess.check_call(cmd, shell=True)
  cmd = 'adb logcat -v raw SmalienLog:I *:S'
  proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

  while True:
    line = proc.stdout.readline()
    if line:
      print(line)
    if not line and proc.poll() is not None:
      print('Finishing the logging')
      break

#if __name__ == '__main__':
#  host_source = os.path.abspath('.')+'/../spaceship/'
#  print('[*] Collecting the host')
#  host = xenomorph.collect_host(host_source)

#  if (host is not None):
#    activate_queen(host)

