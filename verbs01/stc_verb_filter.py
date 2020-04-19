#-*- coding:utf-8 -*-
"""stc_verb_filter.py
 
 
"""
from __future__ import print_function
import sys, re,codecs
from parseheadline import parseheadline
#import transcoder
#transcoder.transcoder_set_dir('transcoder')

class Entry(object):
 Ldict = {}
 def __init__(self,lines,linenum1,linenum2):
  # linenum1,2 are int
  self.metaline = lines[0]
  self.lend = lines[-1]  # the <LEND> line
  self.datalines = lines[1:-1]  # the non-meta lines
  # parse the meta line into a dictionary
  #self.meta = Hwmeta(self.metaline)
  self.metad = parseheadline(self.metaline)
  self.linenum1 = linenum1
  self.linenum2 = linenum2
  #L = self.meta.L
  L = self.metad['L']
  if L in self.Ldict:
   print("Entry init error: duplicate L",L,linenum1)
   exit(1)
  self.Ldict[L] = self
  #  extra attributes
  self.marked = False # from a filter of markup associated with verbs
  self.markcode = None
  self.markline = None

def init_entries(filein):
 # slurp lines
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  lines = [line.rstrip('\r\n') for line in f]
 recs=[]  # list of Entry objects
 inentry = False  
 idx1 = None
 idx2 = None
 for idx,line in enumerate(lines):
  if inentry:
   if line.startswith('<LEND>'):
    idx2 = idx
    entrylines = lines[idx1:idx2+1]
    linenum1 = idx1 + 1
    linenum2 = idx2 + 1
    entry = Entry(entrylines,linenum1,linenum2)
    recs.append(entry)
    # prepare for next entry
    idx1 = None
    idx2 = None
    inentry = False
   elif line.startswith('<L>'):  # error
    print('init_entries Error 1. Not expecting <L>')
    print("line # ",idx+1)
    print(line.encode('utf-8'))
    exit(1)
   else: 
    # keep looking for <LEND>
    continue
  else:
   # inentry = False. Looking for '<L>'
   if line.startswith('<L>'):
    idx1 = idx
    inentry = True
   elif line.startswith('<LEND>'): # error
    print('init_entries Error 2. Not expecting <LEND>')
    print("line # ",idx+1)
    print(line.encode('utf-8'))
    exit(1)
   else: 
    # keep looking for <L>
    continue
 # when all lines are read, we should have inentry = False
 if inentry:
  print('init_entries Error 3. Last entry not closed')
  print('Open entry starts at line',idx1+1)
  exit(1)

 print(len(lines),"lines read from",filein)
 print(len(recs),"entries found")
 return recs

def get_capital_pattern():
 accented_capital_letters = [  # from stc_meta2.txt
 'Ç', #(\u00c7)   295 := LATIN CAPITAL LETTER C WITH CEDILLA
 'É', #(\u00c9)    15 := LATIN CAPITAL LETTER E WITH ACUTE
 'Ê', #(\u00ca)    21 := LATIN CAPITAL LETTER E WITH CIRCUMFLEX
 'Ñ', #(\u00d1)    92 := LATIN CAPITAL LETTER N WITH TILDE
 'Ā', #(\u0100)   736 := LATIN CAPITAL LETTER A WITH MACRON
 'Ī', #(\u012a)   257 := LATIN CAPITAL LETTER I WITH MACRON
 'Ś', #(\u015a)   965 := LATIN CAPITAL LETTER S WITH ACUTE
 'Ū', #(\u016a)   143 := LATIN CAPITAL LETTER U WITH MACRON
 'Π', #(\u03a0)     1 := GREEK CAPITAL LETTER PI
 'Ḍ', #(\u1e0c)    65 := LATIN CAPITAL LETTER D WITH DOT BELOW
 'Ḷ', #(\u1e36)    15 := LATIN CAPITAL LETTER L WITH DOT BELOW
 'Ṃ', #(\u1e42)    44 := LATIN CAPITAL LETTER M WITH DOT BELOW
 'Ṅ', #(\u1e44)    32 := LATIN CAPITAL LETTER N WITH DOT ABOVE
 'Ṇ', #(\u1e46)    29 := LATIN CAPITAL LETTER N WITH DOT BELOW
 'Ṛ', #(\u1e5a)   816 := LATIN CAPITAL LETTER R WITH DOT BELOW
 'Ṝ', #(\u1e5c)   108 := LATIN CAPITAL LETTER R WITH DOT BELOW AND MACRON
 'Ṣ', #(\u1e62)   378 := LATIN CAPITAL LETTER S WITH DOT BELOW
 'Ṭ', #(\u1e6c)    88 := LATIN CAPITAL LETTER T WITH DOT BELOW
 ]
 a = ''.join(accented_capital_letters)
 import string
 b = string.ascii_uppercase
 c = a + b
 return c

