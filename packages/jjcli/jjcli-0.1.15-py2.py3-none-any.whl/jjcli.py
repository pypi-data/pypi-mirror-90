"""
python module for command-line filter

 python3 -m jjcli          ## for manual
 python3 -m jjcli skel     ## for a initial filter skeleton

-- 
 from jjcli import *       ## re.* functions also imported
 c=clfilter(opt="do:")     ## options in c.opt;
                           ##    autostrip         (def=True)
                           ##    inplace           (def=False) 
                           ##    fs (for csvrow()) (def=",")

 for line in c.input():...    ## process one rstriped line at the time
 for txt in c.slurp():...     ## process one striped text at the time
    ## process txt            ##   (end of line spaces and \r also removed)
 for par in c.paragraph():... ## process one striped paragraph at the time
 for tup in c.csvrow():...    ## process one csv row at the time
 for tup in c.tsvrow():...    ## process one tsv row at the time

 c.lineno()                ## line number
 c.filelineno()
 c.parno()                 ## paragraph number
 c.fileparno()
 c.filename()              ## filename or "<stdin>"
 c.nextfile()
 c.isfirstline()

## subprocesses   (qx, qxlines, qxsystem)
 a=qx( "ls" )
 for x in qxlines("find | grep '\.jpg$'"): 
   ...
 qxsystem("vim myfile")

## regular expressions

 imports all functions from re.*

"""

import subprocess 
import re
from re import match, fullmatch, search, sub, subn, split, findall, finditer, compile 
                    ## all re functions are imported!
                    ## and re.I re.S re.X 
import fileinput as F, getopt, sys
import urllib.request as ur, csv

## execute external comands

# execute command return its stdout
def qx(*x)      : return subprocess.getoutput(x)

# execute command return its stdout lines
def qxlines(*x) : return subprocess.getoutput(x).splitlines()

# execute command -- system
def qxsystem(*x): subprocess.call(x,shell=True)

## Command line filters
class clfilter:
   '''csfilter - Class for command line filters'''
   
   def __init__(self,opt="",
                     rs="\n",
                     fs=",",
                     autostrip=True,
                     inplace=False):
       opcs=[]
       
       try:
           opts, args = getopt.getopt(sys.argv[1:],opt)
       except Exception as err:
           print(err)  
           # usage()
           sys.exit(1)
       self.opt=dict(opts)
       self.args=args
       self.rs=rs
       self.fs=fs
       self.autostrip=autostrip
       self.inplace=inplace
 
   def input(self,files=None): 
       files = files or self.args
       if self.autostrip:
           return map(str.rstrip,F.input(files=files,inplace=self.inplace))
# return map(lambda x:str(x).rstrip(),F.input(files=files,inplace=self.inplace))
       else:
           return F.input(files=files,inplace=self.inplace)

   def csvrow(self,files=None):
       files = files or self.args
       return csv.reader(F.input(files=files),
                         skipinitialspace=True, delimiter=self.fs)

   def tsvrow(self,files=None):
       files = files or self.args
       return csv.reader(F.input(files=files),
                         skipinitialspace=True, delimiter="\t")

   def paragraph(self,files=None):
       files = files or self.args or [None]
       self.parno_=0
       for f in files:
           t=""
           state=None
           self.fileparno_=0
           fs = [] if f == None else [f]
           for l in F.input(files=fs,inplace=self.inplace):
               if search(r'\S', l) and state == "inside delim":
                   self.parno_+= 1
                   self.fileparno_+= 1
                   if self.autostrip:
                       yield self.cleanpar(t)
                   else:
                       yield t
                   state ="inside par"
                   t=l
               elif search(r'\S', l) and state != "inside delim":
                   t += l
                   state ="inside par"
               else:
                   state ="inside delim"
                   t += l
           if search(r'\S',t):             ## last paragraph
               self.parno_+= 1
               self.fileparno_+= 1
               if self.autostrip:
                   yield self.cleanpar(t)
               else:
                   yield t

   def off_slurp(self,files=None):
       files = files or self.args or [None]
       for f in files:
           t=""
           fs = [] if f == None else [f]
           for l in F.input(files=fs,inplace=self.inplace):
               t += l
           if self.autostrip:
               yield self.clean(t)
           else:
               yield t

   def slurp(self,files=None):
       files = files or self.args or [None]
       for f in files:
           t=""
           if f == None: fs=[]
           elif match(r'(https?|ftp)://',f):
               yield ur.urlopen(f).read().decode('utf-8')
               continue
           else: fs = [f]

           for l in F.input(files=fs,inplace=self.inplace):
               t += l
           if self.autostrip:
               yield self.clean(t)
           else:
               yield t

   def slurpurlutf8(self,f):
       t= ur.urlopen(f).read()
       try:  
           a = t.decode('utf-8')
           return a
       except Exception as e1:
           try:  
               a = t.decode('iso8859-1')
               return a
           except Exception as e:
               return t

   def clean(self,s):              # clean: normalise end-of-line spaces and termination
       return sub(r'[ \r\t]*\n','\n',s)

   def cleanpar(self,s):           # clean: normalise end-of-line spaces and termination
       return sub(r'\s+$','\n' ,sub(r'[ \r\t]*\n','\n',s))

   filename    = lambda s : F.filename()      # inherited from fileinput
   filelineno  = lambda s : F.filelineno()
   lineno      = lambda s : F.lineno()
   fileparno   = lambda s : s.fileparno_
   parno       = lambda s : s.parno_
   nextfile    = lambda s : F.nextfile()
   isfirstline = lambda s : F.isfirstline()
   close       = lambda s : F.close()

#   filename    = F.filename()      # não funciona assim...

__version__ = "0.1.15"

def main():
   if   len(sys.argv)==1: 
      print("Name\n jjcli - ",__doc__.lstrip())
   elif sys.argv[1] == "skel":
      print(
"""#!/usr/bin/python3
from jjcli import * 
c=clfilter(opt="do:")     ## option values in c.opt dictionary

for line in c.input():    ## process one line at the time
    ## process line

#for txt in c.slurp(): ...    ## process one file at the time
#for par in c.paragraph():... ## process one paragraph at the time
#for txt in c.cvsrow(): ...   ## process one csv row at the time
#for txt in c.tvsrow(): ...   ## process one tsv row at the time
""")

if __name__ == "__main__": main()
