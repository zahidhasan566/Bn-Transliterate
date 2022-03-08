#!/usr/local/bin/python
# coding:utf8
import re
# import numpy as np
import pandas as pd
from trans_dict import trans_bng
from literal_dict import literal
from literal_dict import modific
from pyavrophonetic import avro
from default_dict import trans_words

# counts
ctl_bn = 0
ctl_eng = 0
ctl_1w = 0
ctl_23w = 0
ctl_nw = 0
ctl_words = 0
ctl_sentences = 0
c_lw = 0
ctl_spc = 0
c_noTl = 0
ctl_num = 0
flag_sentences = 0
sp_chars = re.compile('[@_!#$%^&*()<>?/|}{~:\']')
sp_and = re.compile('[&]')


org_file = "C:\\Users\\Daraz\\Desktop\\transfeb\\zahid\\part3_5500.csv"
trans_file = "C:\\Users\Daraz\Desktop\\transfeb\\zahid\\\part3_5500-trans.csv"
new_file = "C:\\Users\Daraz\\Desktop\\transfeb\\zahid\\part3_5500-new.csv"
perfect_file = "C:\\Users\\Daraz\\Desktop\\transfeb\\zahid\\part3_5500-perf.csv"
imperfect_file = "C:\\Users\Daraz\\Desktop\\transfeb\\zahid\\part3_5500-notFound.csv"

df = pd.read_csv(org_file, encoding="ISO-8859-1")
df.columns = ['Original_Word']
t_sentences = []
perfect_sentence_org = []
perfect_sentence_trans = []
imperfect_sentence_org = []
imperfect_sentence_trans = []
not_found_org = []
not_found_trans = []
not_found_cat = []
not_found_mod=[]

