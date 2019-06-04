# -*- coding: utf-8 -*-
# Called by dalvikbytecodeparser.py

container_methods = [
  # Group 0: SharedPreference
  {'code': 'Landroid/content/SharedPreferences$Editor;->put', 'group': 0, 'class': 0},
  {'code': 'Landroid/content/SharedPreferences;->get', 'group': 0, 'class': 1},
  # Group 1: Bundle, Intent
  {'code': 'Landroid/os/Bundle;->put', 'group': 1, 'class': 0},
  {'code': 'Landroid/content/Intent;->put', 'group': 1, 'class': 0},
  {'code': 'Landroid/os/Bundle;->get', 'group': 1, 'class': 1},
  {'code': 'Landroid/content/Intent;->get', 'group': 1, 'class': 1},
  # Group 2: JsonObject
  {'code': 'Lorg/json/JSONObject;->put', 'group': 2, 'class': 0},
  {'code': 'Lorg/json/JSONObject;->get', 'group': 2, 'class': 1},
]
