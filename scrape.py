import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re
import os
import random
# random.seed(2)

# ARPABET Constants
VOWELS = ["AO", "AH", "OY", "AW", "UW", \
        "UH", "OW", "AY", "IH", "ER", \
        "EH", "IY", "AE", "AA", "EY"] # 15

CONSONANTS = ["B", "CH", "D", "DH", "F", "G", \
            "HH", "JH", "K", "L", "M", "N", \
            "NG", "P", "R", "S", "SH", "T", \
            "TH", "V", "W", "Y", "Z", "ZH"] # 24
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



"""
        Phoneme Example Translation
        ------- ------- -----------
        AA	odd     AA D
        AE	at	AE T
        AH	hut	HH AH T
        AO	ought	AO T
        AW	cow	K AW
        AY	hide	HH AY D
        B 	be	B IY
        CH	cheese	CH IY Z
        D 	dee	D IY
        DH	thee	DH IY
        EH	Ed	EH D
        ER	hurt	HH ER T
        EY	ate	EY T
        F 	fee	F IY
        G 	green	G R IY N
        HH	he	HH IY
        IH	it	IH T
        IY	eat	IY T
        JH	gee	JH IY
        K 	key	K IY
        L 	lee	L IY
        M 	me	M IY
        N 	knee	N IY
        NG	ping	P IH NG
        OW	oat	OW T
        OY	toy	T OY
        P 	pee	P IY
        R 	read	R IY D
        S 	sea	S IY
        SH	she	SH IY
        T 	tea	T IY
        TH	theta	TH EY T AH
        UH	hood	HH UH D
        UW	two	T UW
        V 	vee	V IY
        W 	we	W IY
        Y 	yield	Y IY L D
        Z 	zee	Z IY
        ZH	seizure	S IY ZH ER

"""


# UTILITY FUNCTIONS
def file_read_strings(path):
    """
    Read a file into a list of strings. If the file cannot be
    read, print an error message and return an empty list.
    """
    try:
        f = open (path, 'rb')
        contents = f.read().decode("latin-").splitlines()
        f.close ()
        return contents
    except Exception as e:
        print(f'Error: Cannot read {path}\n    {str(e)}')
        return None


def file_write_strings(path, lst):
    """
    Write a list of strings (or things that can be converted to
    strings) to a file. If the file cannot be written, print an
    error message.

    path: A file path
    lst: A list of strings or things that can be converted to strings.
    """
    try:
        f = open (path, 'w')
        for l in lst:
            f.write(str(l) + '\n')
    except Exception as e:
        print(f'Error: Cannot write {path}\n    {str(e)}')
        return None

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
        PRON_DICTIONARY[word.lower()] = pron


    # return PRON_DICTIONARY

def findWords(suffix):
    global PRON_DICTIONARY
    all_words = list(PRON_DICTIONARY.keys())
    word_list = [a for a in all_words if suffix in a]

    

    return word_list               
                    
# SYLLABLE FUNCTIONS

def getVowelsConsonants(word):
    global PRON_DICTIONARY

    pron = PRON_DICTIONARY[word]

    vc = [] # Useful for Perfect Rhymes
    vowels, consonants = [], [] # Useful for Assonance, Consonance

    for phoneme in pron:
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

def noSymbolOverlap(consSet1, consSet2):
    consSet1 = set(consSet1.split(" "))
    consSet2 = set(consSet2.split(" "))

    overlap = consSet1.intersection(consSet2)
    # if len(overlap) == 2:
    if len(overlap) == 0: print(f"OVERLAP:  {overlap}   WORD1: {consSet1}   WORD2: {consSet2}")
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
        remaining_words = candidate_words[0:i] + candidate_words[i+1:]
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
                        
                        if len(single_perfect_pairs) > lengthLimit:
                            return single_perfect_pairs


            j += 1
            if j > comparisonLimit: break
        

        if i > outerLimit: break



    return single_perfect_pairs

def doublePerfectPairs(suffixes, outerLimit = 100, comparisonLimit = 100, lengthLimit = 500):
    """
    outerLimit: Max Number of words (ending in this suffix) to consider as "current word!"
    comparisonLimit: Max number of other words to compare to the current word
    lengthLimit: Desired no. of single perfect pairs!
    """
    single_perfect_pairs = []
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
        remaining_words = candidate_words[0:i] + candidate_words[i+1:]
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

                        if len(double_perfect_pairs) > lengthLimit:
                            return double_perfect_pairs


            j += 1
            if j > comparisonLimit: break
        
        if i > outerLimit: break

    return double_perfect_pairs

