from ai import *

MIN = -float("inf")
MAX = float("inf")

fen_dict = {}

class MiniMaxPlayer:
    player_color = chess.WHITE
    nick_name = 'default player'
    max_depth = 3
    move_count = 0

    def __init__(self, color: bool, nick: str):
        self.nick_name = nick
        self.player_color = color

    def evaluate(self, board: chess.Board) -> float:
        fen = board.fen().split(' ')[0] + ' ' + board.fen().split(' ')[1]
        dict_output = fen_dict.get(fen, None)
        if dict_output is not None:
            return dict_output
        total = 0
        end_game = are_we_in_end_game(board)

        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if not piece:
                continue
            value = piece_value[piece.piece_type] + evaluate_position(piece, square, end_game)
            if piece.color == chess.WHITE:
                total += value
            else:
                total -= value
        fen_dict[fen] = total
        return total

    def evaluate_cotlb(self, board: chess.Board) -> float:
        fen = board.fen().split(' ')[0] + ' ' + board.fen().split(' ')[1]
        dict_output = fen_dict.get(fen, None)
        if dict_output is not None:
            return dict_output
        total = 0

        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if not piece:
                continue

            if piece.color == chess.WHITE:
                value = piece_value_white_cotlb[piece.piece_type] + evaluate_position_cotlb(piece, square, False)
                total += value
            else:
                value = piece_value_black_cotlb[piece.piece_type] + evaluate_position_cotlb(piece, square, False)
                total -= value
        fen_dict[fen] = total
        return total

    def move(self, board: chess.Board, variation) -> chess.Move:
        number_of_pieces = len(board.piece_map())
        if 10 < number_of_pieces < 20:
            self.max_depth = 4
        elif 8 < number_of_pieces <= 10:
            self.max_depth = 5
        elif number_of_pieces <= 8:
            self.max_depth = 6
        value = -float('inf') if self.player_color else float('inf')
        best_move = None
        legal_moves = list(board.legal_moves)
        for move in legal_moves:
            board.push(move)
            if board.is_checkmate():
                board.pop()
                return move
            if board.can_claim_draw():
                temp = 0
            else:
                if variation == 1:
                    temp = minimizer(board, self.max_depth, MIN, MAX, self.evaluate, variation) if self.player_color \
                        else maximizer(board, self.max_depth, MIN, MAX, self.evaluate, variation)
                else:
                    temp = minimizer(board, self.max_depth, MIN, MAX, self.evaluate_cotlb, variation) if self.player_color \
                        else maximizer(board, self.max_depth, MIN, MAX, self.evaluate_cotlb, variation)
            if board.is_game_over():
                if variation == 1:
                    value = max(value, self.evaluate(board)) if self.player_color \
                        else min(value, self.evaluate(board))
                else:
                    value = max(value, self.evaluate_cotlb(board)) if self.player_color \
                        else min(value, self.evaluate_cotlb(board))
                if self.player_color:
                    if temp >= value:
                        value = temp
                        best_move = move
                else:
                    if temp <= value:
                        value = temp
                        best_move = move

                board.pop()
                continue
            if self.player_color:
                if temp >= value:
                    value = temp
                    best_move = move
            else:
                if temp <= value:
                    value = temp
                    best_move = move
            board.pop()
        self.move_count += 1
        return best_move
