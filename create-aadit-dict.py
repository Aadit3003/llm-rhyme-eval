import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re
import os
import random
import math
from clean import write_clean_file, file_read_strings, file_write_strings


PHON_PATH = "/home/aaditd/3_Rhyming/llm-rhyme/celex2/dutch/dpw/dpw.cd"
STRESS_PATH = "/home/aaditd/3_Rhyming/llm-rhyme/celex2/dutch/dpw/stress.txt"
DICTIONARY_PATH = "/home/aaditd/3_Rhyming/llm-rhyme/aadit's-dutch-dict"

SILLZ_PATH = "/home/aaditd/3_Rhyming/llm-rhyme/celex2/dutch/dpw/brackets_sillz.txt"
TIPZ_PATH = "/home/aaditd/3_Rhyming/llm-rhyme/celex2/dutch/dpw/brackets_tipz.txt"

random.seed(2)
first_n = len(file_read_strings(PHON_PATH))

ziploc = list(zip(file_read_strings(PHON_PATH), 
                  file_read_strings(STRESS_PATH),
                  file_read_strings(SILLZ_PATH),
                  file_read_strings(TIPZ_PATH)))



pack_strings, stress_strings, sillz_strings, tipz_strings = zip(*ziploc)
pack_strings = pack_strings[0 : first_n]
stress_strings = stress_strings[0 : first_n]

sillz_strings = sillz_strings[0 : first_n]
tipz_strings = tipz_strings[0 : first_n]




banned_indices = [i for i in range(len(sillz_strings)) if sillz_strings[i] == ""]
banned_indices = [i for i in range(len(sillz_strings)) if len(sillz_strings[i].split(" ")) > 1]
# print(banned_indices)
# print(len(banned_indices))
total = len(pack_strings)
print(total)

pack_strings = [pack_strings[i] for i in range(total) if i not in banned_indices]
stress_strings = [stress_strings[i] for i in range(total) if i not in banned_indices]
sillz_strings = [sillz_strings[i] for i in range(total) if i not in banned_indices]
tipz_strings = [tipz_strings[i] for i in range(total) if i not in banned_indices]

total = len(pack_strings)
print(total)

SYMBOLS = {
    "VOWELS": set(),
    "CONSONANTS": set()
}

def remove_slashes(index):
    i = index
    print(i)
    pack, stress, sillz, tipz = pack_strings[i], stress_strings[i], sillz_strings[i], tipz_strings[i]

    # print(sillz)

    # print(tipz)
    tokens = pack.split("\\")
    _, spelling, _, _, _, _, _  = tokens
    
    sillz = sillz.replace('\'', '')
    tipz = tipz.replace('VV', 'V')
    # print(sillz.split("-"))

    value = add_types(sillz, tipz, stress)

    write_string = f"{spelling} {value}"
    return write_string

# # ā, ē, ī, ō, ū, ȳ


def add_types(sillz, catz, stresses):
    # print(stresses)

    count = 0
    write_list = []
    # print()
    # print("INSIDE ADD TYPES")
    # print(sillz )
    # print(catz)
    for syllable, categories in zip(sillz.split("-"), catz.split("-")):

        for phoneme, category in zip(syllable, categories):

            if category == "V":

                stress = stresses[count]
                SYMBOLS["VOWELS"].add(phoneme)
                phoneme = phoneme + stress
                
            elif category == "C":
                SYMBOLS["CONSONANTS"].add(phoneme)

            write_list.append(phoneme)
        
        count += 1

    return ' '.join(write_list)

WS = [remove_slashes(i) for i in range(total)]

print(f"Started with {first_n}, but only {len(WS)} survived!")
for ws in WS:
    print(ws)


file_write_strings(DICTIONARY_PATH, WS)

# print(add_types(sillz = "krimi-na", catz = "CCVCV-CV", stresses = "10"))

print(remove_slashes(index = 5507))

print()
print()
print(SYMBOLS)