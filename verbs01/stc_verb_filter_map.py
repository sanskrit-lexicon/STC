#-*- coding:utf-8 -*-
"""stc_verb_filter_map.py
"""
from __future__ import print_function
import sys, re,codecs
from stc_verb_filter import init_entries,Entry
import transcoder
from transcoder import transcoder_processString
transcoder.transcoder_set_dir('transcoder')

class Stcverb(object):
 def __init__(self,line):
  line = line.rstrip()
  self.line = line
  try:
   m = re.search(r'L=([^,]*), k1=([^,]*), k2=([^,]*), code=(.*)$',line)
   self.L,self.k1,self.k2,self.code = m.group(1),m.group(2),m.group(3),m.group(4)
  except:
   print('Stcverb error: line=',line)
   exit(1)
  self.mw = None
  self.mwrec = None
  
def init_stcverb(filein):
 with codecs.open(filein,"r","utf-8") as f:
  recs = [Stcverb(x) for x in f if x.startswith(';; Case')]
 print(len(recs),"records read from",filein)
 return recs

class MWVerb(object):
 def __init__(self,line):
  line = line.rstrip()
  self.line = line
  self.k1,self.L,self.cat,self.cps,self.parse = line.split(':')
  self.used = False

def init_mwverbs(filein):
 with codecs.open(filein,"r","utf-8") as f:
  recs = [MWVerb(x) for x in f]
 print(len(recs),"mwverbs read from",filein)
 #recs = [r for r in recs if r.cat == 'verb']
 #recs = [r for r in recs if r.cat in ['root','genuineroot']]
 #recs = [r for r in recs if r.cat == 'verb']
 print(len(recs),"verbs returned from mwverbs")
 # list of keys that can be verb or preverb,
 # AND a code
 ddup = {
  'Ap':'verb','As':'verb','nI':'verb','vyac':'verb',
  'ez':'verb','prez':'preverb','vI':'preverb','vyaj':'verb',
 }
 d = {}
 for rec in recs:
  k1 = rec.k1
  if (k1 in ddup):
   if (rec.cat == ddup[k1]):
    print('Using %s form for %s'%(rec.cat,k1))
    d[k1]=rec
   else:
    print('Skipping %s form for %s'%(rec.cat,k1))
    #pass
   continue
  if k1 in d:
   print('init_mwverbs: Unexpected duplicate',k1)
  d[k1] = rec
 return recs,d


map2mw_special_R = {
 #stc:mw
 'arD':'fD',
 'ij':'yaj',
 'iD':'inD',
 'up':'vap',
 'uS':'vaS',
 'graB':'grah',
 'glA':'glE',
 'Garz':'Gfz',
 'jA':'jan',
 'tA':'tan',
 'tAq':'taq',
 'trA':'trE',
 'dIv':'div',
 'dIv':'div',
 'Day':'DA',
 'DyA':'DyE',
 'Dvas':'DvaMs',
 'pfcC':'praC',
 'pyA':'pyE',
 'praS':'praC',
 'Bfjj':'Brajj',
 'mlA':'mlE',
 'vi':'vA',
 'vyA':'vye',
 'Sat':'Sad',
 'SA':'Si',
 'Sf':'SrA',
 'SyA':'SyE',
 'SvA':'SU',
 'saD':'sAD',
 #'sA':'si',
 'sA':'so',
 'sIv':'siv',
 'styA':'styE',
 'sPA':'sPAy',
 'hU':'hve',
 'hvA':'hve',
 'svar':'svf',
 'kzI':'kzi',
 'zWIv':'zWiv',
 'stF':'stf',
 'jAgarti':'jAgf',
}
def map2mw_R(d,k1):
 """ for stc
 """
 if k1 in map2mw_special_R:
  k =  map2mw_special_R[k1]
  if k not in d:
   #print('map2mw_R Error 1: %s -> %s (not in mw)'%(k1,k))
   return k,False
  else:
   mwrec = d[k]
   if mwrec.cat != 'verb':
    print('map2mw_R Error 2: %s -> %s (a preverb)'%(k1,k))
   else:
    return k,True
 if k1 in d:
  return k1,True
 return '?',True