def get_small_pattern():
 accented_small_letters = [
 'à', #(\u00e0)  6974 := LATIN SMALL LETTER A WITH GRAVE
 'â', #(\u00e2)  1372 := LATIN SMALL LETTER A WITH CIRCUMFLEX
 'ä', #(\u00e4)     2 := LATIN SMALL LETTER A WITH DIAERESIS
 'ç', #(\u00e7)   851 := LATIN SMALL LETTER C WITH CEDILLA
 'è', #(\u00e8)  5976 := LATIN SMALL LETTER E WITH GRAVE
 'é', #(\u00e9) 44709 := LATIN SMALL LETTER E WITH ACUTE
 'ê', #(\u00ea)  4096 := LATIN SMALL LETTER E WITH CIRCUMFLEX
 'ë', #(\u00eb)     8 := LATIN SMALL LETTER E WITH DIAERESIS
 'î', #(\u00ee)  1421 := LATIN SMALL LETTER I WITH CIRCUMFLEX
 'ï', #(\u00ef)   171 := LATIN SMALL LETTER I WITH DIAERESIS
 'ñ', #(\u00f1)   991 := LATIN SMALL LETTER N WITH TILDE
 'ô', #(\u00f4)   532 := LATIN SMALL LETTER O WITH CIRCUMFLEX
 'ö', #(\u00f6)     2 := LATIN SMALL LETTER O WITH DIAERESIS
 'ù', #(\u00f9)   284 := LATIN SMALL LETTER U WITH GRAVE
 'û', #(\u00fb)   477 := LATIN SMALL LETTER U WITH CIRCUMFLEX
 'ü', #(\u00fc)     1 := LATIN SMALL LETTER U WITH DIAERESIS
 'ā', #(\u0101) 29210 := LATIN SMALL LETTER A WITH MACRON
 'ī', #(\u012b)  7988 := LATIN SMALL LETTER I WITH MACRON
 'ś', #(\u015b)  6379 := LATIN SMALL LETTER S WITH ACUTE
 'ū', #(\u016b)  2938 := LATIN SMALL LETTER U WITH MACRON
 'ḍ', #(\u1e0d)  1489 := LATIN SMALL LETTER D WITH DOT BELOW
 'ḥ', #(\u1e25)   478 := LATIN SMALL LETTER H WITH DOT BELOW
 'ḷ', #(\u1e37)    18 := LATIN SMALL LETTER L WITH DOT BELOW
 'ṃ', #(\u1e43)  3620 := LATIN SMALL LETTER M WITH DOT BELOW
 'ṅ', #(\u1e45)  1175 := LATIN SMALL LETTER N WITH DOT ABOVE
 'ṇ', #(\u1e47)  5536 := LATIN SMALL LETTER N WITH DOT BELOW
 'ṛ', #(\u1e5b)  4873 := LATIN SMALL LETTER R WITH DOT BELOW
 'ṣ', #(\u1e63)  8135 := LATIN SMALL LETTER S WITH DOT BELOW
 'ṭ', #(\u1e6d)  2827 := LATIN SMALL LETTER T WITH DOT BELOW
 ]
 a = ''.join(accented_small_letters)
 import string
 b = string.ascii_lowercase
 c = a + b
 return c

def lexflag(line):
 return False
 lexpatterns = [
   '¦.*? <ab>m.</ab>',  #masculine
   '¦.*? <ab>f.</ab>',  #feminine
   '¦.*? <ab>n.</ab>',  #neuter
   '¦.*? <ab>a.</ab>',  #adjective
   '¦ <ab>ind.</ab>',  # indeclineable
   '¦ <ab>inter.</ab>',  # interjection
   '¦ <ab>adv.</ab>',  # adverb
 ] 
 for pattern in lexpatterns:
  if pattern in line:
   return True
 return False

