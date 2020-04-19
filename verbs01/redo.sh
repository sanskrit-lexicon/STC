echo "remake mwverbs"
python mwverb.py mw ../../mw/mw.txt mwverbs.txt
echo "remake mwverbs1"
python mwverbs1.py mwverbs.txt mwverbs1.txt
echo "remake stc_verb_filter.txt"
python stc_verb_filter.py ../stc.txt stc_verb_include.txt stc_verb_filter.txt
echo "remake stc_verb_filter_map.txt"
python stc_verb_filter_map.py slp1 stc_verb_filter.txt mwverbs1.txt ../stc.txt  stc_verb_filter_map.txt 
echo "remake stc_verb_filter_map_deva.txt"
python stc_verb_filter_map.py deva stc_verb_filter.txt mwverbs1.txt ../stc.txt  stc_verb_filter_map_deva.txt 


echo "stc_preverb1.txt"
python preverb1.py slp1  stc_verb_filter_map.txt stc_preverb1.txt
echo "stc_preverb1_deva.txt"
python preverb1.py deva  stc_verb_filter_map.txt stc_preverb1_deva.txt
