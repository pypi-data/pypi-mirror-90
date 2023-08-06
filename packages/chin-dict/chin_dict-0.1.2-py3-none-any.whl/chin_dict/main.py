# TODO can see traditional/simplified form

from .chindict import ChinDict 
import argparse

parser = argparse.ArgumentParser(description='Lookup character or word')
parser.add_argument('character', type=str, help='Character to search')
group = parser.add_mutually_exclusive_group()
group.add_argument('-w', '--word', action='store_true', help='lookup word')
group.add_argument('-t', '--tree', action='store_true', help='show tree')
group.add_argument('-c', '--comp', action='store_true', help='show components')
group.add_argument('-r', '--rad', action='store_true', help='show components')

args = parser.parse_args()


def main():
        
    cd = ChinDict(charset='simplified')

    print("---------------------------------------------")

    if args.word:
        res = cd.lookup_word(args.character)
        for word in res:
            print(word)
    else:
        res = cd.lookup_char(args.character)

        if args.tree:
            res.tree()
        elif args.comp:
            print(res.components)
        elif args.rad:
            print(res.radical)
        else:
            print("Character:", res.character)
            print("Pinyin:", res.pinyin)
            print("Meaning:", res.meaning)
