#!/usr/bin/env python

import argparse
import os.path

# --------------------------------------------------
def get_args():

    parser = argparse.ArgumentParser(
        description='Collapse vowels in a word',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('input',
                        metavar='text',
                        help='A word')

    parser.add_argument('-v',
                        '--vowel',type=str,
                        help='The vowel to substitute',
                        default='a',choices=list('aiueo'))
    
    args = parser.parse_args()

    if os.path.isfile(args.input):
        args.input = open(args.input).read().rstrip()
    return args

# -------------------------------------------------- 
def main():

    args = get_args()
    vowel = args.vowel

    new_word_list = [vowel if c in 'aiueo' else vowel.upper() if c in 'AIUEO' else c for c in args.input]

    def collapse_vowels(new_word):
        final_word = set()
        return ''.join([x for x in new_word if not (x in final_word or final_word.add(x))])
    
    print(collapse_vowels(''.join(new_word_list)))

# --------------------------------------------------
if __name__ == '__main__':
    main()

"""
Output:
$ ./collapse_adjacent_vowels.py quiick -v a
qack
$ ./collapse_adjacent_vowels.py boat -v o
bot
"""
