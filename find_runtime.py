import time

from main import reversi
from main import monte_carlo
from main import alpha_beta
from main import minimax

def time_func(func, rollout=0):
    # The board we are playing on
    board = reversi.make_board(4);
    # Whose turn it is to play
    cur_move = 'X';
    # Flag that keeps track of if the previous player had passed (made no move)
    passed = False;
    if len(reversi.get_valid_moves(board, cur_move)) == 0:
        # If the other player passed too, the game is over
        if passed:
            return
        # Otherwise, allow the other player to continue playing(!)
        passed = True;
        return
    # Reset the pass counter
    passed = False;

    # Play a regular move.
    start = time.clock()
    if rollout == 0:
        move, score = func(board, cur_move);
    else:
        move, score = func(board, cur_move, num_rollouts=rollout);
    end = time.clock()
    timing = end - start

    return timing

if __name__ == '__main__':
    # Run alpha-beta and minimax
    for f in [alpha_beta, minimax]:
        f_output = time_func(f.get_move)
        print("{0} has max runtime of {1:.4f}".format(f.__name__, f_output))

    # Run monte_carlo
    for rollout in [2,20,250,1000,2000, 5000, 8000, 10000]:
        rollout_time = []
        # Do x runs per rollout
        for k in range(50):
            monte_carlo.all_nodes = {} # Reset nodes
            f_output = time_func(monte_carlo.get_move, rollout)
            rollout_time.append(f_output)

        avg_time = sum(rollout_time)/float(len(rollout_time))
        print("Monte Carlo {0:5d} rollouts has avg runtime of {1:.4f}".format(rollout, avg_time))
