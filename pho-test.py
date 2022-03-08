#!/usr/local/bin/python
# coding:utf8
import re
from trans_dict import trans_bng
from literal_dict import literal
from literal_dict import modific
from pyavrophonetic import avro
from default_dict import trans_words

# sp_chars = re.compile('[@_!#$%^&*()<>?/\|}{~:]\'');
# l='å';
# print(l.isalnum())
sp_chars = re.compile('[@_!#$%^&*()<>?/|}{~:\']')

sentence = "A Decisive Tex"
translated_sentence = ""



flag_sentences = 0
if type(sentence) != float:
    sentence = sentence.replace(".", " ")
    words = sentence.split()
else:
    translated_sentence = translated_sentence + avro.parse(word) + " "

for word in words:
    word=word.lower()
    print(word)
    transliteration = trans_bng.get(word, '909')  # getting bangla directly from trans_dict
    if transliteration != '909':  # setting bangla directly
        print('TL-BN')
        translated_sentence = translated_sentence + transliteration + " "
    else:
        transform = trans_words.get(word, '909')  # getting english transliteration from default_dict
        if transform != '909':
            print('TL-ENG')
            translated_sentence = translated_sentence + avro.parse(transform) + " "
        else:
            if len(word) == 1:  # translitering one letter like X
                if re.match('^[a-zA-Z0-9_]', word):
                    translated_sentence = translated_sentence + literal.get(word.upper()) + " "
                else:
                    print("sp-c: ", word)
                    translated_sentence = translated_sentence + word + " "
            elif 1 < len(word) < 4 and word.isupper():  # transliterating 2-3 letter like XYX
                # print('TL-23Word')
                word = " ".join(word)
                letters = word.split()
                # print(word)
                for l in letters:
                    # print(l)
                    # print(literal.get(l))
                    if re.match('^[a-zA-Z0-9]', l):
                        translated_sentence = translated_sentence + literal.get(l.upper()) + " "
                    else:
                        print("sp-c: ", l)
                        translated_sentence = translated_sentence + l + " "
            else:
                if len(word) > 14 and not (" " in word):
                    print('Long-word')
                    translated_sentence = translated_sentence + word + " "
                elif word.isnumeric():
                    translated_sentence = translated_sentence + avro.parse(word) + " "
                elif word.isalnum():
                    # place phonetic modification
                    print('TL-NW-ALNUM')
                    for key in modific:
                        if key in word:
                            print(key, "->", modific[key])
                            word = word.replace(key, modific[key])
                    translated_sentence = translated_sentence + avro.parse(word) + " "
                elif sp_chars.search(word) is not None:
                    print('TL-NW-SPCHAR')
                    raw_word = re.sub('[^A-Za-z0-9]+', '', word)
                    print(word)
                    print(raw_word)
                    transliteration = trans_bng.get(raw_word.lower(), '909')
                    if transliteration != '909':
                        print('TL-BN')
                        if raw_word in word:
                            translated_sentence = translated_sentence + word.replace(raw_word,
                                                                                     transliteration) + " "  # replace here
                        else:
                            translated_sentence = translated_sentence + transliteration + " "
                    else:
                        transform = trans_words.get(raw_word.lower(), '909')
                        if transform != '909':
                            print('TL-ENG')
                            if raw_word in word:
                                translated_sentence = translated_sentence + word.replace(raw_word, avro.parse(
                                    transform)) + " "  # replace here
                            else:
                                translated_sentence = translated_sentence + avro.parse(transform) + " "  # replace here
                        else:
                            flag_sentences += 1
                            print('No-Trans')
                            translated_sentence = translated_sentence + word + " "  # replace here

print(translated_sentence)


# word = "fZashon"
# for key in modific:
#     if key in word:
#         print(key, "->", modific[key])
#         word=word.replace(key, modific[key])
# print(word)
# print(avro.parse(word))