#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fasttest_selenium.common import Var

def driver():
    return Var.instance
driver = driver()
