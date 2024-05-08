''' Sorry no comments :).
'''
import Goban 
import importlib
import time
from io import StringIO
import sys

def fileorpackage(name):
    if name.endswith(".py"):
        return name[:-3]
    return name

if len(sys.argv) > 2:
    classNames = [fileorpackage(sys.argv[1]), fileorpackage(sys.argv[2])]
elif len(sys.argv) > 1:
    classNames = [fileorpackage(sys.argv[1]), 'myPlayer']
else:
    classNames = ['myPlayer', 'myPlayer']
    
b = Goban.Board()

players = []
player1class = importlib.import_module(classNames[0])
player1 = player1class.myPlayer()
player1.newGame(Goban.Board._BLACK)
players.append(player1)

player2class = importlib.import_module(classNames[1])
player2 = player2class.myPlayer()
player2.newGame(Goban.Board._WHITE)
players.append(player2)

totalTime = [0,0] # total real time for each player
nextplayer = 0
nextplayercolor = Goban.Board._BLACK
nbmoves = 1

wrongmovefrom = 0

while not b.is_game_over():
    legals = b.legal_moves() # legal moves are given as internal (flat) coordinates, not A1, A2, ...
    nbmoves += 1
    otherplayer = (nextplayer + 1) % 2
    othercolor = Goban.Board.flip(nextplayercolor)
    
    move = players[nextplayer].getPlayerMove() # The move must be given by "A1", ... "J8" string coordinates (not as an internal move)

    if not Goban.Board.name_to_flat(move) in legals:
        wrongmovefrom = nextplayercolor
        break
    b.push(Goban.Board.name_to_flat(move)) # Here I have to internally flatten the move to be able to check it.
    players[otherplayer].playOpponentMove(move)
 
    nextplayer = otherplayer
    nextplayercolor = othercolor

result = b.result()
print("Winner: ", end="")
if wrongmovefrom > 0:
    if wrongmovefrom == b._WHITE:
        print("BLACK")
    elif wrongmovefrom == b._BLACK:
        print("WHITE")
    else:
        print("ERROR")
elif result == "1-0":
    print("WHITE")
elif result == "0-1":
    print("BLACK")
else:
    print("DEUCE")

