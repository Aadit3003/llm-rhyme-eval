""" This module is used to create the Dutch Rhyming dataset
from the Aadit's Dutch Pronunciation dictionary created using
create_aadit's_dutch_dict.py.

The output for each of the five rhyme types is stored in 
the corresponding directories in data/dutch/solutions/ and data/dutch/test/
"""


import re
import random

from utils import write_clean_file, file_read_strings
from scrape_cmu_dict import populate_dictionary, find_words, product, get_vowels_consonants, len_symbol_overlap, find_primary_stressed_syllable, find_last_syllable
from scrape_cmu_dict import single_perfect_pairs, double_perfect_pairs, assonance_pairs, consonance_pairs, alliterative_pairs, perfect_pairs, slant_pairs, non_rhyming_pairs
# random.seed(2)

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

# Celex2 Constants
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



# MAIN
def main():
    filename = "/home/aaditd/3_Rhyming/llm-rhyme/aadit's-dutch-dict"
    populate_dictionary(filename)

    
    SPP_SOLUTION_WRITE_LIST = []
    DPP_SOLUTION_WRITE_LIST = []

    SUFFIXES = [["en", "eren", "heden", "mannen", "mensen", "vrouwen"], "ert", \
                "weg", ["pjes", "tjes"], "schap", "e", "dom", "'s", 'nde', \
                'ling', 'opt', ['iere', 'ieren'], 'its', 'eer', 'ouw', 'aat', ['ant', 'and']
                    ]

    random.shuffle(SUFFIXES)
    
    # Populate the different data files
    for suffix in SUFFIXES:
        lim = 500

        if suffix in ['opt', 'its', 'eer', 'ouw', 'uik', 'aat', ['ant', 'and']]:
            lim = 1000
        

        spp = single_perfect_pairs(suffix, lim, lim, 1000)
        dpp = double_perfect_pairs(suffix, lim, lim, 1000)

        SPP_SOLUTION_WRITE_LIST.extend(spp)
        DPP_SOLUTION_WRITE_LIST.extend(dpp)

    write_clean_file("data/dutch/solutions/singlePerfect.txt", 
                     "data/dutch/test/singlePerfect.txt",
                     SPP_SOLUTION_WRITE_LIST)
    
    write_clean_file("data/dutch/solutions/doublePerfect.txt", 
                     "data/dutch/test/doublePerfect.txt",
                     DPP_SOLUTION_WRITE_LIST)

    ass, cons = slant_pairs()
    write_clean_file("data/dutch/solutions/assonance.txt",
                     "data/dutch/test/assonance.txt",
                     ass)
    
    write_clean_file("data/dutch/solutions/consonance.txt",
                     "data/dutch/test/consonance.txt",
                     cons)

    allit = alliterative_pairs(1000)
    write_clean_file("data/dutch/solutions/alliterative.txt",
                     "data/dutch/test/alliterative.txt",
                     allit)

    nons = non_rhyming_pairs(100, 20, 5000)
    write_clean_file("data/dutch/solutions/non.txt",
                     "data/dutch/test/non.txt",
                     nons, 5000)

    print("DONE!!")




if __name__ == "__main__":
    main()