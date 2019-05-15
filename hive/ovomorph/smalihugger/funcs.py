# -*- coding: utf-8 -*-
# Called by smalihugger.py

import os
import re
import io
import subprocess

def unpack(host_dest):
  try:
    subprocess.check_call('apktool d '+host_dest+'host.apk -o '+host_dest+'host > /dev/null 2>&1', shell=True)
  except:
    return False
  return True

def find_smalis(host_dest):
  smali_dir = host_dest+'host/smali/'
  #smali_dir = host_dest+'host/smali/com/'
  # Find smalis
  smalis = []
  find_smalis_from_dir(smali_dir, smalis)
  if (smalis == []):
    return False
  return smalis

def find_smalis_from_dir(smali_dir, smalis):
  paths = os.listdir(smali_dir)
  for path in paths:
    check1 = re.search(r'^R[\$\.].*', path)
    check2 = re.search(r'^\..*', path)
    check3 = re.search(r'BuildConfig.smali', path)
    check4 = re.search(r'.smali$', path)
    if ((check1 is None) and (check2 is None) and (check3 is None) and (check4 is not None)):
      smalis.append(smali_dir+path)
    elif (check4 is None):
      new_dir = path.split('/')[-1]
      find_smalis_from_dir(smali_dir+new_dir+'/', smalis)

def find_activities(hd):
  activities = []
  with io.open(hd+'host/AndroidManifest.xml', 'r', encoding='utf-8') as f:
    AM = f.read().split('\n')
  for l in AM:
    if (l.find('<manifest ') > -1 and l.find(' package="') > -1):
      pkg_name = l.split(' package="')[-1].split('"')[0]
    elif (l.find('<activity ') > -1 and l.find(' android:name="') > -1):
      activity = l.split(' android:name="')[-1].split('"')[0]
      if (activity[0] == '.'):
        activity = pkg_name + activity
      elif (activity.find('.') < 0):
        activity = pkg_name + '.' + activity
      activities.append('L'+activity.replace('.', '/')+';')
  return activities

def detach(host_dest, keystore):
  # Pack
  #print('  [--Z--] Packing')
  ret = pack(host_dest)
  if (not ret):
    print('[--!--] Failed to pack')
    return False

  # Sign
  #print('  [--Z--] Signing')
  ret = sign(host_dest, keystore)
  if (not ret):
    print('[--!--] Failed to sign')
    return False

  # Move
  #print('  [--Z--] Moving')
  ret = move(host_dest)
  if (not ret):
    print('[--!--] Failed to move')
    return False

  return True

def pack(host_dest):
  try:
    subprocess.check_call('apktool b '+host_dest+'host/ > /dev/null 2>&1', shell=True)
  except:
    return False
  return True

def sign(host_dest, keystore):
  try:
    subprocess.check_call('jarsigner -verbose -keystore '+keystore[0]+' -storepass '+keystore[1]+' '+host_dest+'host/dist/host.apk '+keystore[2]+' > /dev/null 2>&1', shell=True)
  except:
    return False
  return True

def move(host_dest):
  try:
    subprocess.check_call('mv '+host_dest+'host/dist/host.apk '+host_dest+'implanted.apk', shell=True)
  except:
    return False
  return True

