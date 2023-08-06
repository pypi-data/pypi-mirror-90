import argparse, traceback, yugioh

parser = argparse.ArgumentParser()
parser.add_argument('-m', '--monster', help="name of monster", required=False)
parser.add_argument('-s', '--spell', help="name of spell", required=False)
parser.add_argument('-t', '--trap', help="name of trap", required=False)
args = parser.parse_args()

def main():
    try:
        if args.monster is not None:
            monster = yugioh.monster(card_name = str(args.monster))
            print(monster.name)
            print(monster.archetype)
            print(monster.atk)
            print(monster.attribute)
            print(monster._def)
            print(monster.desc)
            print(monster.id)
            print(monster.level)
            print(monster.race)
            print(monster.type)
        if args.spell is not None:
            spell = yugioh.spell(card_name = str(args.spell))
            print(spell.desc)
            print(spell.id)
            print(spell.name)
            print(spell.type)
            print(spell.race)
        if args.trap is not None:
            spell = yugioh.spell(card_name = str(args.trap))
            print(spell.desc)
            print(spell.id)
            print(spell.name)
            print(spell.type)
            print(spell.race)
    except Exception:
        print(traceback.format_exc())
