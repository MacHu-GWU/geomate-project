#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from docfly import Docfly
import shutil
 
try:
    shutil.rmtree(r"source\geomate")
except Exception as e:
    print(e)
     
docfly = Docfly("geomate", dst="source", 
    ignore=[
        "geomate.zzz_manual_install.py",
        "geomate.tests",
    ]
)
docfly.fly()
