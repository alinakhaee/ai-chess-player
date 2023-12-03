import chess

from ChessGame import ChessGame
from MiniMaxPlayer import MiniMaxPlayer

white_player = MiniMaxPlayer(chess.WHITE, 'white')
black_player = MiniMaxPlayer(chess.BLACK, 'black')
FEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
variation = 1

while True:
    try:
        print('1.standard\n2.charge of the light brigade\n')
        num = int(input('your choice: '))
        if num == 1:
            break
        elif num == 2:
            variation = 2
            FEN = 'nnnnknnn/pppppppp/8/8/8/8/PPPPPPPP/1Q1QK1Q1 w KQkq - 0 1'
        else:
            raise(Exception)
        break
    except Exception:
        print('your choice must be a number in range [0..3]')
        continue

game = ChessGame(white_player, black_player, FEN)

print(game.play(variation))
