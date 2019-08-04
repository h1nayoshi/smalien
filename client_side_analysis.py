# -*- coding: utf-8 -*-

import sys
from hive.queen import install, logging

if (len(sys.argv) < 2):
  print('python3 client_side_analysis.py target')
  sys.exit()

print('[*] Starting client-side analysis')

target_apk = sys.argv[1]

# Installing
install(target_apk)
# Logging
logging()
