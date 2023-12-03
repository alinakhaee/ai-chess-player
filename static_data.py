import chess

# based on:
# https://www.chessprogramming.org/Simplified_Evaluation_Function

piece_value = {
    chess.PAWN: 100,
    chess.ROOK: 500,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.QUEEN: 900,
    chess.KING: 20000
}

piece_value_white_cotlb = {
    chess.PAWN: 100,
    chess.ROOK: 0,
    chess.KNIGHT: 0,
    chess.BISHOP: 0,
    chess.QUEEN: 900,
    chess.KING: 20000
}
piece_value_black_cotlb = {
    chess.PAWN: 100,
    chess.ROOK: 0,
    chess.KNIGHT: 320,
    chess.BISHOP: 0,
    chess.QUEEN: 0,
    chess.KING: 20000
}

pawn_position_based_eval_for_white = [
    0, 0, 0, 0, 0, 0, 0, 0,
    50, 50, 50, 50, 50, 50, 50, 50,
    10, 10, 20, 30, 30, 20, 10, 10,
    5, 5, 10, 25, 25, 10, 5, 5,
    0, 0, 0, 20, 20, 0, 0, 0,
    5, -5, -10, 0, 0, -10, -5, 5,
    5, 10, 10, -20, -20, 10, 10, 5,
    0, 0, 0, 0, 0, 0, 0, 0,
]
pawn_position_based_eval_for_black = list(reversed(pawn_position_based_eval_for_white))

pawn_position_based_eval_for_white_cotlb = [
    0, 0, 0, 0, 0, 0, 0, 0,
    5, 10, -20, -10, -10, -20, 10, 5,
    5, -5, 10, 5, 10, 5, -5, 5,
    15, 10, 5, 10, 5, 10, 10, 15,
    25, 15, 10, 5, 5, 10, 15, 25,
    30, 20, 15, 10, 10, 15, 20, 30,
    50, 50, 50, 50, 50, 50, 50, 50,
    0, 0, 0, 0, 0, 0, 0, 0,
]
pawn_position_based_eval_for_black_cotlb = [
    0, 0, 0, 0, 0, 0, 0, 0,
    50, 50, 50, 50, 50, 50, 50, 50,
    10, 20, 20, 30, 30, 20, 20, 10,
    10, 15, 15, 20, 20, 15, 15, 10,
    5, 10, 20, 30, 30, 20, 10, 5,
    0, 5, 10, 10, 10, 10, -5, 0,
    0, 0, -5, -5, -5, -5, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
]

knight_position_based_eval_for_white = [
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20, 0, 0, 0, 0, -20, -40,
    -30, 0, 10, 15, 15, 10, 0, -30,
    -30, 5, 15, 20, 20, 15, 5, -30,
    -30, 0, 15, 20, 20, 15, 0, -30,
    -30, 5, 10, 15, 15, 10, 5, -30,
    -40, -20, 0, 5, 5, 0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50,
]
knight_position_based_eval_for_black = list(reversed(knight_position_based_eval_for_white))

knight_position_based_eval_for_black_cotlb = [
    -40, -30, 5, 5, 5, 5, -30, -40,
    -30, -20, 10, 10, 10, 10, -20, -30,
    5, 10, 20, 15, 15, 20, 10, 5,
    5, 10, 15, 20, 20, 15, 10, 5,
    -30, 10, 15, 20, 20, 15, 10, -30,
    -20, 5, 10, 15, 15, 10, 5, -20,
    -40, -40, 0, 5, 5, 0, -40, -40,
    -50, -40, -20, -30, -30, -20, -40, -50,
]

bishop_position_based_eval_for_white = [
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -10, 0, 5, 10, 10, 5, 0, -10,
    -10, 5, 5, 10, 10, 5, 5, -10,
    -10, 0, 10, 10, 10, 10, 0, -10,
    -10, 10, 10, 10, 10, 10, 10, -10,
    -10, 5, 0, 0, 0, 0, 5, -10,
    -20, -10, -10, -10, -10, -10, -10, -20,
]
bishop_position_based_eval_for_black = list(reversed(bishop_position_based_eval_for_white))

rook_position_based_eval_for_white = [
    0, 0, 0, 0, 0, 0, 0, 0,
    5, 10, 10, 10, 10, 10, 10, 5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    0, 0, 0, 5, 5, 0, 0, 0,
]
rook_position_based_eval_for_black = list(reversed(rook_position_based_eval_for_white))

queen_position_based_eval_for_white = [
    -20, -10, -10, -5, -5, -10, -10, -20,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -10, 0, 5, 5, 5, 5, 0, -10,
    -5, 0, 5, 5, 5, 5, 0, -5,
    0, 0, 5, 5, 5, 5, 0, -5,
    -10, 5, 5, 5, 5, 5, 0, -10,
    -10, 0, 5, 0, 0, 0, 0, -10,
    -20, -10, -10, -5, -5, -10, -10, -20,
]
queen_position_based_eval_for_black = list(reversed(queen_position_based_eval_for_white))
queen_position_based_eval_for_white_cotlb = [
    -10, -5, -5, -5, -5, -5, -5, -10,
    -5, 0, 0, 5, 5, 0, 0, -5,
    -5, 0, 5, 5, 5, 5, 0, -5,
    5, 5, 5, 5, 5, 5, 5, 5,
    0, 5, 5, 5, 5, 5, 5, 0,
    -5, 0, 5, 5, 5, 5, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -20, -15, -10, -5, -5, -10, -15, -20,
]

king_position_based_eval_for_white = [
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -20, -30, -30, -40, -40, -30, -30, -20,
    -10, -20, -20, -20, -20, -20, -20, -10,
    20, 20, 0, 0, 0, 0, 20, 20,
    20, 30, 10, 0, 0, 10, 30, 20,
]
king_position_based_eval_for_black = list(reversed(king_position_based_eval_for_white))
king_position_based_eval_for_black_cotlb = king_position_based_eval_for_white
king_position_based_eval_for_white_cotlb = [
    -30, -20, 20, 10, 10, 20, -20, -30,
    -20, -10, 20, 20, 20, 20, -10, -20,
    -10, -20, -20, -20, -20, -20, -20, -10,
    -10, -30, -30, -40, -40, -30, -30, -20,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -20, -20, -30, -30, -20, -20, -30,
    -40, -30, -20, -40, -40, -20, -30, -40,
]

king_position_based_eval_for_white_end_game = [
    -50, -40, -30, -20, -20, -30, -40, -50,
    -30, -20, -10, 0, 0, -10, -20, -30,
    -30, -10, 20, 30, 30, 20, -10, -30,
    -30, -10, 30, 40, 40, 30, -10, -30,
    -30, -10, 30, 40, 40, 30, -10, -30,
    -30, -10, 20, 30, 30, 20, -10, -30,
    -30, -30, 0, 0, 0, 0, -30, -30,
    -50, -30, -30, -30, -30, -30, -30, -50
]
king_position_based_eval_for_black_end_game = list(reversed(king_position_based_eval_for_white_end_game))
