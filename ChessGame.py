import os
import platform

import chess
import time


def clear_screen():
    plt = platform.system()
    if plt == 'Linux' or plt == 'Darwin':
        os.system('clear')
    elif plt == 'Windows':
        os.system('cls')


class ChessGame:
    white_player = None
    black_player = None
    board = None

    def __init__(self, w, b, init_state):
        self.white_player = w
        self.black_player = b
        self.board = chess.Board(init_state)

    def __str__(self) -> str:
        out = ''
        count = 0
        for square in chess.SQUARES:
            count += 1
            piece = self.board.piece_at(square)
            if not piece:
                out += "◻"
            if piece and piece.color == chess.WHITE:
                if piece.piece_type == chess.PAWN:
                    out += "♟"
                if piece.piece_type == chess.KNIGHT:
                    out += "♞"
                if piece.piece_type == chess.BISHOP:
                    out += "♝"
                if piece.piece_type == chess.ROOK:
                    out += "♜"
                if piece.piece_type == chess.QUEEN:
                    out += "♛"
                if piece.piece_type == chess.KING:
                    out += "♚"
            if piece and piece.color == chess.BLACK:
                if piece.piece_type == chess.PAWN:
                    out += "♙"
                if piece.piece_type == chess.KNIGHT:
                    out += "♘"
                if piece.piece_type == chess.BISHOP:
                    out += "♗"
                if piece.piece_type == chess.ROOK:
                    out += "♖"
                if piece.piece_type == chess.QUEEN:
                    out += "♕"
                if piece.piece_type == chess.KING:
                    out += "♔"
            out += ' '
            if count == 8:
                out += '\n'
                count = 0
        return out

    def play(self, variation) -> chess.Outcome:
        steps = 0
        start_time = time.time()
        while True:
            move = self.white_player.move(self.board, variation)
            steps = steps + 1
            clear_screen()
            self.board.push(move)
            print('white move', move)
            print(self.board.fen())
            print(self)
            if self.board.is_game_over():
                print('steps= ', steps)
                end_time = time.time()
                elapsed_time = end_time - start_time
                print(f"Execution time: {elapsed_time} seconds")
                return self.board.outcome()

            # a = input("continue?")
            # clear_screen()
            move = self.black_player.move(self.board, variation)
            steps = steps + 1
            self.board.push(move)
            clear_screen()
            print('black move', move)
            print(self.board.fen())
            print(self)
            if self.board.is_game_over():
                print('steps= ', steps)
                end_time = time.time()
                elapsed_time = end_time - start_time
                print(f"Execution time: {elapsed_time} seconds")
                return self.board.outcome()

            # a = input("continue?")
            # clear_screen()
