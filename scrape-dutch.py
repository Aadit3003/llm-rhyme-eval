"""
{'VOWELS': {')', 'A', '!', '|', '}', 'I', 'L', 'M', '*', 'e', '@', 'O', 'E', 'a', '<', 'K', 'i', 'o', 'u', 'y'}, 
 'CONSONANTS': {'Z', 'w', 'z', 'v', 'p', 'g', 'N', 'l', 'S', 'j', '_', 'x', 'k', 'b', 'r', 'h', 'm', 's', 'G', 't', 'd', 'f', 'n'}}

{'VOWELS': {'u', 'M', '(', 'y', '*', 'A', '!', 'o', '@', 'e', '}', '|', '<', 'L', 'O', 'i', 'E', 'K', 'a', ')', 'I'}, 
 'CONSONANTS': {'l', 'f', 'd', 'v', 'k', 'r', 'z', 't', 'g', 'N', 'b', 'w', 'Z', 'm', 'S', 'p', 'n', 's', 'h', '_', 'G', 'j', 'x'}}

{'VOWELS': {'@', 'M', 'I', '(', '}', 'K', ')', 'u', '<', 'A', '|', 'o', 'y', 'L', 'a', 'E', '*', 'e', 'O', '!', 'i'}, 
 'CONSONANTS': {'v', 'S', 'Z', 'd', 'g', 's', 'm', 'n', 'k', 'x', 'l', 'h', 'w', 'z', 'N', 't', 'G', 'j', 'f', 'b', 'r', 'p', '_'}}

{'VOWELS': {'M', ')', 'y', '*', '}', '<', 'L', 'i', 'A', '@', '|', 'o', 'K', 'O', 'u', 'e', 'a', 'I', '!', 'E', '('}, 
 'CONSONANTS': {'z', 'l', 'm', 'k', 'x', 'S', 'j', 'Z', 'G', 'w', 'h', 'v', 'p', 'r', 'd', 'b', 'f', 's', '_', 'n', 'g', 't', 'N'}}

"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re
import os
import random
from clean import write_clean_file, file_read_strings
# random.seed(2)

# ARPABET Constants
VOWELS = ['@', 'M', 'I', '(', '}', 'K', ')', 'u', \
        '<', 'A', '|', 'o', 'y', 'L', 'a', 'E', \
        '*', 'e', 'O', '!', 'i'] # 22

CONSONANTS = ['v', 'S', 'Z', 'd', 'g', 's', 'm', \
            'n', 'k', 'x', 'l', 'h', 'w', 'z', \
            'N', 't', 'G', 'j', 'f', 'b', 'r', 'p', '_'] # 23
PRON_DICTIONARY = {}

SUFFIX_MAP = {
    "acy": ["AH0 S IY0", "AE2 S IY0"],
    "al": ["AH0 L", "AA0 L", "AO2 L"],
    "ance": ["AH0 N S", "AE1 N S"], #
    "ence": ["AH0 N S", "EH1 N S", "EH0 N S"],#
    "dom": "D AH0 M",
    "er": "ER0",  #
    "or": ["ER0", "AO1 R", "AO2 R"], #
    "ism": ["IH2 Z AH0 M", "IH0 Z AH0 M"],
    "ist": ["IH0 S T", "AH0 S T"],
    "ity": ["IH0 T IY0", "AH0 T IY0"], #
    "ty": "T IY0", #
    "ment": ["M AH0 N T"],
    "ness": ["N EH2 S", "N AH0 S"],
    "ship": "SH IH0 P",
    "sion": ["SH AH0 N", "ZH AH0 N"], #
    "tion": "SH AH0 N", #
    "ure": []
}




# UTILITY FUNCTIONS
def populate_Dictionary(file):
    """
    Returns a dictionary of the form:-
    {
        word: [phoneme, phoneme2, ..., phoneme7],
        word2: [phoneme, phoneme2, ..., phoneme7],
        word3: [phoneme, phoneme2, ..., phoneme7],
    }
    """
    global PRON_DICTIONARY

    lines = file_read_strings(file)
    lines = lines[69:]

    for entry in lines:
        word, pron = entry.split(" ", 1)
        pron = pron.strip().split(" ")
        # word, pron
        if pron != ['']:
            PRON_DICTIONARY[word] = pron


    # return PRON_DICTIONARY

def findWords(suffix):
    global PRON_DICTIONARY
    all_words = list(PRON_DICTIONARY.keys())
    word_list = [a for a in all_words if suffix in a]

    

    return word_list               

def product(*args):
    if not args:
        return iter(((),)) # yield tuple()
    return (items + (item,) 
            for items in product(*args[:-1]) for item in args[-1])

# SYLLABLE FUNCTIONS

def getVowelsConsonants(word):
    global PRON_DICTIONARY

    pron = PRON_DICTIONARY[word]

    vc = [] # Useful for Perfect Rhymes
    vowels, consonants = [], [] # Useful for Assonance, Consonance

    for phoneme in pron:
        # print(word, pron)
        p_list = list(filter(None, re.split(r'(\d+)', str(phoneme))))
        phone = p_list[0]

        if len(p_list) > 1:
            stress = p_list[1]
        
        else:
            phone = p_list[0]
        if phone in VOWELS:
            vc.append(((phone, stress), "v"))
            vowels.append(phoneme)
        else:
            vc.append((phone, "c"))
            consonants.append(phone)

    return vc, vowels, consonants

def lenSymbolOverlap(consSet1, consSet2):
    consSet1 = set(consSet1.split(" "))
    consSet2 = set(consSet2.split(" "))

    overlap = consSet1.intersection(consSet2)
    # if len(overlap) == 2:
    # if len(overlap) == 0: print(f"OVERLAP:  {overlap}   WORD1: {consSet1}   WORD2: {consSet2}")
    # print(f"")
    return len(overlap)

def findPrimaryStressedSyllable(vc):
    i = 0
    onset = None
    remaining = None
    type = None

    stresses = []
    for entry, type in vc:
        if type == "v":
            stresses.append(entry[1])
            if entry[1] == "1":
                if i!= 0:
                    onset , remaining = vc[i-1], vc[i:]
        
        i += 1
    
    if "1" not in stresses:
        type = None
    elif len(stresses) == 1:
        type = "final"
    elif stresses[-1] == "1":
        type = "final"
    elif stresses[-2] == "1":
        type = "penultimate"
    else:
        type = "other"

    
    return (onset, remaining, type)

def findLastSyllable(vc):

    categories = ''.join([type for vowel, type in vc])
    lastVowelIndex = categories.rindex("v")

    nucleus = vc[lastVowelIndex]
    coda = vc[lastVowelIndex+1:]
    

    
    return (nucleus, coda)



# RHYME FUNCTIONS

def singlePerfectPairs(suffixes, outerLimit = 300, comparisonLimit = 300, lengthLimit = 500):
    """
    outerLimit: Max Number of words (ending in this suffix) to consider as "current word!"
    comparisonLimit: Max number of other words to compare to the current word
    lengthLimit: Desired no. of single perfect pairs!
    """
    single_perfect_pairs = []

    candidate_words = []

    if type(suffixes) == 'str':
        candidate_words = findWords(suffixes)
    else:
        for suffix in suffixes:
            candidate_words.extend(findWords(suffix))
    n = len(candidate_words)
    print(f"Found {n} words ending with \"{suffixes}\"")

    random.shuffle(candidate_words)

    # print(words_list)
    for i in range(n):
        current_word = candidate_words[i]
        remaining_words = candidate_words[0:i]
        random.shuffle(remaining_words)

        j = 0
        for other_word in remaining_words:
            vc_current, _, _ = getVowelsConsonants(current_word)
            vc_other, _, _ = getVowelsConsonants(other_word)

            onset_current, remaining_current, type_cur = findPrimaryStressedSyllable(vc_current)
            onset_other, remaining_other, type_oth = findPrimaryStressedSyllable(vc_other)


            if remaining_current == remaining_other and type_cur == type_oth:
                if onset_current != onset_other:
                    if type_cur == "final":
                        single_perfect_pairs.append(
                            {current_word: PRON_DICTIONARY[current_word], 
                                other_word:PRON_DICTIONARY[other_word]})
                        
                        if len(single_perfect_pairs) > 5 * lengthLimit:
                            random.shuffle(single_perfect_pairs)
                            return single_perfect_pairs[:lengthLimit]


            j += 1
            if j > comparisonLimit: break
        

        if i > outerLimit: break


    random.shuffle(single_perfect_pairs)
    return single_perfect_pairs[:lengthLimit]

def doublePerfectPairs(suffixes, outerLimit = 100, comparisonLimit = 100, lengthLimit = 1000):
    """
    outerLimit: Max Number of words (ending in this suffix) to consider as "current word!"
    comparisonLimit: Max number of other words to compare to the current word
    lengthLimit: Desired no. of single perfect pairs!
    """
    double_perfect_pairs = []

    candidate_words = []

    if type(suffixes) == 'str':
        candidate_words = findWords(suffixes)
    else:
        for suffix in suffixes:
            candidate_words.extend(findWords(suffix))
    n = len(candidate_words)
    print(f"Found {n} words ending with \"{suffixes}\"")

    random.shuffle(candidate_words)

    # print(words_list)
    for i in range(n):
        current_word = candidate_words[i]
        remaining_words = candidate_words[0:i] 
        random.shuffle(remaining_words)

        j = 0
        for other_word in remaining_words:
            vc_current, _, _ = getVowelsConsonants(current_word)
            vc_other, _, _ = getVowelsConsonants(other_word)

            onset_current, remaining_current, type_cur = findPrimaryStressedSyllable(vc_current)
            onset_other, remaining_other, type_oth = findPrimaryStressedSyllable(vc_other)


            if remaining_current == remaining_other and type_cur == type_oth:
                if onset_current != onset_other:
                    if type_cur == "penultimate":
                        double_perfect_pairs.append(
                            {current_word: PRON_DICTIONARY[current_word], 
                                other_word:PRON_DICTIONARY[other_word]})

                        if len(double_perfect_pairs) > 5 * lengthLimit:
                            random.shuffle(double_perfect_pairs)
                            return double_perfect_pairs[:lengthLimit]


            j += 1
            if j > comparisonLimit: break
        
        if i > outerLimit: break

    random.shuffle(double_perfect_pairs)
    return double_perfect_pairs[:lengthLimit]

def assonancePairs(innerLimit = 5, outerLimit = 1000):
    """
    innerLimit: The number of entries from the same vowel configuration
    outerLimit: The total number of assonance Pairs!
    """
    all_words = list(PRON_DICTIONARY.keys())

    assonancePairs = []
    VOW_MAP = {}
    i = 0
    random.shuffle(all_words)
    # Populate Vowel and Consonant Maps (All seen combinations!)
    for word in all_words:
        _, vowels, consonants = getVowelsConsonants(word)
        vowels = ' '.join(vowels)
        # print(vowels)
        consonants = ' '.join(consonants)

        if vowels not in VOW_MAP.keys():
            VOW_MAP[vowels] = [(word, consonants)]
        else:
            VOW_MAP[vowels].append((word, consonants))

        
        i += 1
        if i > 15000:
            break


    # Find Assonance pairs
    for vowel, words in VOW_MAP.items():
            if len(words) == 1:
                continue
            inner = 0
            for i in range(len(words)):
                current_word, current_cons = words[i]
                other_words = words[0:i]
                for other_word, other_cons in other_words:
                    if lenSymbolOverlap(current_cons, other_cons) == 0:
                        assonancePairs.append({
                            current_word: PRON_DICTIONARY[current_word],
                            other_word: PRON_DICTIONARY[other_word]
                        })
            
                        if len(assonancePairs) > outerLimit: 
                            return assonancePairs
                inner += 1
                if inner > innerLimit:
                    break



    return assonancePairs

def consonancePairs(innerLimit = 5, outerLimit = 1000):
    """
    innerLimit: The number of entries from the same consonant configuration
    outerLimit: The total number of assonance Pairs!
    """
    all_words = list(PRON_DICTIONARY.keys())

    consonancePairs = []

    CONS_MAP = {}
    i = 0
    random.shuffle(all_words)
    # Populate Vowel and Consonant Maps (All seen combinations!)
    for word in all_words:
        _, vowels, consonants = getVowelsConsonants(word)
        vowels = ' '.join(vowels)
        # print(vowels)
        consonants = ' '.join(consonants)


        if consonants not in CONS_MAP.keys():
            CONS_MAP[consonants] = [(word, vowels)]
        else:
            CONS_MAP[consonants].append((word, vowels))

        
        i += 1
        if i > 15000:
            break


    # Find Consonance pairs
    
    for consonant, words in CONS_MAP.items():
            if len(words) == 1:
                continue
            inner = 0
            for i in range(len(words)):
                current_word, current_vows = words[i]
                other_words = words[0:i]

                inner += 1
                if inner > innerLimit:
                    break
                for other_word, other_vows in other_words:
                    if lenSymbolOverlap(current_vows, other_vows) == 0:
                        consonancePairs.append({
                            current_word: PRON_DICTIONARY[current_word],
                            other_word: PRON_DICTIONARY[other_word]
                        })
            
                        if len(consonancePairs) > outerLimit: 
                            return consonancePairs


    return consonancePairs

def alliterativePairs(perConsLimit = 100, lengthLimit = 1000):
    # Match Initial Consonant
    # Match Number of Vowels
    # Initial Stress (but different vowels)
    """
    innerLimit: The number of entries from the same vowel configuration
    outerLimit: The total number of assonance Pairs!
    """
    all_words = list(PRON_DICTIONARY.keys())
    random.shuffle(all_words)
    alliterations_pairs = []

    consonantLexicon = {}
    """
    {
        "B":{
            "AH" : [butter, bust]
            "AA" : [bark. barn]
        }
        "M":{
            "AY" : [mite, mire]
            "EH" : [met, megalodon]
        }
    }
    """

    random.shuffle(CONSONANTS)

    # Populate lists of word starting with the consonant that have initial vowel stress!
    for consonant in CONSONANTS:
        wordsStartingWith = {}
        i = 0
        for word in all_words:

            i+= 1
            if i > perConsLimit: break

            if PRON_DICTIONARY[word][0] == consonant:
                vc, _, _ = getVowelsConsonants(word)
                
                symbol, type = vc[1]
                if type == 'v':
                    vowel, stress = symbol
                    if stress == "1":
                        # print(f"Keys: {wordsStartingWith.keys()}")
                        if vowel not in wordsStartingWith.keys():
                            wordsStartingWith[vowel] = [word]
                        else:
                            # print(wordsStartingWith)
                            # print(f"Vowel: {vowel} | Word: {word}")
                            wordsStartingWith[vowel].append(word)

        consonantLexicon[consonant] = wordsStartingWith
    
    print(consonantLexicon)

    for consonant, vowel_dic in consonantLexicon.items():
        if len(vowel_dic) <= 1:
            continue
        lists = [word_list for _, word_list in vowel_dic.items()]
        

        for i in range(1, len(lists)):
            current_list = lists[i]
            for j in range(0, i-1):
                prev_list = lists[j]
                pairs = list(product(current_list, prev_list))
                print(pairs[0:10])
                for p in pairs:
                    current_word, other_word = p
                    alliterations_pairs.append({
                        current_word: PRON_DICTIONARY[current_word],
                        other_word: PRON_DICTIONARY[other_word]
                    })
                    if len(alliterations_pairs) > 20 *lengthLimit:
                        random.shuffle(alliterations_pairs)
                        return alliterations_pairs[:lengthLimit]
    random.shuffle(alliterations_pairs)
    return alliterations_pairs[:lengthLimit]



        


def PerfectPairs(suffixes):
    return singlePerfectPairs(suffixes), doublePerfectPairs(suffixes)

def SlantPairs():
    return assonancePairs(), consonancePairs()

def nonRhymingPairs(patternLimit = 10, comparisonLimit = 20, lengthLimit = 1000):
    # Zero vowel overlap
    # Zero Consonantal overlap
    all_words = list(PRON_DICTIONARY.keys())

    non_rhyming_pairs = []

    CONS_MAP = {}
    i = 0
    random.shuffle(all_words)
    # Populate Vowel and Consonant Maps (All seen combinations!)
    for word in all_words:
        _, vowels, consonants = getVowelsConsonants(word)
        vowels = ' '.join(vowels)
        # print(vowels)
        consonants = ' '.join(consonants)


        if consonants not in CONS_MAP.keys():
            CONS_MAP[consonants] = [(word, vowels)]
        else:
            CONS_MAP[consonants].append((word, vowels))

        
        i += 1
        if i > 50000:
            break


    # Find Consonance pairs
    consonant_patterns = list(CONS_MAP.keys())

    ind = 0
    for i in range(len(consonant_patterns)):
        ind += 1
        if ind > patternLimit: break

        current_pattern = consonant_patterns[i]
        other_patterns = consonant_patterns[0:i]

        for other_pattern in other_patterns:
            if lenSymbolOverlap(current_pattern, other_pattern) <= 2:

                current_word_list = CONS_MAP[current_pattern]
                other_word_list = CONS_MAP[other_pattern]


                for cw in current_word_list:
                    c_word, c_vowels = cw
                    count = 0
                    for ow in other_word_list:

                        count += 1
                        if count > comparisonLimit: break

                        o_word, o_vowels = ow
                        if lenSymbolOverlap(c_vowels, o_vowels) == 0:
                            non_rhyming_pairs.append({
                                c_word: PRON_DICTIONARY[c_word],
                                o_word: PRON_DICTIONARY[o_word]
                            })

                            if len(non_rhyming_pairs) > 5*lengthLimit:
                                random.shuffle(non_rhyming_pairs)
                                return non_rhyming_pairs[:lengthLimit]
                        
            else:
                continue

    random.shuffle(non_rhyming_pairs)
    return non_rhyming_pairs[:lengthLimit]



# MAIN
def main():
    filename = "/home/aaditd/3_Rhyming/llm-rhyme/aadit's-dutch-dict"
    populate_Dictionary(filename)

    
    SPP_SOLUTION_WRITE_LIST = []
    DPP_SOLUTION_WRITE_LIST = []

    SUFFIXES = [["en", "eren", "heden", "mannen", "mensen", "vrouwen"], "ert", \
                "weg", ["pjes", "tjes"], "schap", "e", "dom", "'s", 'nde', \
                'ling', 'opt', ['iere', 'ieren'], 'its', 'eer', 'ouw', 'aat', ['ant', 'and']
                    ]

    random.shuffle(SUFFIXES)
    for suffix in SUFFIXES:
        lim = 500

        if suffix in ['opt', 'its', 'eer', 'ouw', 'uik', 'aat', ['ant', 'and']]:
            lim = 1000
        

        spp = singlePerfectPairs(suffix, lim, lim, 1000)
        # dpp = doublePerfectPairs(suffix, lim, lim, 1000)

        SPP_SOLUTION_WRITE_LIST.extend(spp)
        # DPP_SOLUTION_WRITE_LIST.extend(dpp)

    write_clean_file("data/dutch/solutions/singlePerfect.txt", 
                     "data/dutch/test/singlePerfect.txt",
                     SPP_SOLUTION_WRITE_LIST)
    
    # write_clean_file("data/dutch/solutions/doublePerfect.txt", 
    #                  "data/dutch/test/doublePerfect.txt",
    #                  DPP_SOLUTION_WRITE_LIST)

    # ass, cons = SlantPairs()
    # write_clean_file("data/dutch/solutions/assonance.txt",
    #                  "data/dutch/test/assonance.txt",
    #                  ass)
    
    # write_clean_file("data/dutch/solutions/consonance.txt",
    #                  "data/dutch/test/consonance.txt",
    #                  cons)

    # allit = alliterativePairs(1000)
    # write_clean_file("data/dutch/solutions/alliterative.txt",
    #                  "data/dutch/test/alliterative.txt",
    #                  allit)

    # nons = nonRhymingPairs(100, 20, 5000)
    # write_clean_file("data/dutch/solutions/non.txt",
    #                  "data/dutch/test/non.txt",
    #                  nons, 5000)

    print("DONE!!")




if __name__ == "__main__":
    main()