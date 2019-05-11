# -*- coding: utf-8 -*-
# Called by sisparser.py

sinks = [
  #{'code': ' Landroid/widget/TextView;->setText(Ljava/lang/CharSequence;)V', 'svars': [1], 'type': 'Ljava/lang/String;'},
  #{'code': ' Landroid/util/Log;->i(Ljava/lang/String;Ljava/lang/String;)I', 'svars': [0, 1], 'type': 'Ljava/lang/String;'},
  # Apache
  {'code': ' Lorg/apache/http/impl/client/DefaultHttpClient;->execute(Lorg/apache/http/client/methods/HttpUriRequest;)Lorg/apache/http/HttpResponse;', 'svars': [1], 'type': 'Lorg/apache/http/client/methods/HttpUriRequest;'},
  {'code': ' Lorg/apache/http/client/HttpClient;->execute(Lorg/apache/http/client/methods/HttpUriRequest;)Lorg/apache/http/HttpResponse;', 'svars': [1], 'type': 'Lorg/apache/http/client/methods/HttpUriRequest;'},
  # OutputStream
  {'code': ' Ljava/io/OutputStream;->write([B)V', 'svars':[1], 'type': '[B'},
  {'code': ' Ljava/io/OutputStream;->write([BII)V', 'svars':[1], 'type': '[B'},
  {'code': ' Ljava/io/OutputStream;->write(I)V', 'svars':[1], 'type': 'I'},
  # FileOutputStream
  {'code': ' Ljava/io/FileOutputStream;->write([B)V', 'svars':[1], 'type': '[B'},
  {'code': ' Ljava/io/FileOutputStream;->write([BII)V', 'svars':[1], 'type': '[B'},
  {'code': ' Ljava/io/FileOutputStream;->write(I)V', 'svars':[1], 'type': 'I'},
  # Writer
  {'code': ' Ljava/io/Writer;->append(C)V', 'svars':[1], 'type': 'C'},
  {'code': ' Ljava/io/Writer;->append(java/lang/CharSequence;)V', 'svars':[1], 'type': 'java/lang/CharSequence;'},
  {'code': ' Ljava/io/Writer;->append(java/lang/CharSequence;II)V', 'svars':[1], 'type': 'java/lang/CharSequence;'},
  {'code': ' Ljava/io/Writer;->write(Ljava/lang/String;)V', 'svars':[1], 'type': 'Ljava/lang/String;'},
  {'code': ' Ljava/io/Writer;->write(Ljava/lang/String;II)V', 'svars':[1], 'type': 'Ljava/lang/String;'},
  {'code': ' Ljava/io/Writer;->write(C)V', 'svars':[1], 'type': 'C'},
  {'code': ' Ljava/io/Writer;->write([C)V', 'svars':[1], 'type': '[C'},
  {'code': ' Ljava/io/Writer;->write([CII)V', 'svars':[1], 'type': '[C'},
]
