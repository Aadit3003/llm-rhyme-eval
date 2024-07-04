""" This module is used to create the English Rhyming dataset
from the CMU Pronunciation dictionary.

The output for each of the five rhyme types is stored in 
the corresponding directories in data/english/solutions/ and data/english/test/
"""

import random
import re

from utils import write_clean_file, file_read_strings
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
def populate_dictionary(file: str):
    """
    Returns a dictionary of the form:-
    {
        word: [phoneme, phoneme2, ..., phoneme7],
        word2: [phoneme, phoneme2, ..., phoneme7],
        word3: [phoneme, phoneme2, ..., phoneme7],
    }
    
    Used to create a global Python dictionary that is used by all 
    subsequent rhyme pair detection functions.
    
    file: The path to CMU-Dict, where each line corresponds to one word 
        and is of the form "<Orthographic rep> <Phonemic rep>"
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

def find_words(suffix: str) -> list[str]:
    """
    Returns a list of words from the pronunciation dictionary ending in a particular suffix.
    """
    
    global PRON_DICTIONARY
    all_words = list(PRON_DICTIONARY.keys())
    word_list = [a for a in all_words if suffix in a]

    

    return word_list               

def product(*args):
    """
    Takes a variable number of lists and returns a cartesian product (usually pair) of each element 
    from every list.
    
    Used to find alliteration pairs, where each argument is a list of words
    that have the same initial consonant, and initial vowel, but no two arguments
    may have the same vowel.
    
    E.g. [butter, bust], [bark, barn] -> [(butter, bark), (butter, barn), (bust, bark), (bust, barn)]
    
    """
    if not args:
        return iter(((),)) # yield tuple()
    return (items + (item,) 
            for items in product(*args[:-1]) for item in args[-1])

# SYLLABLE FUNCTIONS

def get_vowels_consonants(word: str):
    """
    word: An input word
    
    Returns three lists of vowels, consonants, and phoneme information. 
    Used to find Assonance, Consonance pairs, and perfect rhymes.
    
    vc: A list of tuples of the form:- ((phone, stress,), category) for vowels and (phone, category) for consonants
            category: "v"/"c"
    vowels: A list of the vowel phonemes in the word
    consonants: A list of the consonant phonemes in the word
    """
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

def len_symbol_overlap(symbol_set_1, symbol_set_2) -> int:
    """
    Given two sets of symbols, determines how many are shared between the two.
    
    Used in find assonance pairs that have zero consonantal overlap.
    Used to find consonance pairs that have zero vowel overlap.
    Used to find non-rhyming pairs that have less than 2 vowel and consonant overlap.
    """
    symbol_set_1 = set(symbol_set_1.split(" "))
    symbol_set_2 = set(symbol_set_2.split(" "))

    overlap = symbol_set_1.intersection(symbol_set_2)
    # if len(overlap) == 2:
    # if len(overlap) == 0: print(f"OVERLAP:  {overlap}   WORD1: {consSet1}   WORD2: {consSet2}")
    # print(f"")
    return len(overlap)

def find_primary_stressed_syllable(vc):
    """
    Finds the primary stressed syllable, and returns the onset, remaining word, and the type of stress.
    Used to find single and double perfect rhyming word pairs.


    Args:
        vc: A list of tuples of the form:- ((phone, stress,), category) for vowels and (phone, category) for consonants
            category: "v"/"c"

    Returns:
        onset: A tuple of the form (phone, category), corresponding to the onset of the syllable.
        remaining: A list of tuple of the same type as vc, excluding the onset
        type: The type of stress (initial/final/penultimate)
        
        
    Recall, for a syllable like rap, 
        onset: r
        rhyme: ap
            nucleus: a
            coda: p
    """
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
        type = "initial"
    elif stresses[-1] == "1":
        type = "final"
    elif stresses[-2] == "1":
        type = "penultimate"
    else:
        type = "other"

    
    return (onset, remaining, type)

def find_last_syllable(vc):
    """
    Finds the nucleus and coda of the final syllable in a word. 
    
    vc: A list of tuples of the form:- ((phone, stress,), category) for vowels and (phone, category) for consonants
            category: "v"/"c"

    Returns:
        nucleus: A tuple of the form (vowel, stress)
        coda: A list of tuples of the same type as vc, excluding the nucleus
    """

    categories = ''.join([type for vowel, type in vc])
    lastVowelIndex = categories.rindex("v")

    nucleus = vc[lastVowelIndex]
    coda = vc[lastVowelIndex+1:]
    

    
    return (nucleus, coda)



# RHYME FUNCTIONS

def single_perfect_pairs(suffixes, outerLimit = 300, comparisonLimit = 300, lengthLimit = 500):
    """
    A function to find Single Perfect rhyming pairs: 
    Words with final stress, that are identical after the stressed vowel (Different onset, but same nucleus and coda)
    
    suffixes: A list of suffixes to check for rhyming pairs
    outerLimit: Max Number of words (ending in this suffix) to consider as "current word!"
    comparisonLimit: Max number of other words to compare to the current word
    lengthLimit: Desired no. of single perfect pairs!
    
    Returns a list of dictionaries, where each dictionary has two keys corresponding to the rhyme pair.
    Each key corresponds to a value, which is simply the word's phonemic representation from the global
    pronunciation dictionary.
    """
    single_perfect_pairs = []

    candidate_words = []

    if type(suffixes) == 'str':
        candidate_words = find_words(suffixes)
    else:
        for suffix in suffixes:
            candidate_words.extend(find_words(suffix))
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
            vc_current, _, _ = get_vowels_consonants(current_word)
            vc_other, _, _ = get_vowels_consonants(other_word)

            onset_current, remaining_current, type_cur = find_primary_stressed_syllable(vc_current)
            onset_other, remaining_other, type_oth = find_primary_stressed_syllable(vc_other)


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

def double_perfect_pairs(suffixes, outerLimit = 100, comparisonLimit = 100, lengthLimit = 1000):
    """
    A function to find Double Perfect rhyming pairs: 
    Words with penultimate stress, that are identical after the stressed vowel (Different onset, but same remaining phonemes)
    
    suffixes: A list of suffixes to check for rhyming pairs
    outerLimit: Max Number of words (ending in this suffix) to consider as "current word!"
    comparisonLimit: Max number of other words to compare to the current word
    lengthLimit: Desired no. of single perfect pairs!
    
    Returns a list of dictionaries, where each dictionary has two keys corresponding to the rhyme pair.
    Each key corresponds to a value, which is simply the word's phonemic representation from the global
    pronunciation dictionary.
    """
    double_perfect_pairs = []

    candidate_words = []

    if type(suffixes) == 'str':
        candidate_words = find_words(suffixes)
    else:
        for suffix in suffixes:
            candidate_words.extend(find_words(suffix))
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
            vc_current, _, _ = get_vowels_consonants(current_word)
            vc_other, _, _ = get_vowels_consonants(other_word)

            onset_current, remaining_current, type_cur = find_primary_stressed_syllable(vc_current)
            onset_other, remaining_other, type_oth = find_primary_stressed_syllable(vc_other)


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

def assonance_pairs(innerLimit = 5, outerLimit = 1000):
    """
    A function to find Assonance pairs: 
    Words with identical vowels, but no common consonants
    
    innerLimit: The number of entries from the same vowel configuration
    outerLimit: The total number of assonance Pairs!
    
    Returns a list of dictionaries, where each dictionary has two keys corresponding to the rhyme pair.
    Each key corresponds to a value, which is simply the word's phonemic representation from the global
    pronunciation dictionary.
    """
    all_words = list(PRON_DICTIONARY.keys())

    assonancePairs = []
    VOW_MAP = {}
    i = 0
    random.shuffle(all_words)
    # Populate Vowel and Consonant Maps (All seen combinations!)
    for word in all_words:
        _, vowels, consonants = get_vowels_consonants(word)
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
                    if len_symbol_overlap(current_cons, other_cons) == 0:
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

def consonance_pairs(innerLimit = 5, outerLimit = 1000):
    """
    A function to find Consonant: 
    Words with the same sequence of consonants, but completely different vowels
    
    innerLimit: The number of entries from the same consonant configuration
    outerLimit: The total number of assonance Pairs!
    
    Returns a list of dictionaries, where each dictionary has two keys corresponding to the rhyme pair.
    Each key corresponds to a value, which is simply the word's phonemic representation from the global
    pronunciation dictionary.
    """
    all_words = list(PRON_DICTIONARY.keys())

    consonancePairs = []

    CONS_MAP = {}
    i = 0
    random.shuffle(all_words)
    # Populate Vowel and Consonant Maps (All seen combinations!)
    for word in all_words:
        _, vowels, consonants = get_vowels_consonants(word)
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
                    if len_symbol_overlap(current_vows, other_vows) == 0:
                        consonancePairs.append({
                            current_word: PRON_DICTIONARY[current_word],
                            other_word: PRON_DICTIONARY[other_word]
                        })
            
                        if len(consonancePairs) > outerLimit: 
                            return consonancePairs


    return consonancePairs

def alliterative_pairs(perConsLimit = 100, lengthLimit = 1000):
    """
    A function to find Alliterative rhyming pairs: 
    Words with initial stress, the same initial consonant (onset), but different stressed vowels.
    
    innerLimit: The number of entries from the same vowel configuration
    outerLimit: The total number of assonance Pairs!
    
    Returns a list of dictionaries, where each dictionary has two keys corresponding to the rhyme pair.
    Each key corresponds to a value, which is simply the word's phonemic representation from the global
    pronunciation dictionary.
    """
    
    # Match Initial Consonant
    # Match Number of Vowels
    # Initial Stress (but different vowels)
    
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
                vc, _, _ = get_vowels_consonants(word)
                
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


def perfect_pairs(suffixes):
    """
    Returns Single and Double perfect rhyming pairs given a list of suffixes to match words against
    """
    return single_perfect_pairs(suffixes), double_perfect_pairs(suffixes)

def slant_pairs():
    """
    Returns Assonance and Consonance pairs.
    """
    return assonance_pairs(), consonance_pairs()

def non_rhyming_pairs(patternLimit = 10, comparisonLimit = 20, lengthLimit = 1000):
    """
    A function to find Non-Rhyming pairs: 
    Words with zero vowel overlap and zero consonantal overlap.
    
    patternLimit: The Max number of consonant patterns to iterate over while searching for disjoint consonant sets.
    comparisonLimit: Max number of other words to compare to the current word
    lengthLimit: Desired no. of single perfect pairs!
    
    Returns a list of dictionaries, where each dictionary has two keys corresponding to the rhyme pair.
    Each key corresponds to a value, which is simply the word's phonemic representation from the global
    pronunciation dictionary.
    """
    # Zero vowel overlap
    # Zero Consonantal overlap
    all_words = list(PRON_DICTIONARY.keys())

    non_rhyming_pairs = []

    CONS_MAP = {}
    i = 0
    random.shuffle(all_words)
    # Populate Vowel and Consonant Maps (All seen combinations!)
    for word in all_words:
        _, vowels, consonants = get_vowels_consonants(word)
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
            if len_symbol_overlap(current_pattern, other_pattern) <= 2:

                current_word_list = CONS_MAP[current_pattern]
                other_word_list = CONS_MAP[other_pattern]


                for cw in current_word_list:
                    c_word, c_vowels = cw
                    count = 0
                    for ow in other_word_list:

                        count += 1
                        if count > comparisonLimit: break

                        o_word, o_vowels = ow
                        if len_symbol_overlap(c_vowels, o_vowels) == 0:
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
    filename = "/home/aaditd/3_Rhyming/llm-rhyme/cmudict-0.7b"
    populate_dictionary(filename)

    
    SPP_SOLUTION_WRITE_LIST = []
    DPP_SOLUTION_WRITE_LIST = []

    SUFFIXES = ["ing", ["sion", "tion"], ["ence", "ance"], 'acy', \
                'al', 'dom', ['er', 'or'], 'ism', 'ist', ['ity', 'ty'], \
                'ment', 'ness', 'ship', 'ure', ['ery', 'ary'], 'age', ['ant', 'ent'], \
                ['air', 'are'], ['eel', 'ill', 'eal', 'ial'], ['ch', 'tch'], \
                'op', 'ept', 'ed', 'ect', 'ept']

    random.shuffle(SUFFIXES)
    
    # Populate the different data files
    for suffix in SUFFIXES:
        if suffix in [['air', 'are'],'op', 'ept', 'ed', 'ect', 'ept', ['eel', 'ill', 'eal', 'ial']]:
            lim = 500
        else:
            lim = 200
        spp = single_perfect_pairs(suffix, lim, lim, 1000)
        dpp = double_perfect_pairs(suffix, 500, 500, 1000)

        SPP_SOLUTION_WRITE_LIST.extend(spp)
        DPP_SOLUTION_WRITE_LIST.extend(dpp)

    write_clean_file("data/english/solutions/singlePerfect.txt", 
                     "data/english/test/singlePerfect.txt",
                     SPP_SOLUTION_WRITE_LIST)
    
    write_clean_file("data/english/solutions/doublePerfect.txt", 
                     "data/english/test/doublePerfect.txt",
                     DPP_SOLUTION_WRITE_LIST)

    ass, cons = slant_pairs()
    write_clean_file("data/english/solutions/assonance.txt",
                     "data/english/test/assonance.txt",
                     ass)
    
    write_clean_file("data/english/solutions/consonance.txt",
                     "data/english/test/consonance.txt",
                     cons)

    allit = alliterative_pairs(1000)
    write_clean_file("data/english/solutions/alliterative.txt",
                     "data/english/test/alliterative.txt",
                     allit)

    nons = non_rhyming_pairs(100, 20, 5000)
    write_clean_file("data/english/solutions/non.txt",
                     "data/english/test/non.txt",
                     nons, 5000)

    print("DONE!!")


if __name__ == "__main__":
    main()