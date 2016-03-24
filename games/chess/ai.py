# This is where you build your AI for the Chess game.

from joueur.base_ai import BaseAI
from copy import deepcopy
import random

class AI(BaseAI):
    """ The basic AI functions that are the same between games. """

    def get_name(self):
        """ This is the name you send to the server so your AI will control the player named this string.
        Returns
            str: The name of your Player.
        """
        return "Checkers"


    def start(self):
        """ This is called once the game starts and your AI knows its playerID and game. You can initialize your AI here.
        """
        # initialize gameboard dict with my pieces
        for piece in self.game.pieces:
            self.game.board[piece.file][piece.rank] = piece


    def game_updated(self):
        """ This is called every time the game's state updates, so if you are tracking anything you can update it here.
        """
        if self.game.moves:
            oldFile = self.game.moves[-1].from_file
            oldRank = self.game.moves[-1].from_rank
            newFile = self.game.moves[-1].to_file
            newRank = self.game.moves[-1].to_rank
            self.game.board[oldFile][oldRank] = 0
            self.game.board[newFile][newRank] = self.game.moves[-1].piece



    def end(self, won, reason):
        """ This is called when the game ends, you can clean up your data and dump files here if need be.

        Args:
            won (bool): True means you won, False means you lost.
            reason (str): The human readable string explaining why you won or lost.
        """
        # replace with your end logic

    def promote_pawn(self, rank):
        promote_options = ["Queen", "Bishop", "Knight", "Rook"]
        if rank == 1 or rank == 8:
            return random.choice(promote_options)
        else:
            return ""

    def check_pawn(self, oldFile, oldRank, newFile, newRank, player, game_board):
        if abs(oldRank - newRank) == 1:
            if game_board[oldFile][oldRank + player.rank_direction] == 0 and\
                    1 <= newRank <= 8 and oldFile == newFile:
                return True
            elif 1 <= newRank <= 8 and oldFile != newFile and\
                    game_board[newFile][oldRank + player.rank_direction] != 0:
                if game_board[newFile][oldRank + player.rank_direction].owner != player:
                    return True
        elif abs(oldRank - newRank) == 2:
            if game_board[oldFile][oldRank + player.rank_direction] == 0 and\
                            game_board[oldFile][oldRank + player.rank_direction * 2] == 0:
                return True
        return False

    def pawnmoves(self, pawn, player, game_board):
        move_list = []
        if not pawn.has_moved:  # start move
            randomRank = pawn.rank + player.rank_direction * 2
            if self.check_pawn(pawn.file, pawn.rank, pawn.file, randomRank, player, game_board):
                move_list.append((pawn, pawn.file, randomRank, ""))

        # move 1 forward
        randomRank = pawn.rank + player.rank_direction
        if self.check_pawn(pawn.file, pawn.rank, pawn.file, randomRank, player, game_board):
            move_list.append((pawn, pawn.file, randomRank, self.promote_pawn(randomRank)))

        randomRank = pawn.rank + player.rank_direction
        if ord(pawn.file) - 1 >= 97:  # left diagonal
            if self.check_pawn(pawn.file, pawn.rank, chr(ord(pawn.file) - 1), randomRank, player, game_board):
                move_list.append((pawn, chr(ord(pawn.file) - 1), randomRank, self.promote_pawn(randomRank)))
        elif ord(pawn.file) + 1 <= 104:  # right diagonal
            if self.check_pawn(pawn.file, pawn.rank, chr(ord(pawn.file) + 1), randomRank, player, game_board):
                move_list.append((pawn, chr(ord(pawn.file) + 1), randomRank, self.promote_pawn(randomRank)))
        return move_list

    def rookmoves(self, rook, player, game_board):
        move_list = []
        possible_moves = [(1, 0), (0, 1), (-1, 0), (0, -1)]

        for file, rank in possible_moves:
            run_file = file
            run_rank = rank
            while 1 <= rook.rank + run_rank <= 8 and 97 <= ord(rook.file) + run_file <= 104 and\
                    game_board[chr(ord(rook.file) + run_file)][rook.rank + run_rank] == 0:
                move_list.append((rook, chr(ord(rook.file) + run_file), rook.rank + run_rank))
                run_file += run_file
                run_rank += run_rank
            else:
                if 1 <= rook.rank + run_rank <= 8 and 97 <= ord(rook.file) + run_file <= 104 and\
                        game_board[chr(ord(rook.file) + run_file)][rook.rank + run_rank].owner != player:
                    move_list.append((rook, chr(ord(rook.file) + run_file), rook.rank + run_rank))

        return move_list

    def knightmoves(self, knight, player, game_board):
        move_list = []
        possible_moves = [(1, 2), (-1, 2), (1, -2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1)]

        for file, rank in possible_moves:
            if (1 <= knight.rank + rank <= 8 and 97 <= ord(knight.file) + file <= 104) and\
                    (game_board[chr(ord(knight.file) + file)][knight.rank + rank] == 0 or
                     game_board[chr(ord(knight.file) + file)][knight.rank + rank].owner != player):
                move_list.append((knight, chr(ord(knight.file) + file), knight.rank + rank))

        return move_list

    def bishopmoves(self, bishop, player, game_board):
        move_list = []
        possible_moves = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

        for file, rank in possible_moves:
            run_file = file
            run_rank = rank
            while 1 <= bishop.rank + run_rank <= 8 and 97 <= ord(bishop.file) + run_file <= 104 and \
                    game_board[chr(ord(bishop.file) + run_file)][bishop.rank + run_rank] == 0:
                move_list.append((bishop, chr(ord(bishop.file) + run_file), bishop.rank + run_rank))
                run_file += run_file
                run_rank += run_rank
            else:
                if 1 <= bishop.rank + run_rank <= 8 and 97 <= ord(bishop.file) + run_file <= 104 and \
                        game_board[chr(ord(bishop.file) + run_file)][bishop.rank + run_rank].owner != player:
                    move_list.append((bishop, chr(ord(bishop.file) + run_file), bishop.rank + run_rank))

        return move_list

    def queenmoves(self, queen, player, game_board):
        move_list = []
        move_list += self.rookmoves(queen, player, game_board)
        move_list += self.bishopmoves(queen, player, game_board)
        return move_list

    def kingmoves(self, king, player, game_board):
        move_list = []
        possible_moves = [(1, 0), (0, 1), (1, 1), (1, -1), (-1, 0), (0, -1), (-1, -1), (-1, 1)]

        for file, rank in possible_moves:
            if 1 <= king.rank + rank <= 8 and 97 <= ord(king.file) + file <= 104 and\
                    (game_board[chr(ord(king.file) + file)][king.rank + rank] == 0 or
                     game_board[chr(ord(king.file) + file)][king.rank + rank].owner != player):
                move_list.append((king, chr(ord(king.file) + file), king.rank + rank))

        return move_list

    def piece_value(self, game_board, move):
        piece = game_board[move[1]][move[2]]
        if piece != 0:
            if piece.type == "Pawn":
                return 1
            elif piece.type == "Knight":
                return 3
            elif piece.type == "Bishop":
                return 3
            elif piece.type == "Rook":
                return 5
            elif piece.type == "Queen":
                return 9
            elif piece.type == "King":
                return 20
        else:
            return 0

    def alter_board(self, game_board, move):
        board = game_board
        game_board[move[0].file][move[0].rank] == 0
        game_board[move[1]][move[2]] = move[0]
        return board

    def minimax(self, game_board):
        move_list = self.retrieve_moves(self.player, game_board)
        best_move = random.choice(move_list)
        best_score = float("-inf")
        for move in move_list:
            new_board = deepcopy(self.alter_board(game_board, move))
            score = self.min_play(new_board, self.player.other_player)
            if score > best_score:
                best_move = move
                best_score = score

        return best_move

    def min_play(self, game_board, player):
        # implement game over state
        moves = self.retrieve_moves(player, game_board)
        best_move = random.choice(moves)
        best_score = float('inf')
        for move in moves:
            new_board = deepcopy(self.alter_board(game_board, move))
            score = self.max_play(new_board, player)
            if score < best_score:
                best_move = move
                best_score = score
        return best_score

    def max_play(self, game_board, player):
        # implement game over state
        moves = self.retrieve_moves(player, game_board)
        best_score = float('-inf')
        for move in moves:
            score = self.piece_value(game_board, move)
            if score > best_score:
                best_score = score
        return best_score


    def retrieve_moves(self, player, game_board):
        move_list = []
        pieces = {"Pawn": [], "Knight": [], "Rook": [], "Bishop": [], "Queen": [], "King": []}

        for piece in player.pieces:
            pieces[piece.type].append(piece)

        for pawn in pieces["Pawn"]:
            move_list += self.pawnmoves(pawn, player, game_board)
        for knight in pieces["Knight"]:
            move_list += self.knightmoves(knight, player, game_board)
        for rook in pieces["Rook"]:
            move_list += self.rookmoves(rook, player, game_board)
        for bishop in pieces["Bishop"]:
            move_list += self.bishopmoves(bishop, player, game_board)
        for queen in pieces["Queen"]:
            move_list += self.queenmoves(queen, player, game_board)
        for king in pieces["King"]:
            move_list += self.kingmoves(king, player, game_board)

        return move_list

    def run_turn(self):
        """ This is called every time it is this AI.player's turn.

        Returns:
            bool: Represents if you want to end your turn. True means end your turn, False means to keep your turn going and re-call this function.
        """

        # Here is where you'll want to code your AI.

        # We've provided sample code that:
        #    1) prints the board to the console
        #    2) prints the opponent's last move to the console
        #    3) prints how much time remaining this AI has to calculate moves

        # 1) print the board to the console
        for r in range(9, -2, -1): # iterate through the range in reverse order
            output = ""
            if r == 9 or r == 0: # then the top or bottom of the board
                output = "   +------------------------+"
            elif r == -1: # then show the ranks
                output = "     a  b  c  d  e  f  g  h"
            else: # board
                output = " " + str(r) + " |"
                # fill in all the files with pieces at the current rank
                for file_offset in range(0, 8):
                    f = chr(ord("a") + file_offset) # start at a, with with file offset increasing the char
                    current_piece = None
                    for piece in self.game.pieces:
                        if piece.file == f and piece.rank == r: # then we found the piece at (file, rank)
                            current_piece = piece
                            break

                    code = "." # default "no piece"
                    if current_piece:
                        code = current_piece.type[0] # the code will be the first character of their type, e.g. 'Q' for "Queen"

                        if current_piece.type == "Knight": # 'K' is for "King", we use 'N' for "Knights"
                            code = "N"

                        if current_piece.owner.id == "1": # the second player (black) is lower case. Otherwise it's upppercase already
                            code = code.lower()

                    output += " " + code + " "

                output += "|"

            print(output)

        # 2) print the opponent's last move to the console
        if len(self.game.moves) > 0:
            print("Opponent's Last Move: '" + self.game.moves[-1].san + "'")

        # 3) print how much time remaining this AI has to calculate moves
        print("Time Remaining: " + str(self.player.time_remaining) + " ns")

        # 4) make a random (and probably invalid) move.

        best_move = self.minimax(self.game.board)


        """randomMove = random.choice(move_list)
        for move in move_list:
            if move[0] == randomMove[0]:
                print("{}{}{} {}{}{}".format(move[0].type[0:1], move[0].file,
                                             move[0].rank, move[0].type[0:1], move[1], move[2]))
        """

        if best_move[0].type == "Pawn":
            best_move[0].move(best_move[1], best_move[2], best_move[3])
        else:
            best_move[0].move(best_move[1], best_move[2])

        return True
