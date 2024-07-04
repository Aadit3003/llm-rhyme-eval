""" This module was used to create Aadit's Dutch Pronunciation dictionary 
in the same format as the CMU Pronunciation dictionary. 

The final dictionary contains 349K pairs of orthographic and phonemic representations of Dutch words.
"""

import random

from utils import write_clean_file, file_read_strings, file_write_strings


PHON_PATH = "../celex2/dutch/dpw/dpw.cd"
STRESS_PATH = "../celex2/dutch/dpw/stress.txt"
DICTIONARY_PATH = "../aadit's-dutch-dict"

SILLZ_PATH = "../celex2/dutch/dpw/brackets_sillz.txt"
TIPZ_PATH = "../celex2/dutch/dpw/brackets_tipz.txt"

random.seed(2)
first_n = len(file_read_strings(PHON_PATH))

ziploc = list(zip(file_read_strings(PHON_PATH), 
                  file_read_strings(STRESS_PATH),
                  file_read_strings(SILLZ_PATH),
                  file_read_strings(TIPZ_PATH)))


# Lists of Strings mined from Celex2 (Dutch Pronunciation Dictionary)
pack_strings, stress_strings, sillz_strings, tipz_strings = zip(*ziploc)
pack_strings = pack_strings[0 : first_n] # The entire string containing information about spelling, vowels/consonants, stresses, phonemes etc.
stress_strings = stress_strings[0 : first_n] # Stresses based on syllables (1 - Primary stress, 0 - No stress)

sillz_strings = sillz_strings[0 : first_n] # Syllables
tipz_strings = tipz_strings[0 : first_n] # Types (Consonants/Vowels C/V)




banned_indices = [i for i in range(len(sillz_strings)) if sillz_strings[i] == ""]
banned_indices = [i for i in range(len(sillz_strings)) if len(sillz_strings[i].split(" ")) > 1]

total = len(pack_strings)
# print(total)

pack_strings = [pack_strings[i] for i in range(total) if i not in banned_indices]
stress_strings = [stress_strings[i] for i in range(total) if i not in banned_indices]
sillz_strings = [sillz_strings[i] for i in range(total) if i not in banned_indices]
tipz_strings = [tipz_strings[i] for i in range(total) if i not in banned_indices]

total = len(pack_strings)
# print(total)

SYMBOLS = {
    "VOWELS": set(),
    "CONSONANTS": set()
}

def add_types(sillz: str, catz: str, stresses: str) -> str:
    """
    For a single word, given its syllables, vowel/consonant categories, and 
    stress markers, return a string of the phonemic representation with stress. 
    Additionally, add new symbols to the dictionary.

    sillz: The syllables for a word separated by "-" E.g. "krimi-na" 
    catz: The vowels and consonant categories of each phoneme 
        (same number of characters and "_" as sillz) E.g. "CCVCV-CV"
    stresses: The stress on each syllable (Same number as characters as no. of syllables) E.g. "10"
    """

    count = 0
    write_list = []

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


def remove_slashes(index):
    """
    For a single index in Celex2's list of Dutch words, 
    return a string of the format <Orthographic Spelling> <Phonemic Symbols with Stresses>

    For e.g. an output could be: "aaiend a1 j @0 n t"
    """
    i = index
    print(i)
    pack, stress, sillz, tipz = pack_strings[i], stress_strings[i], sillz_strings[i], tipz_strings[i]

    tokens = pack.split("\\")
    _, spelling, _, _, _, _, _  = tokens
    
    
    sillz = sillz.replace('\'', '')
    tipz = tipz.replace('VV', 'V')

    # Convert Syllables and Vowels to a string with Phonemic symbols and Stress Markers
    value = add_types(sillz, tipz, stress)

    write_string = f"{spelling} {value}"
    return write_string


def main():

    # For Debugging functions
    # print(add_types(sillz = "krimi-na", catz = "CCVCV-CV", stresses = "10"))
    # print(remove_slashes(index = 5507))
    
    # For constructing Aadit's Dutch dictionary
    WS = [remove_slashes(i) for i in range(total)]

    print(f"Started with {first_n}, but only {len(WS)} survived!")
    for ws in WS:
        print(ws)

    file_write_strings(DICTIONARY_PATH, WS)

    print()
    print()
    print(SYMBOLS)
    
if __name__ == "__main__":
    main()