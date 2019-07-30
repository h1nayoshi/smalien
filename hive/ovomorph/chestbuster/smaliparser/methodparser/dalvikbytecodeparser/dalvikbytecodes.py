# -*- coding: utf-8 -*-
# Called by dalvikbytecodeparser.py
# Return operations are written in methodparser.py

dalvik_byte_codes = [
  # Group 0: opcode x1, x4, ..., xn
  #   Class 0: opcode dest, lit
  {'code': '    const ', 'group': 0, 'class': 0, 'type': 'const'},
  {'code': '    const/4 ', 'group': 0, 'class': 0, 'type': 'const'},
  {'code': '    const/16 ', 'group': 0, 'class': 0, 'type': 'const'},
  {'code': '    const/high16 ', 'group': 0, 'class': 0, 'type': 'const'},
  {'code': '    const-wide ', 'group': 0, 'class': 0, 'type': 'const'},
  {'code': '    const-wide/16 ', 'group': 0, 'class': 0, 'type': 'const'},
  {'code': '    const-wide/32 ', 'group': 0, 'class': 0, 'type': 'const'},
  {'code': '    const-wide/high16 ', 'group': 0, 'class': 0, 'type': 'const'},

  {'code': '    const-string ', 'group': 0, 'class': 0, 'type': 'Ljava/lang/String;'},
  {'code': '    const-string/jumbo ', 'group': 0, 'class': 0, 'type': 'Ljava/lang/String;'},
  {'code': '    const-method-handle ', 'group': 0, 'class': 0, 'type': 'unknown'},
  {'code': '    const-method-type ', 'group': 0, 'class': 0, 'type': 'unknown'},
  {'code': '    fill-array-data ', 'group': 0, 'class': 0, 'type': 'unknown'},
  {'code': '    move-exception ', 'group': 0, 'class': 0, 'type': 'unknown'},
  {'code': '    cmpl-float ', 'group': 0, 'class': 0, 'type': 'Z'},
  {'code': '    cmpg-float ', 'group': 0, 'class': 0, 'type': 'Z'},
  {'code': '    cmpl-double ', 'group': 0, 'class': 0, 'type': 'Z'},
  {'code': '    cmpg-double ', 'group': 0, 'class': 0, 'type': 'Z'},
  {'code': '    cmp-long ', 'group': 0, 'class': 0, 'type': 'Z'},
  #   Class 1: opcode dest, (x), type
  {'code': '    new-array ', 'group': 0, 'class': 1, 'dtype': 'oprnd'},
  {'code': '    array-length ', 'group': 0, 'class': 1, 'dtype': 'I'},
  {'code': '    const-class ', 'group': 0, 'class': 1, 'dtype': 'uninitialized'},
  {'code': '    instance-of ', 'group': 0, 'class': 1, 'dtype': 'Z'},
  #{'code': '    new-instance ', 'group': 0, 'class': 1, 'dtype': 'oprnd'},
  {'code': '    new-instance ', 'group': 0, 'class': 1, 'dtype': 'uninitialized'},
  #   Class 2: opcode dest, src, (x)
  {'code': '    move ', 'group': 0, 'class': 2, 'dtype': 'stype'},
  {'code': '    move/16 ', 'group': 0, 'class': 2, 'dtype': 'stype'},
  {'code': '    move/from16 ', 'group': 0, 'class': 2, 'dtype': 'stype'},
  {'code': '    move-wide ', 'group': 0, 'class': 2, 'dtype': 'stype'},
  {'code': '    move-wide/16 ', 'group': 0, 'class': 2, 'dtype': 'stype'},
  {'code': '    move-wide/from16 ', 'group': 0, 'class': 2, 'dtype': 'stype'},
  {'code': '    move-object ', 'group': 0, 'class': 2, 'dtype': 'unknown'}, # Currently compromised with unknown type
  {'code': '    move-object/16 ', 'group': 0, 'class': 2, 'dtype': 'stype'},
  {'code': '    move-object/from16 ', 'group': 0, 'class': 2, 'dtype': 'stype'},

  {'code': '    add-int/lit16 ', 'group': 0, 'class': 2, 'dtype': 'stype'},
  {'code': '    rsub-int/lit16 ', 'group': 0, 'class': 2, 'dtype': 'stype'},
  {'code': '    mul-int/lit16 ', 'group': 0, 'class': 2, 'dtype': 'stype'},
  {'code': '    div-int/lit16 ', 'group': 0, 'class': 2, 'dtype': 'stype'},
  {'code': '    rem-int/lit16 ', 'group': 0, 'class': 2, 'dtype': 'stype'},
  {'code': '    and-int/lit16 ', 'group': 0, 'class': 2, 'dtype': 'stype'},
  {'code': '    or-int/lit16 ', 'group': 0, 'class': 2, 'dtype': 'stype'},
  {'code': '    xor-int/lit16 ', 'group': 0, 'class': 2, 'dtype': 'stype'},

  {'code': '    add-int/lit8 ', 'group': 0, 'class': 2, 'dtype': 'stype'},
  {'code': '    rsub-int/lit8 ', 'group': 0, 'class': 2, 'dtype': 'stype'},
  {'code': '    mul-int/lit8 ', 'group': 0, 'class': 2, 'dtype': 'stype'},
  {'code': '    div-int/lit8 ', 'group': 0, 'class': 2, 'dtype': 'stype'},
  {'code': '    rem-int/lit8 ', 'group': 0, 'class': 2, 'dtype': 'stype'},
  {'code': '    and-int/lit8 ', 'group': 0, 'class': 2, 'dtype': 'stype'},
  {'code': '    or-int/lit8 ', 'group': 0, 'class': 2, 'dtype': 'stype'},
  {'code': '    xor-int/lit8 ', 'group': 0, 'class': 2, 'dtype': 'stype'},
  {'code': '    shl-int/lit8 ', 'group': 0, 'class': 2, 'dtype': 'stype'},
  {'code': '    shr-int/lit8 ', 'group': 0, 'class': 2, 'dtype': 'stype'},
  {'code': '    ushr-int/lit8 ', 'group': 0, 'class': 2, 'dtype': 'stype'},

  {'code': '    int-to-byte ', 'group': 0, 'class': 2, 'dtype': 'B'},
  {'code': '    int-to-short ', 'group': 0, 'class': 2, 'dtype': 'S'},
  {'code': '    int-to-char ', 'group': 0, 'class': 2, 'dtype': 'C'},
  {'code': '    int-to-long ', 'group': 0, 'class': 2, 'dtype': 'J'},
  {'code': '    int-to-float ', 'group': 0, 'class': 2, 'dtype': 'F'},
  {'code': '    int-to-double ', 'group': 0, 'class': 2, 'dtype': 'D'},

  {'code': '    long-to-int ', 'group': 0, 'class': 2, 'dtype': 'I'},
  {'code': '    long-to-float ', 'group': 0, 'class': 2, 'dtype': 'F'},
  {'code': '    long-to-double ', 'group': 0, 'class': 2, 'dtype': 'D'},

  {'code': '    float-to-int ', 'group': 0, 'class': 2, 'dtype': 'I'},
  {'code': '    float-to-long ', 'group': 0, 'class': 2, 'dtype': 'J'},
  {'code': '    float-to-double ', 'group': 0, 'class': 2, 'dtype': 'D'},

  {'code': '    double-to-int ', 'group': 0, 'class': 2, 'dtype': 'I'},
  {'code': '    double-to-long ', 'group': 0, 'class': 2, 'dtype': 'J'},
  {'code': '    double-to-float ', 'group': 0, 'class': 2, 'dtype': 'F'},

  {'code': '    sget ', 'group': 0, 'class': 2, 'dtype': 'stype'}, # for static
  {'code': '    sget-byte ', 'group': 0, 'class': 2, 'dtype': 'stype'}, # for static
  {'code': '    sget-short ', 'group': 0, 'class': 2, 'dtype': 'stype'}, # for static
  {'code': '    sget-char ', 'group': 0, 'class': 2, 'dtype': 'stype'}, # for static
  {'code': '    sget-boolean ', 'group': 0, 'class': 2, 'dtype': 'stype'}, # for static
  {'code': '    sget-wide ', 'group': 0, 'class': 2, 'dtype': 'stype'}, # for static
  {'code': '    sget-object ', 'group': 0, 'class': 2, 'dtype': 'stype'}, # for static

  {'code': '    iget ', 'group': 0, 'class': 2, 'dtype': 'I'},
  {'code': '    iget-byte ', 'group': 0, 'class': 2, 'dtype': 'B'},
  {'code': '    iget-short ', 'group': 0, 'class': 2, 'dtype': 'S'},
  {'code': '    iget-char ', 'group': 0, 'class': 2, 'dtype': 'C'},
  {'code': '    iget-boolean ', 'group': 0, 'class': 2, 'dtype': 'Z'},
  {'code': '    iget-wide ', 'group': 0, 'class': 2, 'dtype': 'stype'},
  {'code': '    iget-object ', 'group': 0, 'class': 2, 'dtype': 'stype'},

  {'code': '    aget ', 'group': 0, 'class': 2, 'dtype': 'I'},
  {'code': '    aget-byte ', 'group': 0, 'class': 2, 'dtype': 'B'},
  {'code': '    aget-short ', 'group': 0, 'class': 2, 'dtype': 'S'},
  {'code': '    aget-char ', 'group': 0, 'class': 2, 'dtype': 'C'},
  {'code': '    aget-boolean ', 'group': 0, 'class': 2, 'dtype': 'Z'},
  {'code': '    aget-wide ', 'group': 0, 'class': 2, 'dtype': 'src_elem'},
  {'code': '    aget-object ', 'group': 0, 'class': 2, 'dtype': 'src_elem'},

  {'code': '    neg-int ', 'group': 0, 'class': 2, 'dtype': 'stype'},
  {'code': '    not-int ', 'group': 0, 'class': 2, 'dtype': 'stype'},
  {'code': '    neg-long ', 'group': 0, 'class': 2, 'dtype': 'stype'},
  {'code': '    not-long ', 'group': 0, 'class': 2, 'dtype': 'stype'},
  {'code': '    neg-float ', 'group': 0, 'class': 2, 'dtype': 'stype'},
  {'code': '    neg-double ', 'group': 0, 'class': 2, 'dtype': 'stype'},
  #   Class 3: opcode dest_src, src
  {'code': '    add-int/2addr ', 'group': 0, 'class': 3, 'type': 'I'},
  {'code': '    sub-int/2addr ', 'group': 0, 'class': 3, 'type': 'I'},
  {'code': '    mul-int/2addr ', 'group': 0, 'class': 3, 'type': 'I'},
  {'code': '    div-int/2addr ', 'group': 0, 'class': 3, 'type': 'I'},
  {'code': '    rem-int/2addr ', 'group': 0, 'class': 3, 'type': 'I'},
  {'code': '    and-int/2addr ', 'group': 0, 'class': 3, 'type': 'I'},
  {'code': '    or-int/2addr ', 'group': 0, 'class': 3, 'type': 'I'},
  {'code': '    xor-int/2addr ', 'group': 0, 'class': 3, 'type': 'I'},
  {'code': '    shl-int/2addr ', 'group': 0, 'class': 3, 'type': 'I'},
  {'code': '    shr-int/2addr ', 'group': 0, 'class': 3, 'type': 'I'},
  {'code': '    ushr-int/2addr ', 'group': 0, 'class': 3, 'type': 'I'},

  {'code': '    add-long/2addr ', 'group': 0, 'class': 3, 'type': 'J'},
  {'code': '    sub-long/2addr ', 'group': 0, 'class': 3, 'type': 'J'},
  {'code': '    mul-long/2addr ', 'group': 0, 'class': 3, 'type': 'J'},
  {'code': '    div-long/2addr ', 'group': 0, 'class': 3, 'type': 'J'},
  {'code': '    rem-long/2addr ', 'group': 0, 'class': 3, 'type': 'J'},
  {'code': '    and-long/2addr ', 'group': 0, 'class': 3, 'type': 'J'},
  {'code': '    or-long/2addr ', 'group': 0, 'class': 3, 'type': 'J'},
  {'code': '    xor-long/2addr ', 'group': 0, 'class': 3, 'type': 'J'},
  {'code': '    shl-long/2addr ', 'group': 0, 'class': 3, 'type': 'J'},
  {'code': '    shr-long/2addr ', 'group': 0, 'class': 3, 'type': 'J'},
  {'code': '    ushr-long/2addr ', 'group': 0, 'class': 3, 'type': 'J'},

  {'code': '    add-float/2addr ', 'group': 0, 'class': 3, 'type': 'F'},
  {'code': '    sub-float/2addr ', 'group': 0, 'class': 3, 'type': 'F'},
  {'code': '    mul-float/2addr ', 'group': 0, 'class': 3, 'type': 'F'},
  {'code': '    div-float/2addr ', 'group': 0, 'class': 3, 'type': 'F'},
  {'code': '    rem-float/2addr ', 'group': 0, 'class': 3, 'type': 'F'},

  {'code': '    add-double/2addr ', 'group': 0, 'class': 3, 'type': 'D'},
  {'code': '    sub-double/2addr ', 'group': 0, 'class': 3, 'type': 'D'},
  {'code': '    mul-double/2addr ', 'group': 0, 'class': 3, 'type': 'D'},
  {'code': '    div-double/2addr ', 'group': 0, 'class': 3, 'type': 'D'},
  {'code': '    rem-double/2addr ', 'group': 0, 'class': 3, 'type': 'D'},

  #   Class 4: opcode dest, src, src
  {'code': '    add-int ', 'group': 0, 'class': 4},
  {'code': '    sub-int ', 'group': 0, 'class': 4},
  {'code': '    mul-int ', 'group': 0, 'class': 4},
  {'code': '    div-int ', 'group': 0, 'class': 4},
  {'code': '    rem-int ', 'group': 0, 'class': 4},
  {'code': '    and-int ', 'group': 0, 'class': 4},
  {'code': '    or-int ', 'group': 0, 'class': 4},
  {'code': '    xor-int ', 'group': 0, 'class': 4},
  {'code': '    shl-int ', 'group': 0, 'class': 4},
  {'code': '    shr-int ', 'group': 0, 'class': 4},
  {'code': '    ushr-int ', 'group': 0, 'class': 4},

  {'code': '    add-long ', 'group': 0, 'class': 4},
  {'code': '    sub-long ', 'group': 0, 'class': 4},
  {'code': '    mul-long ', 'group': 0, 'class': 4},
  {'code': '    div-long ', 'group': 0, 'class': 4},
  {'code': '    rem-long ', 'group': 0, 'class': 4},
  {'code': '    and-long ', 'group': 0, 'class': 4},
  {'code': '    or-long ', 'group': 0, 'class': 4},
  {'code': '    xor-long ', 'group': 0, 'class': 4},
  {'code': '    shl-long ', 'group': 0, 'class': 4},
  {'code': '    shr-long ', 'group': 0, 'class': 4},
  {'code': '    ushr-long ', 'group': 0, 'class': 4},

  {'code': '    add-float ', 'group': 0, 'class': 4},
  {'code': '    sub-float ', 'group': 0, 'class': 4},
  {'code': '    mul-float ', 'group': 0, 'class': 4},
  {'code': '    div-float ', 'group': 0, 'class': 4},
  {'code': '    rem-float ', 'group': 0, 'class': 4},

  {'code': '    add-double ', 'group': 0, 'class': 4},
  {'code': '    sub-double ', 'group': 0, 'class': 4},
  {'code': '    mul-double ', 'group': 0, 'class': 4},
  {'code': '    div-double ', 'group': 0, 'class': 4},
  {'code': '    rem-double ', 'group': 0, 'class': 4},

  #{'code': '    aget ', 'group': 0, 'class': 4, 'dtype': 'I'},
  #{'code': '    aget-byte ', 'group': 0, 'class': 4, 'dtype': 'B'},
  #{'code': '    aget-short ', 'group': 0, 'class': 4, 'dtype': 'S'},
  #{'code': '    aget-char ', 'group': 0, 'class': 4, 'dtype': 'C'},
  #{'code': '    aget-boolean ', 'group': 0, 'class': 4, 'dtype': 'Z'},
  #{'code': '    aget-wide ', 'group': 0, 'class': 4, 'dtype': 'src_elem'},
  #{'code': '    aget-object ', 'group': 0, 'class': 4, 'dtype': 'src_elem'},

  #{'code': '    iget ', 'group': 0, 'class': 4, 'dtype': 'I'},
  #{'code': '    iget-byte ', 'group': 0, 'class': 4, 'dtype': 'B'},
  #{'code': '    iget-short ', 'group': 0, 'class': 4, 'dtype': 'S'},
  #{'code': '    iget-char ', 'group': 0, 'class': 4, 'dtype': 'C'},
  #{'code': '    iget-boolean ', 'group': 0, 'class': 4, 'dtype': 'Z'},
  #{'code': '    iget-wide ', 'group': 0, 'class': 4, 'dtype': 'stype'},
  #{'code': '    iget-object ', 'group': 0, 'class': 4, 'dtype': 'unknown'},

  #   Class 5: src, dest
  {'code': '    sput ', 'group': 0, 'class': 5}, # for static
  {'code': '    sput-byte ', 'group': 0, 'class': 5}, # for static
  {'code': '    sput-short ', 'group': 0, 'class': 5}, # for static
  {'code': '    sput-char ', 'group': 0, 'class': 5}, # for static
  {'code': '    sput-boolean ', 'group': 0, 'class': 5}, # for static
  {'code': '    sput-wide ', 'group': 0, 'class': 5}, # for static
  {'code': '    sput-object ', 'group': 0, 'class': 5}, # for static

  {'code': '    iput ', 'group': 0, 'class': 5},
  {'code': '    iput-byte ', 'group': 0, 'class': 5},
  {'code': '    iput-short ', 'group': 0, 'class': 5},
  {'code': '    iput-char ', 'group': 0, 'class': 5},
  {'code': '    iput-boolean ', 'group': 0, 'class': 5},
  {'code': '    iput-wide ', 'group': 0, 'class': 5},
  {'code': '    iput-object ', 'group': 0, 'class': 5},

  #   Class 6: opcode src, src_dest, src
  {'code': '    aput ', 'group': 0, 'class': 6, 'dtype': 'array_dest'},
  {'code': '    aput-byte ', 'group': 0, 'class': 6, 'dtype': 'array_dest'},
  {'code': '    aput-short ', 'group': 0, 'class': 6, 'dtype': 'array_dest'},
  {'code': '    aput-char ', 'group': 0, 'class': 6, 'dtype': 'array_dest'},
  {'code': '    aput-boolean ', 'group': 0, 'class': 6, 'dtype': 'array_dest'},
  {'code': '    aput-wide ', 'group': 0, 'class': 6, 'dtype': 'array_dest'},
  {'code': '    aput-object ', 'group': 0, 'class': 6, 'dtype': 'array_dest'},

  #{'code': '    iput ', 'group': 0, 'class': 6, 'dtype': 'stype'},
  #{'code': '    iput-byte ', 'group': 0, 'class': 6, 'dtype': 'stype'},
  #{'code': '    iput-short ', 'group': 0, 'class': 6, 'dtype': 'stype'},
  #{'code': '    iput-char ', 'group': 0, 'class': 6, 'dtype': 'stype'},
  #{'code': '    iput-boolean ', 'group': 0, 'class': 6, 'dtype': 'stype'},
  #{'code': '    iput-wide ', 'group': 0, 'class': 6, 'dtype': 'stype'},
  #{'code': '    iput-object ', 'group': 0, 'class': 6, 'dtype': 'stype'},

  # Group 1: move result
  {'code': '    move-result ', 'group': 1},
  {'code': '    move-result-wide ', 'group': 1},
  {'code': '    move-result-object ', 'group': 1},
  # Group 2: return
  {'code': '    return ', 'group': 2}, # return
  {'code': '    return-wide ', 'group': 2},
  {'code': '    return-object ', 'group': 2},
  # Group 3: invoke {dest, src, ..., src}, method
  {'code': '    invoke-direct', 'group': 3},
  {'code': '    invoke-virtual', 'group': 3},
  {'code': '    invoke-super', 'group': 3},
  {'code': '    invoke-interface', 'group': 3},

  # Group 4: invoke {src_dest, src_dest, ..., src_dest}, method
  {'code': '    invoke-static', 'group': 4},

  # Group 5: do nothing
  {'code': '    nop ', 'group': 5},
  {'code': '    goto ', 'group': 5},
  {'code': '    goto/16 ', 'group': 5},
  {'code': '    goto/32 ', 'group': 5},
  {'code': '    throw ', 'group': 5},
  {'code': '    monitor-enter ', 'group': 5},
  {'code': '    monitor-exit ', 'group': 5},
  {'code': '    check-cast ', 'group': 5},
]

invoke_kind = {
  0: [
    'invoke-virtual',
    'invoke-super',
    'invoke-direct',
    'invoke-interface',
    'invoke-virtual/range',
    'invoke-super/range',
    'invoke-direct/range',
    'invoke-interface/range',
  ],
  1: [
    'invoke-static',
    'invoke-static/range',
  ],
  2: [
    'invoke-polymorphic',
    'invoke-polymorphic/range',
  ],
  3: [
    'invoke-custom',
    'invoke-custom/range',
  ],
}

