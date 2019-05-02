# -*- coding: utf-8 -*-

import subprocess

output = 'smalienlog.txt'

def run_logcat(output):
  try:
    result = subprocess.check_output('adb logcat -v raw -d SmalienLog:I *:S', shell=True)
    #print(result)
    #print result
    with open(output, 'bw') as f:
      f.write(result)
  except:
    return False
  return True

if __name__ == '__main__':
  run_logcat(output)

