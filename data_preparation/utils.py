""" This module contains useful functions that read and write strings from/to files
"""


import os
import re
import random


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


def write_clean_file(solution_filename, test_filename, lines, limit=1000):

    solution_list = lines
    test_list = [' '.join(list(a.keys())) for a in solution_list]
    
    blacklist = set('()0123456789')
    new_test_list = [''.join(c for c in line if c not in blacklist) for line in test_list]
    
    ziploc = list(zip(solution_list, new_test_list))
    random.shuffle(ziploc)
    
    solution_list, new_test_list = zip(*ziploc)
    new_test_list = new_test_list[0:limit]
    solution_list = solution_list[0:limit]

    file_write_strings(solution_filename, solution_list)
    file_write_strings(test_filename, new_test_list)
    print(f"File: {test_filename} cleaned up!" )


def main():
    a = 0


# if __name__ == "__main__":
#     # clean_file("try.txt")
#     path = "/home/aaditd/3_Rhyming/llm-rhyme/data/english/test/"
#     test_files = os.listdir(path)
#     # test_files = [t fo t in test_files if t != "singlePerfect.txt"]
#     print(test_files)

#     for file in test_files:
#         write_clean_file(path + file)



"""
edan nettie
poteet onto(1)
meisch diemer
spinal demeree
yuichi man-made
dayne odom
gasich duve
grave swoope
into reliance
co-worker seif
durn masch
marielito seff
musher ossify
dooner sweep
baucum duve
gaska grove
predisposition ribald
apatite onto
dehmer nieto(1)
cork hoepfner(1)
mersch knight
soon assaf
dave mish
texts croquet
mesch kwik
biochem man-made
dooner moesch
sohn edam
karraker damme
deny demme
diona hapner
dane nieto(1)
sweep quick
corker damn
flabbergast yoichi
chirico ribald
baucum seff
dohn manmade
dum heppner
gaska hoepner
marlette recurrence(1)
sana into(1)
suny hapner
kroeker humiliate
donne quik
baucum dawn
predisposition musher
dive sweeper
yoichi normandin
marielito beckum
beckom deemer
greever misch
deener mersch
gurski bargain(1)
karriker onto
dione dimaio
pertuit bargeron
garvie espinal
bahama mush
serino humiliate
doyon mish
dannie moishe
mush hapner
groove durn
choric sweep
mish toyota
deaner spinal
beacom suffer
gasca diemer
creek co-worker
texts potpourris
brueggen creek
burham choric
choric nettie
crack nite
brueggen krakower
dam anette
carrick durn
petito dahn(1)
abramovitz seife
sweeper dama
mattea sophy
micheaux onto
diener serf
garvie footnotes
hoepfner(1) manmade
borgen knight
crack dime
"""