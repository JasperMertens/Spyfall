# Spyfall

This is a script to play the board game 'Spyfall2' online.
The roles and locations are randomly chosen and the players are
informed through Facebook chat messages.

## Setup
- The module *fbchat* is required. Use `$ sudo pip install fbchat` to install it.

- You need to replace the default values in the configuration file *config.ini*
  with the values that are appropriate to you.
  These fields that need to be replaced are: 
 	1. player names
	2. username
	3. user agent
  The meaning of the fields is explained in the configuration file.

## Usage
run `$ python main.py -h` to see usage information for the possible arguments.
If no arguments are given, a round of 'spyfall' is started.

In a separate terminal, the command `watch -n1 timer.log` can be used to inspect
the countdown timer value. The 'timer.log' file is only created once the timer
has been started.

### Example
`$ python main.py -i`
`>>> round start`
`>>> timer start`
`quit`

## References
An image of the different locations can be found
[here](http://www.jumpingturtlegames.be/images/spellen/spyfall2-locaties.png) and
[this](https://world-of-board-games.com.sg/docs/Spyfall2.pdf)
also includes an explanation of the rules.
