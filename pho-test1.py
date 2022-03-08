#!/usr/local/bin/python
# coding:utf8
import re
from trans_dict import trans_bng
from literal_dict import literal
from literal_dict import modific
from pyavrophonetic import avro
from default_dict import trans_words

word = "piur"
for key in modific:
    if key in word:
        print(key, "->", modific[key])
        word=word.replace(key, modific[key])
print(word)
print(avro.parse(word))
