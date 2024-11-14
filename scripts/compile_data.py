# coding: utf-8

import sys
sys.path.insert(1, './')

from pysle import isletool
from collections import defaultdict, Counter
import re
import random
import codecs
import json


isleDict = isletool.Isle("data/ISLEdict.txt")

# load forbidden words
with open('data/nope.txt','rt') as f:
    nope = set([codecs.decode(t.strip().encode(),'hex').decode('utf8') for t in f])


# re to find initial stressed vowel
raw_vowels = [u'aʊ', u'ei', u'i', u'oʊ', u'u', u'æ',
             u'ɑ', u'ɑɪ', u'ɔ', u'ɔi', u'ə', u'ɚ', u'ɛ', u'ɝ',
             u'ɪ', u'ʊ', u'ʌ', u'ɛ̃']
vowel_sounds = [fr'{vs} ?\.? ɹ' for vs in raw_vowels] + [fr'{vs} ?\.? l' for vs in raw_vowels] + raw_vowels
vre = '|'.join(vowel_sounds)
initial_stressed_vowel_sound = fr"^#[^#]*ˈ({vre})\s"


# make mapping for intial stressed vowel sounds
t_cands = defaultdict(set)
for trochee in isleDict.search("",numSyllables=2,multiword='no',stressedSyllable='only',wordInitial='only',pos='nn'):
    t = trochee['word']
    if t in nope or len(t) < 4:
        continue
    # check part of speech
    pos = trochee['posList']
    if 'nn' not in [p.strip() for p in pos.split(',')]:
        continue
    pr = trochee['pronunciation']
    matches = re.findall(initial_stressed_vowel_sound,pr)
    if matches:
        m = matches[0].replace(' .','')
        t_cands[m].add(t)

# define expletives
expletives = [
    ('arse','ɑ ɹ'),
    ('ass','æ'),
    ('belch','ɛ l'),
    ('bile','ɑɪ l'),
    ('boff','ɑ'),
    ('boink','ɔi'),
    ('boob','u'),
    ('bone','oʊ'),
    ('bung','ʌ'),
    ('burp','ɝ ɹ'),
    ('butt','ʌ'),
    ('chode','oʊ'),
    ('cock','ɑ'),
    ('cooch','u'),
    ('crap','æ'),
    ('dick','ɪ'),
    ('dong','ɑ'),
    ('doof','u'),
    ('dook','u'),
    ('douche','u'),
    ('dump','ʌ'),
    ('fart','ɑ ɹ'),
    ('felch','ɛ l'),
    ('filth','ɪ l'),
    ('fuck','ʌ'),
    #('hump','ə'),
    ('jizz','ɪ'),
    ('knob','ɑ'),
    ('muff','ʌ'),
    ('nad','æ'),
    ('nard','ɑ ɹ'),
    ('nut','ʌ'),
    ('pee','i'),
    ('piss','ɪ'),
    ('prick','ɪ'),
    ('pube','u'),
    ('puke','u'),
    ('puss','ʊ'),
    ('puss','ʌ'),
    ('queef','i'),
    ('schlong','ɑ'),
    ('scrote','oʊ'),
    ('scum','ʌ'),
    ('shag','æ'),
    ('shit','ɪ'),
    ('shite','ɑɪ'),
    ('smut','ʌ'),
    ('snot','ɑ'),
    ('spit','ɪ'),
    ('splooge','u'),
    ('spunk','ʌ'),
    ('taint','ei'),
    ('tit','ɪ'),
    ('turd','ɝ ɹ'),
    ('vag','æ'),
    ('wank','æ'),
]


# trochee counts for each expletive
t_counts = {(e,vs):len(t_cands[vs]) for (e,vs) in expletives}
print(t_counts)

print([(k,v) for (k,v) in t_counts.items() if v < 50])

# write data files
with open('data/expletives.json','wt') as f:
    json.dump(expletives,f)
with open('data/t_cands.json','wt') as f:
    json.dump({k:list(t) for (k,t) in t_cands.items()},f)


