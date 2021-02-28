from fbChatter import FbChatter
from interactiveCLI import InteractiveCLI
from game import Game

import argparse
import configparser
import logging

def parseInputs ():
    parser = argparse.ArgumentParser(description=
        """This is a script to play the board game 'Spyfall2' online.
           The roles and locations are randomly chosen and the players are
           informed through Facebook chat messages.
           If no arguments are given, a round of 'Spyfall2' is started.
        """)
    parser.add_argument("-m", nargs=2, metavar=('MESSAGE', 'FRIEND'),
            help="send a facebook MESSAGE (e.g. 'Hello!') to a FRIEND (e.g. 'Tom Anderson')")
    parser.add_argument("-p", "--pretend", action="store_true",
            help="no messages are actually send")
    parser.add_argument("-i", "--interactive", action="store_true",
            help="start interactive mode")
    return parser.parse_args()

def runInteractiveCLI (game):
    runner = InteractiveCLI(game)
    runner.cmdloop()

if __name__ == "__main__":
    logging.basicConfig(filename="game.log", filemode='w', level=logging.INFO)
    logging.info("Started logging")
    args = parseInputs()

    with FbChatter(args.pretend) as chatter:
        game = Game(chatter)
        if args.interactive:
            runInteractiveCLI(game)
        elif args.m:
            chatter.sendMessage(message=args.m[0], name=args.m[1])
        else:
            game.setupNewRound()