def mark_entries_verb(entries,exclusions,inclusions):
 """ stc verbs: P """
 cp = get_capital_pattern()
 sp = get_small_pattern()
 cp1 = cp + '-'
 sp1 = sp + '-'
 patterns = [
  '{@[%s]+@}¦' % cp1, #verbs
  '{@[%s]+-[%s]+@}¦' % (sp1,cp1), # prefixed verbs   
  '{@[0-9]+ +[%s]+@}¦' % cp1, #verbs with homonym
  '{@[0-9]+ +[%s]+-[%s]+@}¦' % (sp1,cp1), # prefixed verbs   with homonym
  '{@[0-9 ]*[%s]+- \([%s]+\)@}¦' % (sp1,cp1), # prefixed verbs, with verb altered

  '^{@[^@]*[%s].*?@}¦' %cp,  # odd - at least one capital letter
  #'¦ *[({@]+[%s]+[)@}]+' % cp1,
 ]
 pattern_codes = ['V','P','V1','P1','P2','Q','X']
 for entry in entries:
  k1 = entry.metad['k1']
  # first exclude known non-verbs
  if entry.metaline in exclusions:
   exclusions[entry.metaline] = True  # so we know exclusion has been used
   continue 
  if entry.metaline in inclusions:
   if k1 == 'jAgarti':
    entry.markcode = 'VX'
   else:
    entry.markcode = 'PX'
   continue
  L  = entry.metad['L']
  code = None
  linenum1 = entry.linenum1  # integer line number of metaline
  datalines = entry.datalines
  #if lexflag(datalines[0]):
  # continue

  codes = [None,None,None,None,None,None,None]
  codeidx={}
  for i,c in enumerate(pattern_codes):
   codeidx[c] = i
  # two special cases. 
  if L == '3984':
   codes[1] = 'P'
   datalines=[]
  elif L == '10446':
   codes[0] = 'V'
   datalines=[]
  lex = False
  for iline,line in enumerate(datalines):
   if iline != 0:
    break
   for ipattern,pattern in enumerate(patterns):
    if re.search(pattern,line):
     codes[ipattern] = pattern_codes[ipattern]
     break  # get all patterns # only get first pattern
  codes_used = [c for c in codes if c != None]
  if len(codes_used) != 0:
   code = ''.join(codes_used)
  if (code != None) and lex:
   print('exclude lex',code,entry.metaline)
   code=None
  if code != None:
    entry.markcode = code
 for x in exclusions:
  if not exclusions[x]:
   print('Unused exclusion:',x)

def write_verbs(fileout,entries):
 n = 0
 coded = {}
 with codecs.open(fileout,"w","utf-8") as f:
  for ientry,entry in enumerate(entries):
   code = entry.markcode
   if not code:
    continue
   if code not in coded:
    coded[code] = 0
   coded[code] = coded[code] + 1
   n = n + 1
   outarr = []
   k1 = entry.metad['k1']  
   L =  entry.metad['L']
   k2 = entry.metad['k2']
   k2a = re.sub(r'^([a-zA-Z-()]+)(.*)$',r'\1',k2)
   if k2a != k2:
    print('simplifying k2 from "%s" to "%s"'%(k2,k2a))
    k2=k2a
   outarr.append(';; Case %04d: L=%s, k1=%s, k2=%s, code=%s' %(n,L,k1,k2,code))
   for out in outarr:
    f.write(out+'\n')
 code_keys = sorted(coded.keys())
 for code in code_keys:
  print('%04d %s' %(coded[code],code))
 print('%04d' %n,"verbs written to",fileout)

def init_exclusions(filein):
 with codecs.open(filein,"r","utf-8") as f:
  recs = [x.rstrip() for x in f if not x.startswith(';')]
 d = {}
 for rec in recs:
  d[rec] = False
 print(len(recs),"records read from",filein)
 return d

def init_inclusions(filein):
 with codecs.open(filein,"r","utf-8") as f:
  recs = [x.rstrip() for x in f if not x.startswith(';')]
 d = {}
 for rec in recs:
  d[rec] = False
 print(len(recs),"records read from",filein)
 return d

if __name__=="__main__": 
 filein = sys.argv[1] #  xxx.txt (path to digitization of xxx
 #filein1 = sys.argv[2] # stc_verb_exclude.txt
 filein2 = sys.argv[2] # stc_verb_include.txt
 fileout = sys.argv[3] # 
 entries = init_entries(filein)
 exclusions = {} #init_exclusions(filein1)
 inclusions = init_inclusions(filein2)
 mark_entries_verb(entries,exclusions,inclusions)
 write_verbs(fileout,entries)
