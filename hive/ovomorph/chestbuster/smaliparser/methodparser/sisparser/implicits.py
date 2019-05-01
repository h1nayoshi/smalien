# -*- coding: utf-8 -*-
# Called by sisparser.py

implicits = [
  # Group 0
  {'code': ' if-eq ', 'group': 0},
  {'code': ' if-ne ', 'group': 0},
  {'code': ' if-lt ', 'group': 0},
  {'code': ' if-le ', 'group': 0},
  {'code': ' if-ge ', 'group': 0},
  {'code': ' if-gt ', 'group': 0},
  {'code': ' if-eqz ', 'group': 0},
  {'code': ' if-nez ', 'group': 0},
  {'code': ' if-ltz ', 'group': 0},
  {'code': ' if-lez ', 'group': 0},
  {'code': ' if-gtz ', 'group': 0},
  {'code': ' if-gez ', 'group': 0},

  # Group 1
  {'code': ' packed-switch ', 'group': 1},
  {'code': ' sparse-switch ', 'group': 1},

  # Group 2
  {'code': ' cmpl-float ', 'group': 2},
  {'code': ' cmpg-float ', 'group': 2},
  {'code': ' cmpl-double ', 'group': 2},
  {'code': ' cmpg-double ', 'group': 2},
  {'code': ' cmp-long ', 'group': 2},

  # Group 3 array
  {'code': ' aget ', 'group': 3},
  {'code': ' aget-byte ', 'group': 3},
  {'code': ' aget-short ', 'group': 3},
  {'code': ' aget-char ', 'group': 3},
  {'code': ' aget-boolean ', 'group': 3},
  {'code': ' aget-wide ', 'group': 3},
  {'code': ' aget-object ', 'group': 3},

  {'code': ' aput ', 'group': 3},
  {'code': ' aput-byte ', 'group': 3},
  {'code': ' aput-short ', 'group': 3},
  {'code': ' aput-char ', 'group': 3},
  {'code': ' aput-boolean ', 'group': 3},
  {'code': ' aput-wide ', 'group': 3},
  {'code': ' aput-object ', 'group': 3},

  # Group 4: {x, imp1, ..}
  {'code': 'openFileInput(Ljava/lang/String;)Ljava/io/FileInputStream;', 'group': 4},
  {'code': 'Ljava/lang/Runtime;->exec([Ljava/lang/String;)Ljava/lang/Process;', 'group': 4},
  {'code': 'Ljava/io/FileOutputStream;->write(I)V', 'group': 4},
  {'code': 'Ljava/io/FileOutputStream;->write([B)V', 'group': 4},
  {'code': 'Ljava/lang/Thread;->sleep(J)V', 'group': 4},
  {'code': 'Landroid/graphics/Bitmap;->setPixel(III)V', 'group': 4},
  {'code': 'Landroid/widget/TextView;->setTextScaleX(F)V', 'group': 4},
  {'code': 'Ljava/nio/ByteBuffer;->putChar(IC)Ljava/nio/ByteBuffer;', 'group': 4},
  {'code': 'Ljava/io/File;->setLastModified(J)Z', 'group': 4},
  #{'code': 'Ljava/lang/String;->contains(Ljava/lang/CharSequence;)Z', 'group': 4},
  #{'code': 'Ljava/lang/String;->contains(Ljava/lang/CharSequence;)Z', 'group': 4},
  #{'code': 'Ljava/lang/String;->equals(Ljava/lang/Object;)Z', 'group': 4},
  #{'code': 'Ljava/lang/String;->startsWith(Ljava/lang/String;)Z', 'group': 4},
  #{'code': 'Ljava/lang/String;->endsWith(Ljava/lang/String;)Z', 'group': 4},
  {'code': 'Landroid/content/ClipData;->addItem(Landroid/content/ClipData$Item;)V', 'group': 4},
]