map2mw_special_D = {
 'acCe':'acCAi',  # probably should change MW
 'atidIv':'atidiv',
 'pratidIv':'pratidiv',
 'vidIv':'vidiv',
 'nirnI':'nirRI',
 'aDyavasA':'aDyavaso',
 'anuvyavasA':'anuvyavaso',
 'anvavasA':'anvavaso',
 'avasA':'avaso',
 'udavasA':'udavaso',
 'paryavasA':'paryavaso',
 'vyavasA':'vyavaso',
 'samavasA':'samavaso',
 'atisvar':'atisvf',
'anuDyA':'anuDyE',
 'apaDyA':'apaDyE',
 'aBiDyA':'aBiDyE',
 'aBiniDyA':'aBiniDyE',
 'avaDyA':'avaDyE',
 'ADyA':'ADyE',
 'niDyA':'niDyE',
 'nirDyA':'nirDyE',
 'parIDyA':'parIDyE',
 'praRiDyA':'praRiDyE',
 'praDyA':'praDyE',
 'saMDyA':'saMDyE',
 'samanuDyA':'samanuDyE',
 'samapaDyA':'samapaDyE',
 'samaBiDyA':'samaBiDyE',
 'samADyA':'samADyE',
 #'saMparikamp':'samparikamp',
 #'saMprakamp':'samprakamp',
 #'saMprakAS':'samprakAS',
 'viglA':'viglE',
 'anusaYj':'anuzaYj',
}
def map2mw_D(d,k1):
 """ for stc
 """
 if k1 in map2mw_special_D:
  k =  map2mw_special_D[k1]
  if k not in d:
   #print('map2mw_R Error 1: %s -> %s (not in mw)'%(k1,k))
   return k,False
  else:
   mwrec = d[k]
   if mwrec.cat != 'preverb':
    print('map2mw_D Error 2: %s -> %s (a verb)'%(k1,k))
   else:
    return k,True
 if k1 in d:
  return k1,True
 changes=[('saM','sam'),('sam','saM'),('kzI$','kzi'),
   ('trA$','trE'),('praS','praC'),('Bfjj','Brajj'),
   ('vyA$','vye'),('Sat','Sad'),('sTA$','zWA'),
   ('A$','E'),('zWIv','zWiv'),('stF$','stf'),('hU$','hve'),
   ('jAgarti','jAgf'),
   ]
 for old,new in changes:
  k = re.sub(old,new,k1)
  if k in d:
   return k,True
 return '?',True


def stcmap(recs,mwd,entry_Ldict,mwverbs):
 
 for rec in recs:
  # try mw spelling directly
  #if rec.k1 in['garayAmi']:print('stcmap chk:',rec.k1,rec.code)
  if rec.code.startswith('V'):
   rec.mw,matchflag = map2mw_R(mwd,rec.k1)
   if rec.mw in mwd:
    rec.mwrec = mwd[rec.mw]
   else:
    #print('stcmap anomaly:',rec.k1,rec.mw,rec.mw in mwd)
    pass
   if rec.k1 in ['vyaj']:print('stcmap chk:',rec.L,rec.k1,rec.code,rec.mw in mwd)
  else:  # rec.code starts with P (prefixed verb)
   L = rec.L
   entry = entry_Ldict[L]
   rec.mw,matchflag = map2mw_D(mwd,rec.k1)
   if rec.mw in mwd:
    rec.mwrec = mwd[rec.mw]
  #print('stcmap: L=%s, k1=%s, rec.mw=%s'%(rec.L,rec.k1,rec.mw))

stc_preverb_parses = {
 #'atipaT':'ati+paT',  #
}

class Stcmap(object):
 def __init__(self,out):
  self.out = out
  m = re.search(r'L=([^,]*), k1=([^,]*), k2=([^,]*), code=(.*), mw=(.*)$',out)
  self.L,self.k1,self.k2,self.code,self.mwfield = m.group(1),m.group(2),m.group(3),m.group(4),m.group(5)
  parts = self.mwfield.split(',')
  self.mwhw = parts[0]
  if len(parts) == 1:
   self.mwcat = 'verb'
  else:
   self.mwcat = parts[1]
  if len(parts) == 3:
   self.mwparse = parts[2]
   #if self.L in ['1087','2442','2799','2986','3138','3307','17851']:
   # print('Stcmap chk 2: %s, %s, mwparse="%s"'%(self.L,self.k1,self.mwparse))
  else:
   self.mwparse = None

 def transcode(self,tranin,tranout):
  k1 = transcoder_processString(self.k1,tranin,tranout)
  k2 = transcoder_processString(self.k2,tranin,tranout)
  mwhw = transcoder_processString(self.mwhw,tranin,tranout)
  ans = 'L=%s, k1=%s, k2=%s, code=%s, mw=%s,%s'%(
         self.L,k1,k2,self.code,mwhw,self.mwcat)

  if self.mwparse != None:
   mwparse = transcoder_processString(self.mwparse,tranin,tranout)
   ans = '%s,%s' %(ans,mwparse)
  return ans

