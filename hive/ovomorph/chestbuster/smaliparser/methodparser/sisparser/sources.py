# -*- coding: utf-8 -*-
# Called by sisparser.py

sources = [
  {'code': 'Landroid/telephony/TelephonyManager;->getDeviceId()Ljava/lang/String;', 'type': 'Ljava/lang/String;', 'data': 'IMEI'},
  {'code': 'Landroid/telephony/TelephonyManager;->getSimSerialNumber()Ljava/lang/String;', 'type': 'Ljava/lang/String;', 'data': 'ICCID'},
  {'code': 'Landroid/telephony/TelephonyManager;->getSubscriberId()Ljava/lang/String;', 'type': 'Ljava/lang/String;', 'data': 'IMSI'},
  {'code': 'Landroid/telephony/TelephonyManager;->getLine1Number()Ljava/lang/String;', 'type': 'Ljava/lang/String;', 'data': 'Phone Number'},
  {'code': 'Landroid/telephony/TelephonyManager;->getNetworkOperator()Ljava/lang/String;', 'type': 'Ljava/lang/String;', 'data': 'MCC+MNC'},
  {'code': 'Landroid/location/Location;->getLatitude()D', 'type': 'D', 'data': 'GPS'},
  {'code': 'Landroid/location/Location;->getLongitude()D', 'type': 'D', 'data': 'GPS'},
  {'code': 'Landroid/telephony/SmsMessage;->getDisplayOriginatingAddress()Ljava/lang/String;', 'type': 'Ljava/lang/String;', 'data': 'SMS'},
  {'code': 'Landroid/telephony/SmsMessage;->getOriginatingAddress()Ljava/lang/String;', 'type': 'Ljava/lang/String;', 'data': 'SMS'},
  {'code': 'Landroid/telephony/SmsMessage;->getEmailFrom()Ljava/lang/String;', 'type': 'Ljava/lang/String;', 'data': 'SMS'},
  {'code': 'Landroid/telephony/SmsMessage;->getDisplayMessageBody()Ljava/lang/String;', 'type': 'Ljava/lang/String;', 'data': 'SMS'},
  {'code': 'Landroid/telephony/SmsMessage;->getMessageBody()Ljava/lang/String;', 'type': 'Ljava/lang/String;', 'data': 'SMS'},
  {'code': 'Landroid/telephony/SmsMessage;->getEmailBody()Ljava/lang/String;', 'type': 'Ljava/lang/String;', 'data': 'SMS'},
]

