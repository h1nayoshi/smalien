# -*- coding: utf-8 -*-
# Called by queen.py

import os
import re
import shutil
import subprocess

def collect_host(host_source):
  hosts = []

  paths = os.listdir(host_source)

  for path in paths:
    check = re.search(r'^\..*', path)
    if (check is None):
      return host_source+path
  return None

def init_hive(host, host_dest):
  # Clean hive
  try:
    os.remove(host_dest+'host.apk')
  except:
    pass
  try:
    os.remove(host_dest+'implanted.apk')
  except:
    pass
  try:
    shutil.rmtree(host_dest+'host')
  except:
    pass

  # Move new host to hive
  try:
    subprocess.check_call('cp '+host+' '+host_dest+'host.apk', shell=True)
  except:
    return False
  return True