parse_special_L = {
 '7183':'upa-i',
 '7190':'upa-upa-i',
 '819':'ati-A-ruh',
 '2151':'anu-aYc',
 '2152':'anu-api-DA',
 '2171':'anu-A-dru',
 '2596':'api-Uh',
 '2954':'aBi-nI', 
 '3257':'aBi-sam-ruD',
 '3420':'aBi-arh',
 '3431':'aBi-ava-pad',
 '3450':'aBi-ah',
 '3533':'aBi-upa-i', 
 '3949':'ava-Cand', 
 '3984':'ava-dA', 
 '6024':'ud-SaS', 
 '6039':'ud-Cfd',
 '6439':'ud-Df', 
 '6440':'ud-hf', 
 '6794':'upa-nI', 
 '6795':'upa-ni-i',
 '7105':'upa-A-Cid', 
 '7108':'upa-ati-gam',
 '7156':'upa-As', 
 '13384':'pari-svaYj', 
 '22014':'sam-ud-hf', 
 '6092':'ud-kaw', 
 '6119':'ud-kup', 
 '6232':'ud-puz', 
 '6270':'ud-su', 
 '6281':'ud-sPUrj', 

 '6582':'ud-muw', 
 '6585':'ud-mUrC', 

 '7016':'upa-sam-pre', 
 '7108':'upa-ati-gam', 
 '7113':'upa-A-Dam', 
 '7122':'upa-A-nud', 
 '7142':'upa-A-lap', 
 '7152':'upa-A-SaNk', 

 '7240':'ud-luRW', 
 '14937':'praty-ud-BU', 
 '19888':'vu-A-ruj', 
 '20777':'sam-vi-Df', 
 '20809':'sam-vfh', 
 '20919':'sam-sPUrj', 
 '21396':'sam-nand', 

 '22172':'sam-pari-stf', 
 '22207':'sam-pra-gA', 
 '22284':'sam-pra-manT', 
 '22318':'sam-pra-vep', 
 '22321':'sam-praC', 
 '22427':'sam-mUrC', 
 '2152':'anu-api-DA',
 '2171':'anu-A-dru',
}
def init_stcmapobj_helper(rec,mwd):
 # Case 0250: L=1942, k1=anuvimfj, k2=anu-vi-mfj, code=P ?
 assert rec.mw == '?'
 line = rec.line
 #print('init_stcmapobj_helper:',line)
 if rec.L in parse_special_L:
  k2 = parse_special_L[rec.L]
 else:
  k2 = rec.k2
 parts = k2.split('-')
 if parts[-1] in map2mw_special_R:
  parts[-1] = map2mw_special_R[parts[-1]]
 root = parts[-1]
 
 if root not in mwd:
  if len(parts) == 1:
   extra = '%s,verb'%rec.mw
   out = '%s, mw=%s'%(line,extra)
  else:
   extra = '%s,preverb'%rec.mw
   out = '%s, mw=%s'%(line,extra)
 else:
  parse = '+'.join(parts)
  out = '%s, mw=?%s,preverb,%s' %(line,rec.k1,parse)
 return out

def stc_preverb_parse(rec):
 if rec.L in parse_special_L:
  return parse_special_L[rec.L]
 mwrec = rec.mwrec
 if mwrec != None:
  return mwrec.parse
 return '?'

def init_stcmapobj(recs,mwd):
 recs1 = []
 for rec in recs:
  line = rec.line
  # add mw 
  mwrec = rec.mwrec
  #if rec.L in parse_special_L:print('chk:',rec.L,rec.k1,rec.mw,mwrec == None,rec.mw in mwd)
  if (mwrec == None) and (rec.mw == '?'):
   # Case 0250: L=1942, k1=anuvimfj, k2=anu-vi-mfj, code=P ?
   out = init_stcmapobj_helper(rec,mwd)
   #continue
  elif mwrec == None:
   extra = rec.mw
   #print('chk:',line,rec.mw)
   if not rec.mw.startswith('?'):
    # sometimes, rec.mw is a guess, but not a verb in mw.
    # make these cases easy to identify
    if rec.mw in stc_preverb_parses:
     parse = stc_preverb_parses[rec.mw]
     extra = '%s,preverb,%s' %(rec.mw,parse)
    else:
     extra = '%s,verb'%rec.mw
    extra = '?'+extra
   out = '%s, mw=%s'%(line,extra)
  elif rec.L == '19369':  # vI, as verb
   cat = 'verb'
   out = '%s, mw=%s,%s' %(line,rec.mw,cat)
  elif mwrec.cat == 'verb':
   out = '%s, mw=%s,%s' %(line,rec.mw,mwrec.cat)
  elif mwrec.cat == 'preverb':
   parse = stc_preverb_parse(rec)
   out = '%s, mw=%s,%s,%s' %(line,rec.mw,mwrec.cat,parse)
  else:
   print('init_stcmapobj. mwrec=%s',mwrec.line)
   exit(1)
  recs1.append(Stcmap(out))
 return recs1

def write(fileout,recs,tranout):
 tranin = 'slp1'
 n = 0
 nprob = 0
 with codecs.open(fileout,"w","utf-8") as f:
  for rec in recs1:
   n = n + 1
   outrec = rec.transcode(tranin,tranout)
   out = ';; Case %04d: %s' %(n,outrec)
   f.write(out+'\n')
 print(n,"records written to",fileout)

if __name__=="__main__": 
 tranout = sys.argv[1]
 filein = sys.argv[2] #  stc_verb_filter.txt
 filein2 = sys.argv[3] # mwverbs1
 filein3 = sys.argv[4] # stc.txt
 fileout = sys.argv[5]

 recs = init_stcverb(filein)
 mwverbrecs,mwverbsd= init_mwverbs(filein2)
 entries = init_entries(filein3)
 entry_Ldict = Entry.Ldict
 stcmap(recs,mwverbsd,entry_Ldict,mwverbrecs)
 recs1 = init_stcmapobj(recs,mwverbsd)
 write(fileout,recs1,tranout)