# Old, deprecated
def imperfectPairs(suffixes, outerLimit = 1000, comparisonLimit = 1000, lengthLimit = 500):
    """
    outerLimit: Max Number of words (ending in this suffix) to consider as "current word!"
    comparisonLimit: Max number of other words to compare to the current word
    lengthLimit: Desired no. of single perfect pairs!
    """

    imperfect_pairs = []

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
        remaining_words = candidate_words[0:i] + candidate_words[i+1:]
        random.shuffle(remaining_words)

        j = 0
        for other_word in remaining_words:
            vc_current, _, _ = getVowelsConsonants(current_word)
            vc_other, _, _ = getVowelsConsonants(other_word)

            nucleus_current, coda_current = findLastSyllable(vc_current)
            nucleus_other, coda_other = findLastSyllable(vc_other)


            if coda_current[1:] == coda_other[1:] and nucleus_current[1] != nucleus_other[1]:
                    imperfect_pairs.append(
                            {current_word: PRON_DICTIONARY[current_word], 
                                other_word:PRON_DICTIONARY[other_word]})

                    if len(imperfect_pairs) > lengthLimit:
                            return imperfect_pairs


            j += 1
            if j > comparisonLimit: break
        
        if i > outerLimit: break

    return imperfect_pairs
    

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
                    if noSymbolOverlap(current_cons, other_cons) == 0:
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


    # Find Assonance pairs
    
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
                    if noSymbolOverlap(current_vows, other_vows) == 0:
                        consonancePairs.append({
                            current_word: PRON_DICTIONARY[current_word],
                            other_word: PRON_DICTIONARY[other_word]
                        })
            
                        if len(consonancePairs) > outerLimit: 
                            return consonancePairs


    return consonancePairs

def alliterativeConsPairs(innerLimit = 5, outerLimit = 1000):
    a = 0
    # Match Initial Consonant
    # Match Number of Vowels
    # Initial Stress (but different vowels)

def PerfectPairs(suffixes):
    return singlePerfectPairs(suffixes), doublePerfectPairs(suffixes)

def SlantPairs():
    return assonancePairs(), consonancePairs()

def nonRhymingPairs(outerLimit = 1000, comparisonLimit = 1000, lengthLimit = 500):
    # No Consonant Overlap
    # Different vowels!

    a = 0


# MAIN
def main():
    filename = "/home/aaditd/3_Rhyme/cmudict-0.7b"
    populate_Dictionary(filename)

    
    SPP_SOLUTION_WRITE_LIST = []
    DPP_SOLUTION_WRITE_LIST = []
    IPP_SOLUTION_WRITE_LIST = []
    ASS_SOLUTION_WRITE_LIST = []
    CONS_SOLUTION_WRITE_LIST = []

    SPP_TEST_LIST, DPP_TEST_LIST, ASS_TEST_LIST, CONS_TEST_LIST, IPP_TEST_LIST = [], [], [], [], []

    SUFFIXES = ["ing", ["sion", "tion"], ["ence", "ance"], 'acy', 'al', 'dom', ['er', 'or'], 'ism', 'ist', ['ity', 'ty'], 'ment', 'ness', 'ship', 'ure']


    for suffix in SUFFIXES:
        # spp, dpp = PerfectPairs(suffix)
        spp = singlePerfectPairs(suffix)
        ipp = imperfectPairs(suffix)

        SPP_SOLUTION_WRITE_LIST.extend(spp)
        # DPP_SOLUTION_WRITE_LIST.extend(dpp)
        IPP_SOLUTION_WRITE_LIST.extend(ipp)

        SPP_TEST_LIST.extend([' '.join(list(s.keys())) for s in spp])
        # DPP_TEST_LIST.extend([' '.join(list(d.keys())) for d in dpp])
        IPP_TEST_LIST.extend([' '.join(list(i.keys())) for i in ipp])

    # file_write_strings("/home/aaditd/3_Rhyme/data/english/solutions/singlePerfect.txt", SPP_SOLUTION_WRITE_LIST)
    # file_write_strings("/home/aaditd/3_Rhyme/data/english/solutions/doublePerfect.txt", DPP_SOLUTION_WRITE_LIST)
    # file_write_strings("/home/aaditd/3_Rhyme/data/english/solutions/imperfect.txt", IPP_SOLUTION_WRITE_LIST)

    # file_write_strings("/home/aaditd/3_Rhyme/data/english/test/singlePerfect.txt", SPP_TEST_LIST)
    # file_write_strings("/home/aaditd/3_Rhyme/data/english/test/doublePerfect.txt", DPP_TEST_LIST)
    # file_write_strings("/home/aaditd/3_Rhyme/data/english/test/imperfect.txt", IPP_TEST_LIST)

    # print()
    # print(f"{len(SPP_TEST_LIST)}, Single Perfect pairs")
    # print(f"{len(DPP_TEST_LIST)}, Double Perfect pairs")
    # print(f"{len(IPP_TEST_LIST)}, Imerfect pairs")

    # Write Assonance and Consonance Pairs!
    # ass, cons = SlantPairs()

    # ASS_SOLUTION_WRITE_LIST = ass
    # ASS_TEST_LIST = [' '.join(list(a.keys())) for a in ass]
    # CONS_SOLUTION_WRITE_LIST = cons
    # CONS_TEST_LIST = [' '.join(list(c.keys())) for c in cons]

    # file_write_strings("/home/aaditd/3_Rhyme/data/english/solutions/assonance.txt", ASS_SOLUTION_WRITE_LIST)
    # file_write_strings("/home/aaditd/3_Rhyme/data/english/test/assonance.txt", ASS_TEST_LIST)
    # file_write_strings("/home/aaditd/3_Rhyme/data/english/solutions/consonance.txt", CONS_SOLUTION_WRITE_LIST)
    # file_write_strings("/home/aaditd/3_Rhyme/data/english/test/consonance.txt", CONS_TEST_LIST)

    print("DONE!!")




if __name__ == "__main__":
    main()