# -*- coding: utf-8 -*-
# Called by queen.py

import sys
from pprint import pprint

from ..chestbuster import chestbuster
from .funcs import unpack, decon_smalis, find_smalis, detach, find_activities

def run(host_dest, keystore, ppe):
  print('  [*] Unpacking the apk')

  # Unpack the apk
  ret = unpack(host_dest)
  if (not ret):
    print('[--!--] Failed to unpack')
    sys.exit()

  # Deconcentrate smalis
  smali_dirs = decon_smalis(host_dest)

  # Find target smali files
  print('  [*] Finding targets')
  smalis, new_dex_dir = find_smalis(host_dest, smali_dirs)
  if (not smalis):
    print('[--!--] Failed to find smalis')
    sys.exit()

  # Find activities
  pkg, activities = find_activities(host_dest)
  if (activities == []):
    print('[--!--] Failed to find activities')
    sys.exit()
  print('   [+] Target pkg name: ' + pkg)
  print('   [+] Activities found: ' + str(len(activities)))

  # Analyze and Inject to smali files
  ret, parsed_data, data_flows, log_ids = chestbuster.run(smalis, activities, new_dex_dir, ppe)
  if (not ret):
    sys.exit()

  # Repack and resign the apk
  print('  [*] Repackaging the apk')
  ret = detach(host_dest, keystore, pkg)
  if (not ret):
    sys.exit()

  return True, pkg, parsed_data, data_flows, log_ids