for sentence in df['Original_Word']:
    flag_sentences = 0
    # print('sentence: ', sentence)
    # print(ctl_sentences)
    translated_sentence = ""
    if type(sentence) != float:
        sentence = sentence.replace(".", " ")
        words = sentence.split()
    else:
        translated_sentence = translated_sentence + avro.parse(word) + " "
        ctl_num += 1
        t_sentences.append(translated_sentence)
        continue

    ctl_sentences += 1

    for word in words:
        word=word.lower()
        transliteration = trans_bng.get(word, '909')  # getting bangla directly from trans_dict
        ctl_words += 1
        if transliteration != '909':  # setting bangla directly
            # print('TL-BN')
            ctl_bn += 1
            translated_sentence = translated_sentence + transliteration + " "
        else:
            transform = trans_words.get(word, '909')  # getting english transliteration from default_dict
            if transform != '909':
                # print('TL-ENG')
                ctl_eng += 1
                translated_sentence = translated_sentence + avro.parse(transform) + " "
            else:
                if len(word) == 1:  # translitering one letter like X
                    ctl_1w += 1
                    if re.match('^[a-zA-Z0-9_]', word):
                        translated_sentence = translated_sentence + literal.get(word.upper()) + " "
                    else:
                        # print("sp-c: ", word)
                        translated_sentence = translated_sentence + word + " "
                elif 1 < len(word) < 4 and word.isupper():  # translitering 2-3 letter like XYX
                    # print('TL-23Word')
                    ctl_23w += 1
                    word = " ".join(word)
                    letters = word.split()
                    # print(word)
                    for l in letters:
                        # print(l)
                        # print(literal.get(l))
                        if re.match('^[a-zA-Z0-9]', l):
                            translated_sentence = translated_sentence + literal.get(l.upper()) + " "
                        else:
                            # print("sp-c: ", l)
                            translated_sentence = translated_sentence + l + " "
                else:
                    if len(word) > 14 and not (" " in word):
                        # print('Long-word')
                        c_lw += 1
                        translated_sentence = translated_sentence + word + " "
                        not_found_org.append(word)
                        not_found_mod.append(word)
                        not_found_trans.append(word)
                        not_found_cat.append('Long-word')
                    elif word.isnumeric():
                        ctl_num += 1
                        translated_sentence = translated_sentence + avro.parse(word) + " "
                    elif word.isalnum():
                        # place phonetic modification
                        # print('TL-NW-ALNUM')
                        ctl_nw += 1
                        org_word=word
                        for key in modific:
                            if key in word.lower():
                                # print(key, "->", modific[key])
                                word = word.replace(key, modific[key])
                        #replace T
                        translated_sentence = translated_sentence + avro.parse(word) + " "
                        not_found_org.append(org_word)
                        not_found_mod.append(word)
                        not_found_trans.append(avro.parse(word))
                        not_found_cat.append('TL-NW-ALNUM')
                    elif sp_chars.search(word) is not None:
                        # print('TL-NW-SPCHAR')
                        ctl_spc += 1
                        raw_word = re.sub('[^A-Za-z0-9]+', '', word)
                        # print(word)
                        # print(raw_word)
                        transliteration = trans_bng.get(raw_word.lower(), '909')
                        if transliteration != '909':
                            # print('TL-BN')
                            ctl_bn += 1
                            if raw_word in word:
                                translated_sentence = translated_sentence + word.replace(raw_word,
                                                                                         transliteration) + " "  # replace here
                            else:
                                translated_sentence = translated_sentence + transliteration + " "
                        else:
                            transform = trans_words.get(raw_word.lower(), '909')
                            if transform != '909':
                                # print('TL-ENG')
                                ctl_eng += 1
                                if raw_word in word:
                                    translated_sentence = translated_sentence + word.replace(raw_word, avro.parse(
                                        transform)) + " "  # replace here
                                else:
                                    translated_sentence = translated_sentence + avro.parse(
                                        transform) + " "  # replace here
                            else:
                                flag_sentences += 1

                                translated_sentence = translated_sentence + word + " "  # replace here
                                c_noTl += 1
                                not_found_org.append(word)
                                not_found_mod.append(word)
                                not_found_trans.append(word)
                                not_found_cat.append('TL-NW-SP-Error')
                    else:
                        translated_sentence = translated_sentence + word + " "
                        c_noTl += 1
                        not_found_org.append(word)
                        not_found_mod.append(word)
                        not_found_trans.append(word)
                        not_found_cat.append('TL-NW-Error')
    if flag_sentences == 0:
        perfect_sentence_org.append(sentence)
        perfect_sentence_trans.append(translated_sentence)
    else:
        imperfect_sentence_org.append(sentence)
        imperfect_sentence_trans.append(translated_sentence)
    t_sentences.append(translated_sentence)

df['translated_words'] = t_sentences
df.to_csv(trans_file, header=True, index=False, encoding="utf-8")

# nf_words = {'perfect_sentence_org': perfect_sentence_org, 'perfect_sentence_trans': perfect_sentence_trans}
# df = pd.DataFrame(nf_words)
# df.to_csv(perfect_file, index=False)
#
# nf_words = {'imperfect_sentence_org': perfect_sentence_org, 'imperfect_sentence_trans': perfect_sentence_trans}
# df = pd.DataFrame(nf_words)
# df.to_csv(imperfect_file, index=False)

if ctl_nw != 0:
    nf_words = {'not_found_org': not_found_org, 'not_found_mod':not_found_mod, 'not_found_trans': not_found_trans, 'not_found_cat': not_found_cat}
    df = pd.DataFrame(nf_words)
    df.to_csv(new_file, index=False)

print('sentences ', ctl_sentences)
print('words ', ctl_words)
print('ctl_bn ', ctl_bn)
print('ctl_eng ', ctl_eng)
print('ctl_1w ', ctl_1w)
print('ctl_23w ', ctl_23w)
print('ctl_nw', ctl_nw)
print('c_lw ', c_lw)
print('ctl_spc ', ctl_spc)
print('c_noTl ', c_noTl)
print('c_num ', ctl_num)
