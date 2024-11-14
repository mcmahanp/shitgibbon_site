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
    if t in nope:
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
    ('shit','ɪ'),
    ('fuck','ʌ'),
    ('ass','æ'),
    ('dick','ɪ'),
    ('cock','ɑ'),
    ('douche','u'),
    ('fart','ɑ ɹ'),
    ('spunk','ʌ'),
    ('crap','æ'),
    ('splooge','u'),
    ('piss','ɪ'),
    ('jizz','ɪ'),
    ('vag','æ'),
    ('tit','ɪ'),
    ('chode','oʊ'),
    ('butt','ʌ'),
    ('arse','ɑ ɹ'),
    ('wank','æ'),
    ('nut','ʌ'),
    ('muff','ʌ'),
    ('scrote','oʊ'),
    ('snot','ɑ'),
    ('dong','ɑ'),
    ('shite','ɑɪ'),
    ('taint','ei'),
    ('turd','ɝ ɹ'),
    ('queef','i'),
    ('doof','u'),
    ('dook','u'),
    ('prick','ɪ'),
    ('pee','i'),
    ('boob','u'),
    ('bung','ʌ'),
    ('cooch','u'),
    ('felch','ɛ l'),
    ('belch','ɛ l'),
    ('dump','ʌ'),
    ('scum','ʌ'),
    ('knob','ɑ'),
    ('nad','æ'),
    ('nard','ɑ ɹ'),
    ('pube','u'),
    ('puke','u'),
    ('schlong','ɑ')
]


# trochee counts for each expletive
t_counts = {e:len(t_cands[vs]) for (e,vs) in expletives}
print(t_counts)

# write data files
with open('data/expletives.json','wt') as f:
    json.dump(expletives,f)
with open('data/t_cands.json','wt') as f:
    json.dump({k:list(t) for (k,t) in t_cands.items()},f)


