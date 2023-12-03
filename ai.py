from static_data import *

def evaluate_position(piece: chess.Piece, square: chess.Square, end_game: bool) -> int:
    piece_type = piece.piece_type
    positions = None
    if piece_type == chess.PAWN:
        if piece.color == chess.WHITE:
            positions = pawn_position_based_eval_for_white
        else:
            positions = pawn_position_based_eval_for_black
    if piece_type == chess.KNIGHT:
        if piece.color == chess.WHITE:
            positions = knight_position_based_eval_for_white
        else:
            positions = knight_position_based_eval_for_black
    if piece_type == chess.BISHOP:
        if piece.color == chess.WHITE:
            positions = bishop_position_based_eval_for_white
        else:
            positions = bishop_position_based_eval_for_black
    if piece_type == chess.ROOK:
        if piece.color == chess.WHITE:
            positions = rook_position_based_eval_for_white
        else:
            positions = rook_position_based_eval_for_black
    if piece_type == chess.QUEEN:
        if piece.color == chess.WHITE:
            positions = queen_position_based_eval_for_white
        else:
            positions = queen_position_based_eval_for_black
    if piece_type == chess.KING:
        if end_game:
            if piece.color == chess.WHITE:
                positions = king_position_based_eval_for_white_end_game
            else:
                positions = king_position_based_eval_for_black_end_game
        else:
            if piece.color == chess.WHITE:
                positions = king_position_based_eval_for_white
            else:
                positions = king_position_based_eval_for_black

    return positions[square]


def evaluate_position_cotlb(piece: chess.Piece, square: chess.Square, end_game: bool) -> float:
    piece_type = piece.piece_type
    positions = None
    if piece_type == chess.PAWN:
        if piece.color == chess.WHITE:
            positions = pawn_position_based_eval_for_white_cotlb
        else:
            positions = pawn_position_based_eval_for_black_cotlb
    if piece_type == chess.KNIGHT:
        if piece.color == chess.WHITE:
            return -float('inf')
        else:
            positions = knight_position_based_eval_for_black_cotlb
    if piece_type == chess.BISHOP or piece_type == chess.ROOK:
        if piece.color == chess.WHITE:
            return -float('inf')
        else:
            return -float('inf')
    if piece_type == chess.QUEEN:
        if piece.color == chess.WHITE:
            positions = queen_position_based_eval_for_white_cotlb
        else:
            return -float('inf')
    if piece_type == chess.KING:
        if end_game:
            if piece.color == chess.WHITE:
                positions = king_position_based_eval_for_white_end_game
            else:
                positions = king_position_based_eval_for_black_end_game
        else:
            if piece.color == chess.WHITE:
                positions = king_position_based_eval_for_white_cotlb
            else:
                positions = king_position_based_eval_for_black_cotlb

    return positions[square]

def evaluate_move(move: chess.Move, board: chess.Board, move_eval_dict: dict, variation):
    if variation == 1:
        white_piece_values = piece_value
        black_piece_values = piece_value
    else:
        white_piece_values = piece_value_white_cotlb
        black_piece_values = piece_value_black_cotlb
    start_point = move.from_square
    end_point = move.to_square
    source_rank = chess.square_rank(move.from_square)
    dest_rank = chess.square_rank(move.to_square)
    # Check if it's a forward move for white or black
    player_color = board.piece_at(start_point).color
    piece_at_start = board.piece_at(start_point)
    piece_at_end = board.piece_at(end_point)
    value = 0
    if board.gives_check(move):  # a check move
        value = 900 if player_color else -900
    elif piece_at_end:  # an attacking move or capture
        if player_color:
            value = black_piece_values[piece_at_end.piece_type] - white_piece_values[
                piece_at_start.piece_type] // 10
        else:
            value = -(white_piece_values[piece_at_end.piece_type] - black_piece_values[
                piece_at_start.piece_type] // 10)
    elif board.is_attacked_by(not player_color, start_point):  # a defensive move
        if player_color:
            value = white_piece_values[piece_at_start.piece_type] // 10
        else:
            value = - black_piece_values[piece_at_start.piece_type] // 10
    elif player_color and dest_rank > source_rank:  # forward move for white
        value = 10
    elif not player_color and dest_rank < source_rank:  # forward move for black
        value = 10
    if piece_at_start.piece_type == chess.KING:
        value = value / 2
    move_eval_dict[move] = value
    return value


def are_we_in_end_game(board: chess.Board) -> bool:
    queens = 0
    bishops_knights = 0

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            if piece.piece_type == chess.QUEEN:
                queens += 1
            if piece.piece_type == chess.KNIGHT or piece.piece_type == chess.BISHOP:
                bishops_knights += 1
    # no one has a queen or no other pieces are on the board
    if queens == 0 or (queens == 2 and bishops_knights <= 1):
        return True
    else:
        return False

def maximizer(board: chess.Board, depth: int, alpha: float, beta: float, evaluate, variation) -> float:
    if board.is_checkmate():
        return -float("inf")
    if depth == 0 or board.is_game_over():
        return evaluate(board)
    value = -float('inf')
    max_move_evaluation_dict = {}
    legal_moves = node_ordering(board, True, max_move_evaluation_dict, variation)
    for move in legal_moves:
        if value - 100 > max_move_evaluation_dict[move]:
            break
        board.push(move)
        value = max(value, minimizer(board, depth - 1, alpha, beta, evaluate, variation))
        if value >= beta:
            board.pop()
            return value
        alpha = max(alpha, value)
        board.pop()
    return value


def minimizer(board: chess.Board, depth: int, alpha: float, beta: float, evaluate, variation) -> float:
    if board.is_checkmate():
        return float("inf")
    if depth == 0 or board.is_game_over():
        return evaluate(board)
    value = float('inf')
    min_move_evaluation_dict = {}
    legal_moves = node_ordering(board, False, min_move_evaluation_dict, variation)
    for move in legal_moves:
        if value + 100 < min_move_evaluation_dict[move]:
            break
        board.push(move)
        value = min(value, maximizer(board, depth - 1, alpha, beta, evaluate, variation))
        if value <= alpha:
            board.pop()
            return value
        beta = min(value, beta)
        board.pop()
    return value


def node_ordering(board: chess.Board, player_color: bool, move_eval_dict: dict, variation) -> list:
    legal_moves = list(board.legal_moves)
    legal_moves.sort(key=lambda move: evaluate_move(move, board, move_eval_dict, variation), reverse=True) if player_color \
        else legal_moves.sort(key=lambda move: evaluate_move(move, board, move_eval_dict, variation))
    return legal_moves
