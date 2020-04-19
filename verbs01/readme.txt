
Analysis of stc verbs
This work was done in a temporary subdirectory (temp_verbs01) of csl-orig/v02/stc/.

The shell script redo.sh reruns several python programs, from mwverb.py to verb1.py.


* mwverbs
python mwverb.py mw ../../mw/mw.txt mwverbs.txt
#copy from v02/mw/temp_verbs
#cp ../../mw/temp_verbs/verb.txt mwverbs.txt
each line has 5 fields, colon delimited:
 k1
 L
 verb category: genuinroot, root, pre,gati,nom
 cps:  classes and/or padas. comma-separated string
 parse:  for pre and gati,  shows x+y+z  parsing prefixes and root

* mwverbs1.txt
python mwverbs1.py mwverbs.txt mwverbs1.txt
Merge records with same key (headword)
Also  use 'verb' for categories root, genuineroot, nom
and 'preverb' for categories pre, gati.
Format:
 5 fields, ':' separated
 1. mw headword
 2. MW Lnums, '&' separated
 3. category (verb or preverb)
 4. class-pada list, ',' separated
 5. parse. Empty for 'verb' category. For preverb category U1+U2+...+root

* stc_verb_filter.
stc has prefixed verbs as separate entries (like MW, in contrast to pwg, etc.).

python stc_verb_filter.py ../stc.txt  stc_verb_include.txt stc_verb_filter.txt

Patterns for non-prefixed verbs:
V  {@X-@}¦ where X contains only 'capital' letters, with ending '-'
   Example: {@AÑC-@}¦ 
V1 {@n @X-@}¦ Same, but with homonym
   Example: {@1 AJ-@}¦ 
VX Only example: {@1 jāgarti@}¦ ({@GṚ-@}

Patterns for prefixed verbs:
P  {@P-X-@}¦ where X is as above, and P contains 'small' letters and -
   Example: {@acchā-GAM-@}¦ 
P1 {@n P-X-@}¦ Same, but with homonym
   Example: {@1 ati-BHŪ-@}¦
P2 {@[0-9 ]*[%s]+- \([%s]+\)@} Same, but with base form of verb altered
   Example: {@sam-upe- (I-)@}   sam+upa+i == samupe
PX Other patterns (in file stc_verb_include.txt). 
   Example: {@uc-chaś-@}¦ ({@ŚAŚ-@})
   Note: It might be better to have changed the markup of such cases to:
   {@uc-chaś- (ŚAŚ-)@}¦   , which would be like P2.

Counts of total patterns:
24574 entries found (verbs and nonverbs)
2863 P
0143 P1
0074 P2
0169 PX
0456 V
0177 V1
0001 VX
(+ 456 177 1)
(+ 2863 143 74 169)
Total 634 entries identified as non-prefixed verbs.
Total 3249 entries identified as prefixed verbs>

Format of file stc_verb_filter.txt by example:
;; Case 0001: L=201, k1=ac, k2=ac, code=V
;; Case 0002: L=232, k1=acCAgam, k2=acCA-gam, code=P
;; Case 0003: L=233, k1=acCAcar, k2=acCA-car, code=P
;; Case 0004: L=236, k1=acCe, k2=acCe(i), code=P2


* stc_verb_filter_map
python stc_verb_filter_map.py slp1 stc_verb_filter.txt mwverbs1.txt ../stc.txt stc_verb_filter_map.txt 

python stc_verb_filter_map.py deva stc_verb_filter.txt mwverbs1.txt ../stc.txt  stc_verb_filter_map_deva.txt 


Correspondences between stc verb spellings and
 - stc verb spellings
 - mw verb spellings

Uses some empirically derived rules, and some empirically derived mappings.
In most cases, the stc headword spelling for a verb, whether prefixed or
unprefixed, agrees with the spelling of MW. For instance
<L>232<pc>8,1<k1>acCAgam<k2>acCA-gam
{@acchā-GAM-@}¦ aller vers.

But in some cases, STC uses a different spelling. For instance,
both hU and hvA in STC are believed to correspond to 'hve' in MW.
;; Case 3868: L=24485, k1=hU, k2=hU, code=V, mw=hve,verb
<L>24485<pc>891,1<k1>hU<k2>hU
{@HŪ-@}¦ ({%HVĀ-%}) {%-hvayati te ; juhāva ; hūyate johavīti ; hūta-%}
{%hvātum hūtvā °hūya%} -- appeler, appeler en défi. défier.
<L>24572<pc>894,2<k1>hvA<k2>hvA
{@HVĀ-@}¦ <ab>v.</ab> {%-HŪ-.%}

;; Case 3882: L=24572, k1=hvA, k2=hvA, code=V, mw=hve,verb

And similarly, several prefixed verbs with hU in stc are believed to
correspond to prefixed verbs with hve in MW:
;; Case 1020: L=5864, k1=AhU, k2=A-hU, code=P, mw=Ahve,preverb,A+hve
;; Case 1327: L=7082, k1=upahU, k2=upa-hU, code=P, mw=upahve,preverb,upa+hve
;; Case 1365: L=7170, k1=upAhU, k2=upA-hU, code=P, mw=upAhve,preverb,upa+A+hve
;; Case 2297: L=14915, k1=pratyAhU, k2=praty-A-hU, code=P, mw=pratyAhve,preverb,prati+A+hve
;; Case 3551: L=21903, k1=samAhU, k2=sam-A-hU, code=P, mw=samAhve,preverb,sam+A+hve
;; Case 3636: L=22092, k1=samupahU, k2=sam-upa-hU, code=P, mw=samupahve,preverb,sam+upa+hve

When there is no MW entry for an STC verb or prefixed verb, the markup
'mw=?...' so indicates.  
There are 109 such instances; and it so happens that all of these are 
prefixed verb forms.
For example:
;; Case 0046: L=561, k1=atimfd, k2=ati-mfd, code=P, mw=?atimfd,preverb,ati+mfd
Here, 'mfd' is a verb in STC, which is spelled the same way in MW.
However, MW has no entry for the prefixed verb 'atimfd'; hence the '?' mark.

* stc_preverb1.txt and stc_preverb1_deva.txt
python preverb1.py slp1  stc_verb_filter_map.txt stc_preverb1.txt
python preverb1.py deva  stc_verb_filter_map.txt stc_preverb1_deva.txt

One prints Sanskrit text in SLP1, and the other prints Sanskrit text in
Devanagari.

The stc_preverb1 report is a reorganization of stc_verb_filter_map.
It groups the various entries related to a given MW verb entry.
For example, for the mw verb 'hve':

; Verb 0591: hve (2 verb entries, 6 prefix entries)
  L=24485 k1=hU         code=V   mw=hve,verb
  L=24572 k1=hvA        code=V   mw=hve,verb
  L=5864  k1=AhU        code=P   mw=Ahve,preverb,A+hve
  L=7082  k1=upahU      code=P   mw=upahve,preverb,upa+hve
  L=7170  k1=upAhU      code=P   mw=upAhve,preverb,upa+A+hve
  L=14915 k1=pratyAhU   code=P   mw=pratyAhve,preverb,prati+A+hve
  L=21903 k1=samAhU     code=P   mw=samAhve,preverb,sam+A+hve
  L=22092 k1=samupahU   code=P   mw=samupahve,preverb,sam+upa+hve

First appears the entries in STC for the STC roots that correspond to 
the mw spelling; in the case of 'hve', there are the two STC roots 'hU'
and 'hvA'.

Next appear 6 entries whose headword is believed to be a prefixed verb for
stc root 'hU', and the corresponding MW prefixed roots (for 'hve').

