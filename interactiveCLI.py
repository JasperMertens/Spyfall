import cmd
import time
from threading import Thread
from common import loadConfig
import logging

class Timer ():

    def __init__ (self):
        self.seconds = self.getStartTime()
        self.thread = None
        self.running = False

    def run (self):
        while (self.running and self.seconds >= 0):
            self.countDown()
            self.logTime()

    def countDown (self):
        time.sleep(1)
        self.seconds = max(0, self.seconds-1)

    def getStartTime (self):
        return int(loadConfig()['Timer']['duration'])

    def getTime (self):
        return "{:02d}m {:02d}s".format(self.seconds // 60, self.seconds % 60)

    def logTime (self):
        with open('timer.log', 'w') as f:
            f.write(self.getTime() + "\n")

    def start (self):
        self.seconds = self.getStartTime()
        self.resume()

    def stop (self):
        self.running = False
        msg = "Timer stopped at ", self.getTime()
        logging.info(msg)
        print(msg)

    def pause (self):
        self.running = False
        msg = "Timer paused at ", self.getTime()
        logging.info(msg)
        print(msg)

    def resume (self):
        if (not self.running):
            self.thread = Thread(target=self.run)
            self.running = True
            self.thread.start()
            logging.info("Timer running")
            print("Timer running")


class InteractiveCLI(cmd.Cmd):

    def __init__ (self, game):
        super(InteractiveCLI, self).__init__()
        self.game = game
        self.timer = Timer()

    intro = "A Spyfall game is ready to be started! Type help or ? to list commands.\n"
    prompt = ">>> "
    
    def do_timer (self, cmd):
        "The commands 'timer start|stop|pause|resume' control the timer."
        if (cmd == "start"):
            self.timer.start()
        elif (cmd == "stop"):
            self.timer.stop()
        elif (cmd == "pause"):
            self.timer.pause()
        elif (cmd == "resume"):
            self.timer.resume()
        else:
            print("Invalid argument")

    def do_round (self, cmd):
        "The command 'round start' starts a new round, sending messages to all players."
        if (cmd == "start"):
            self.game.setupNewRound()
        else:
            print("Invalid argument")

    def do_quit (self, s):
        "Exit this program."
        self.timer.stop()
        return True
