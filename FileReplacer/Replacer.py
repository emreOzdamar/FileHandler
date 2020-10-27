#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import re
import pathlib



class Autoplacer():

    def __init__(self):
        self.Error1 = "###  Bad entry, please try again  ####"
        self.fromPath = ""
        self.toPath = ""
        self.filetype = ""


    def askPath(self, opt="from"):
        
        if ((opt !="from") and (opt != "to")):
            print("Bad arg. for 'askPath func.'/('from' or 'to')")
        
        while True:
            entry = input("Enter Directory To Look For(q to quit) : ")
            if os.path.exists(entry):
                if opt == "from":
                    self.fromPath = entry
                    return self.fromPath
                    break
                elif opt =="to":
                    self.toPath = entry
                    return self.toPath
                    break
            elif entry == "q":
                sys.exit("Bye")
            else:
                print(self.Error1)
        
    
    def askFileType (self):

        self.filetype = input("Please enter extension of files you want to look for : ")
        if re.match("(^\.)", self.filetype):
            self.filetype = self.filetype[1:]
        return self.filetype


    def pattern(self):
        self.pattern_ = ""
        for i in self.filetype:
            self.pattern_ += f"[{i.lower()}"+f"{i.upper()}]"
        self.pattern_ = f"(.+{self.pattern_})$"
        return self.pattern_

    def walkMatch(self):
        self.directories = []
        self.files = []
        self.pattern_ = self.pattern()  ###
        for i,j,k in os.walk(self.fromPath):
            for l in k:
                if re.match(self.pattern_, l):
                    self.files.append(l)
                    self.directories.append(os.path.abspath(i))
        return [self.directories,self.files]

    def crToPath(self):
        q1 = "###Where do you want to move the files\n"
        q2 = "(1) - "+"Create a directory by default(in search area).\n"
        q3 = "(2) - "+"Enter an existing directory\n### Option : "
        question_ = input(q1+q2+q3)

        if question_ == "1":
            if (re.match(".+[/\\\]$", self.fromPath)):
                self.fromPath=self.fromPath[:-1]
            self.toPath = self.fromPath+"/"+self.filetype+"Files"
            a = 1
            while os.path.exists(self.toPath):
                self.toPath = self.fromPath+"/"+self.filetype+"Files"+str(a)
                a+=1
            os.mkdir(self.toPath)
            print("Created "+ self.toPath)
            return self.toPath

        elif question_ == "2":
            self.askPath("to")  ###
            print("Directory : "+ self.toPath)
        else:
            print(self.Error1)
            self.crToPath()

    def mvFiles(self):

        self.toPath_ = self.toPath
        if (re.match(".+[/\\\]$", self.toPath_)):
            self.toPath_ = self.toPath_[:-1]

        print("Searching Files....")
        directs, files = self.walkMatch()
        files2 = files[:]

        for i in files2:
            a = 1
            while files2.count(i) >= 2:
                files2[files2.index(i)] = i[:(-len(self.filetype))] + str(a) + self.filetype
                a += 1

        print("Moving Files...")
        for i in range(len(files)):
            path_ = directs[i]+"/"+files[i]
            toPath_2 =self.toPath_ + "/" + files2[i]
            print(path_ +"------> " + toPath_2)
            pathlib.Path(path_).rename(toPath_2)
        
        print(f"Files found and replaced : {len(files)}")
        return len(files)

    def start(self):
        self.askPath()
        self.askFileType()
        self.crToPath()
        self.mvFiles()



if __name__ == "__main__":
    rp = Autoplacer()
    rp.start()

