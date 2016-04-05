import time

from main import reversi
from main import monte_carlo
from main import alpha_beta
from main import minimax

def runtime(func):
    ''' Wrapper function for timing purposes '''
    start = time.clock()
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    end = time.clock()
    print(end - start)
    return wrapper

def time_func(func):
    # The board we are playing on
    board = reversi.make_board(4);
    # Whose turn it is to play
    cur_move = 'X';
    # Flag that keeps track of if the previous player had passed (made no move)
    passed = False;
    while True:
        if len(reversi.get_valid_moves(board, cur_move)) == 0:
            # If the other player passed too, the game is over
            if passed:
                break;
            # Otherwise, allow the other player to continue playing(!)
            passed = True;
            continue;
        # Reset the pass counter
        passed = False;

        # Play a regular move.
        move, score = func(board, cur_move);
        reversi.make_move(board, move, cur_move);
        cur_move = reversi.get_other_player(cur_move);

if __name__ == '__main__':

