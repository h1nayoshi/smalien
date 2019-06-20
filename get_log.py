# -*- coding: utf-8 -*-

import sys
import subprocess

class GetLog():
  def __init__(self, pkg):
    self.log_output = pkg+'_log.txt'

  def get_log(self):
    self.__clear()

    input('\nRun your application, and hit Enter to finish the analysis.')

    self.__get()
    print('Log has saved successfully in', self.log_output)

  def __clear(self):
    subprocess.check_output('adb logcat -c', shell=True)

  def __get(self):
    result = subprocess.check_output('adb logcat -v raw -d SmalienLog:I *:S', shell=True)
    with open(self.log_output, 'bw') as f:
      f.write(result)

if __name__ == '__main__':
  pkg = sys.argv[1]
  GL = GetLog(pkg)
  GL.get_log()

