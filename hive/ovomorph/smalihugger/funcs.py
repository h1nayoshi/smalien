# -*- coding: utf-8 -*-
# Called by smalihugger.py

import os
import re
import io
import json
import subprocess

from .exclusion import exclusion
from .df_csv_generator import run_csv_generator

def unpack(host_dest):
  try:
    subprocess.check_call('apktool d '+host_dest+'host.apk -o '+host_dest+'host > /dev/null 2>&1', shell=True)
  except:
    return False
  return True

def decon_smalis(host_dest):
  smali_dirs = []
  dirs = os.listdir(host_dest+'host/')
  for d in dirs:
    if (d.find('smali') > -1):
      smali_dirs.append(host_dest+'host/'+d+'/')
  dnum = len(smali_dirs)
  for i in range(dnum):
    dnum += 1
    newdir = host_dest+'host/smali_classes'+str(dnum)+'/'
    os.mkdir(newdir)
    smali_dirs.append(newdir)
    files = os.listdir(smali_dirs[i])
    dirs = []
    for f in files:
      if (os.path.isdir(smali_dirs[i]+f)):
        dirs.append(f)
    for j in range(int(len(dirs)/2)):
      move_dir(smali_dirs[i]+dirs[j], newdir)
  return smali_dirs

def move_dir(target, dest):
  subprocess.check_call('mv '+target+' '+dest, shell=True)

def find_smalis(host_dest, smali_dirs):
  # Find smalis
  smalis = []
  for sdir in smali_dirs:
    # Create exclusion list
    sdir_ex = []
    for ex in exclusion:
      sdir_ex.append(sdir+ex)
    # Find smalis
    find_smalis_from_dir(sdir, smalis, sdir_ex)
  if (smalis == []):
    return False
  new_dex_dir = host_dest+'host/smali_classes'+str(len(smali_dirs)+1)
  return smalis, new_dex_dir

def find_smalis_from_dir(smali_dir, smalis, sdir_ex):
  paths = os.listdir(smali_dir)
  for path in paths:
    if (smali_dir+path in sdir_ex):
      return
    check1 = re.search(r'^R[\$\.].*', path)
    check2 = re.search(r'^\..*', path)
    check3 = re.search(r'BuildConfig.smali', path)
    check4 = re.search(r'.smali$', path)
    if ((check1 is None) and (check2 is None) and (check3 is None) and (check4 is not None)):
      smalis.append(smali_dir+path)
    elif (check4 is None):
      new_dir = path.split('/')[-1]
      find_smalis_from_dir(smali_dir+new_dir+'/', smalis, sdir_ex)

def find_activities(hd):
  activities = []
  with io.open(hd+'host/AndroidManifest.xml', 'r', encoding='utf-8') as f:
    AM = f.read().split('\n')
  for l in AM:
    if (l.find('<manifest ') > -1 and l.find(' package="') > -1):
      pkg = l.split(' package="')[-1].split('"')[0]
    elif (l.find('<activity ') > -1 and l.find(' android:name="') > -1):
      activity = l.split(' android:name="')[-1].split('"')[0]
      if (activity[0] == '.'):
        activity = pkg + activity
      elif (activity.find('.') < 0):
        activity = pkg + '.' + activity
      activities.append('L'+activity.replace('.', '/')+';')
  return pkg, activities

def write_results(pkg, parsed_data, data_flows, log_ids):
  output_to_file(pkg+'_parsed_data.json', parsed_data)
  output_to_file(pkg+'_data_flows.json', data_flows)
  output_to_file(pkg+'_log_ids.json', log_ids)
  # CSV generating
  run_csv_generator(pkg)

def output_to_file(fname, data):
  r = json.dumps(data)
  with open(fname, 'w') as f:
    f.write(r)

def detach(host_dest, keystore, pkg):
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
  ret = move(host_dest, pkg)
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
    subprocess.check_call('jarsigner -verbose -keystore '+keystore[0]+' -storepass '+keystore[1]+' -keypass '+keystore[2]+' '+host_dest+'host/dist/host.apk '+keystore[3]+' > /dev/null 2>&1', shell=True)
  except:
    return False
  return True

def move(host_dest, pkg):
  try:
    subprocess.check_call('mv '+host_dest+'host/dist/host.apk '+host_dest+'implanted_'+pkg+'.apk', shell=True)
  except:
    return False
  return True

