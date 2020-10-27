#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import re
import pathlib

class Replacer():
    def __init__(self, fpath="../", tpath="./", ftype=""):
        self.fpath = fpath
        self.tpath = tpath
        self.ftype = ftype

    def _pattern(self):
        if re.match("(^\.)", self.ftype):
            self.ftype = self.ftype[1:]
        self.pattern_ = ""
        for i in self.ftype:
            self.pattern_ += f"[{i.lower()}"+f"{i.upper()}]"
        self.pattern_ = f"(.+{self.pattern_})$"
        return self.pattern_

    def searchfiles(self):
        self.directories = []
        self.files = []
        self.pattern_ = self._pattern()  ###
        for i,j,k in os.walk(self.fpath):
            for l in k:
                if re.match(self.pattern_, l):
                    self.files.append(l)
                    self.directories.append(os.path.abspath(i))
        return self.directories,self.files


rp = Replacer()
print(rp._pattern())
a, b = rp.searchfiles()
# print(a)
print(b)