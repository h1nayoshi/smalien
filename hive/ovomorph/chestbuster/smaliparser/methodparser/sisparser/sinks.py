# -*- coding: utf-8 -*-
# Called by sisparser.py

sinks = [
  #{'code': 'Landroid/util/Log;->d(Ljava/lang/String;Ljava/lang/String;)I', 'svars': [1], 'type': 'Ljava/lang/String;'},
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
  {'code': ' Ljava/io/Writer;->append(Ljava/lang/CharSequence;)V', 'svars':[1], 'type': 'Ljava/lang/CharSequence;'},
  {'code': ' Ljava/io/Writer;->append(Ljava/lang/CharSequence;II)V', 'svars':[1], 'type': 'Ljava/lang/CharSequence;'},
  {'code': ' Ljava/io/Writer;->write(Ljava/lang/String;)V', 'svars':[1], 'type': 'Ljava/lang/String;'},
  {'code': ' Ljava/io/Writer;->write(Ljava/lang/String;II)V', 'svars':[1], 'type': 'Ljava/lang/String;'},
  {'code': ' Ljava/io/Writer;->write(C)V', 'svars':[1], 'type': 'C'},
  {'code': ' Ljava/io/Writer;->write([C)V', 'svars':[1], 'type': '[C'},
  {'code': ' Ljava/io/Writer;->write([CII)V', 'svars':[1], 'type': '[C'},
  # PrintStream
  {'code': ' Ljava/io/PrintStream;->append(C)Ljava/io/PrintStream;', 'svars':[1], 'type': 'C'},
  {'code': ' Ljava/io/PrintStream;->append(Ljava/lang/CharSequence;II)Ljava/io/PrintStream;', 'svars':[1], 'type': 'Ljava/lang/CharSequence;'},
  {'code': ' Ljava/io/PrintStream;->append(Ljava/lang/CharSequence;)Ljava/io/PrintStream;', 'svars':[1], 'type': 'Ljava/lang/CharSequence;'},
  {'code': ' Ljava/io/PrintStream;->print(I)V', 'svars':[1], 'type': 'I'},
  {'code': ' Ljava/io/PrintStream;->print(D)V', 'svars':[1], 'type': 'D'},
  {'code': ' Ljava/io/PrintStream;->print(Z)V', 'svars':[1], 'type': 'Z'},
  {'code': ' Ljava/io/PrintStream;->print(C)V', 'svars':[1], 'type': 'C'},
  {'code': ' Ljava/io/PrintStream;->print(J)V', 'svars':[1], 'type': 'J'},
  {'code': ' Ljava/io/PrintStream;->print(F)V', 'svars':[1], 'type': 'F'},
  {'code': ' Ljava/io/PrintStream;->print(Ljava/lang/String;)V', 'svars':[1], 'type': 'Ljava/lang/String;'},
  {'code': ' Ljava/io/PrintStream;->print([C)V', 'svars':[1], 'type': '[C'},
  {'code': ' Ljava/io/PrintStream;->println(C)V', 'svars':[1], 'type': 'C'},
  {'code': ' Ljava/io/PrintStream;->println(Z)V', 'svars':[1], 'type': 'Z'},
  {'code': ' Ljava/io/PrintStream;->println(J)V', 'svars':[1], 'type': 'J'},
  {'code': ' Ljava/io/PrintStream;->println(I)V', 'svars':[1], 'type': 'I'},
  {'code': ' Ljava/io/PrintStream;->println(Ljava/lang/String;)V', 'svars':[1], 'type': 'Ljava/lang/String;'},
  {'code': ' Ljava/io/PrintStream;->println([C)V', 'svars':[1], 'type': '[C'},
  {'code': ' Ljava/io/PrintStream;->println(F)V', 'svars':[1], 'type': 'F'},
  {'code': ' Ljava/io/PrintStream;->println(D)V', 'svars':[1], 'type': 'D'},
  {'code': ' Ljava/io/PrintStream;->write([BII)V', 'svars':[1], 'type': '[B'},
  {'code': ' Ljava/io/PrintStream;->write(I)V', 'svars':[1], 'type': 'I'},
  # GZIPStream
  {'code': ' Ljava/util/zip/GZIPOutputStream;->write([BII)V', 'svars': [1], 'type': '[B'},
]
