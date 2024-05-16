# -*- coding: utf-8 -*-
''' This is the file you have to modify for the tournament. Your default AI player must be called by this module, in the
myPlayer class.

Right now, this class contains the copy of the randomPlayer. But you have to change this!
'''
import sys
import time
import Goban 
from random import choice
from playerInterface import *
import numpy as np

def add_tuple(x,y):
    return tuple(map(lambda i, j: i + j, x, y))


class myPlayer(PlayerInterface):
    ''' Example of a random player for the go. The only tricky part is to be able to handle
    the internal representation of moves given by legal_moves() and used by push() and 
    to translate them to the GO-move strings "A1", ..., "J8", "PASS". Easy!

    '''

    def __init__(self):
        self._board = Goban.Board()
        self._mycolor = None
        self._opponent = None
        self._dist_list = []
        self._contour = [(0,0),(-1,0),(1,0),(0,-1),(0,1),(-2,0),(-1,-1),(0,-2),(-1, 1),(1, -1),(0, 2),(1,1),(2,0),(-3,0),(-2,-1),(-1,-2),(0,-3),(-2, 1),(1, -2),(2,-1),(-1,2),(0,3),(1, 2),(2,1),(3,0)]
        self._turn_count = 0
        self._opponent_last_move = "NoMove"


    def initDist(self):
        for i in range(64):
            l = np.zeros(64)
            for j in self._contour:
                v = i + j[0] * 8 + j[1]
                if i//8 + j[0] >= 0 and i//8 + j[0] < 8 and i%8 + j[1] >= 0 and i%8 + j[1] < 8 :
                    l[v] = 16 - 2**(abs(j[0]) + abs(j[1]))
            self._dist_list.append(l)




    def getPlayerName(self):
        return "Random Player"

    def getPlayerMove(self):
        if self._board.is_game_over():
            print("Referee told me to play but the game is over!")
            return "PASS" 
        
        moves = self._board.legal_moves() # Dont use weak_legal_moves() here!
 
        move = 0
        if self._turn_count < 2 :
            if 27 in moves :
                move = 27
            elif 36 in moves :
                move = 36
            
            if self._dist_list == []:
                self.initDist()
        else :
            move = self.play_alphabeta(self._mycolor, 1, -1000000, 1000000, True)

        self._turn_count += 1
        self._board.play_move(move)

        # New here: allows to consider internal representations of moves
        # print("MyplayerZone am playing ", self._board.move_to_str(move), "\n\n\n", file=sys.stderr)
        # print("My current board :")
        # self._board.prettyPrint()
        # move is an internal representation. To communicate with the interface I need to change if to a string
        return Goban.Board.flat_to_name(move) 

    def playOpponentMove(self, move):
        # print("Opponent played ", move) # New here
        # the board needs an internal represetation to push the move.  Not a string
        self._opponent_last_move = move
        self._board.push(Goban.Board.name_to_flat(move)) 

    def newGame(self, color):
        self._mycolor = color
        self._opponent = Goban.Board.flip(color)

    def endGame(self, winner):
        if self._mycolor == winner:
            print("I won!!!")
        else:
            print("I lost :(!!")


    def neighbours(self, index):
        match index:
            case 0:
                return (1, 8)
            case 7:
                return (6, 15)
            case 56:
                return (48, 57)
            case 63:
                return (55, 62)
        if index // 8 == 0:
            return (index-1, index+1, index + 8)
        if index // 8 == 7:
            return (index-1, index+1, index - 8)
        if index % 8 == 0:
            return (index - 8, index + 1, index + 8)
        if index % 8 == 7:
            return (index - 8, index - 1, index + 8)
        return (index - 8, index - 1, index + 1, index + 8)
        


    def heur(self):
        
        score = 0
        # for d in self._dist_list:
        #     # pos = 0
        #     # neg = 0

        #     for j in self._board._board:
        #         if j == self._mycolor:
        #             # pos += 2*d[j]
        #             score += 2*d[j]
        #         elif j != 0:
        #             score = d[j]
                    # neg += d[j]

            # if pos > neg:
            #     score += pos
            # else :
            #     score -= neg
        return -np.count_nonzero(self._board._board == self._opponent)


    def evaluate_board(self, moves):

        my_v = np.zeros(64)
        you_v = np.zeros(64)

        for i in range(64):
            if self._board._board[i] == self._mycolor :
                for j in self.neighbours(i):
                    my_v[j] += 1

            elif self._board._board[i] == self._opponent:
                for j in self.neighbours(i):
                    you_v[j] += 1

        next_move = -1
        op_num = np.count_nonzero(self._board._board == self._opponent)
        for move in moves:
            if you_v[move] > 0 :
                self._board.push(move)
                new_op_num = np.count_nonzero(self._board._board == self._opponent)
                if new_op_num < op_num :
                    op_num = new_op_num
                    next_move = move
                self._board.pop()
        if next_move != -1:
            return next_move

        for i in moves:
            nei = self.neighbours(i)
            for j in nei:
                # l = len(nei)

                # match l:
                #     case 2:
                #         # make eye without taking risk
                #         if my_v[j] == 2 and (you_v[i] != 1 or self._board._board[j] == self._opponent) :
                #             return i
                #     case 3:
                #         # make eye without taking risk
                #         if my_v[j] == 2 and (you_v[i] != 2 or self._board._board[j] == self._opponent):
                #             return i
                #         # protect an eye creation
                #         if you_v[j] == 2 and you_v[i] < 1 and self._board._board[j] != self._opponent:
                #             return i
                #     case 4:
                # make eye without taking risk
                if my_v[j] == 3 and (you_v[i] != 3 or self._board._board[j] == self._opponent):
                    return i
                # protect an eye creation
                if you_v[j] == 3 and you_v[i] != 3 and self._board._board[j] != self._opponent:
                    return i
                # Enclosing a pawn when there are already 2
                if my_v[j] == 2 and you_v[j] == 0 and self._board._board[j] == self._opponent:
                    return i
                
                # Help a solo bro
                # if self._board._board[j] == self._mycolor and my_v[j] == 0 and my_v[i] == 2 and you_v[i] < 2:
                #     return i
        return -1
            


    def play_alphabeta(self, player, depth, alpha, beta, ret_coup = False):
        if depth == 0 or self._board._gameOver:
            return self.heur()

        coup = []
        last_alpha = alpha

        if ret_coup :
            moves = self._board.legal_moves()
            if np.count_nonzero(self._board._board != self._mycolor) >= np.count_nonzero(self._board._board == self._mycolor):
                moves.remove(-1)
                if moves == []:
                    return -1 #If we are forced to PASS
            elif self._opponent_last_move == -1:
                return -1 #If the oppenent PASS and we have advantage
            
            move = self.evaluate_board(moves)
            if move != -1:
                return move

        else :
            moves = self._board.weak_legal_moves()

        for move in moves:

            self._board.push(move)

            if player == self._mycolor:
                alpha = max(alpha, self.play_alphabeta(self._opponent, depth - 1, alpha, beta))
            else :
                beta = min(beta, self.play_alphabeta(self._mycolor, depth - 1, alpha, beta))

            self._board.pop()

            if ret_coup :
                if last_alpha == alpha :
                    coup.append(move)
                else :
                    coup = [move]
                    last_alpha = alpha

            if alpha >= beta : 
                return beta

        if ret_coup :
            return choice(coup)

        if player == self._mycolor:
            return alpha
        else:
            return beta
