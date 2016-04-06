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

def time_func(func, rollout=0):
    timings = []
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
        start = time.clock()
        if rollout == 0:
            move, score = func(board, cur_move);
        else:
            move, score = func(board, cur_move, num_rollouts=rollout);
        end = time.clock()
        timings.append(end-start)

        # Make the move
        reversi.make_move(board, move, cur_move);
        cur_move = reversi.get_other_player(cur_move);
    # Append score to list
    myscore = reversi.get_score_difference(board)
    return (timings, myscore)

if __name__ == '__main__':
    # Run alpha-beta and minimax
    for f in [alpha_beta, minimax]:
        f_output = time_func(f.get_move)
        avg_timing = sum(f_output[0])/float(len(f_output[0]))
        print("{0} has avg runtime of {1:.4f} with avg score {2:.4f}".format(f.__name__, avg_timing, f_output[1]))

    # Run monte_carlo
    for rollout in [2,20,200,1000,2000]:
        rollout_time = []
        rollout_score = []
        # Do x runs per rollout
        for k in range(50):
            monte_carlo.all_nodes = {} # Reset nodes
            f_output = time_func(monte_carlo.get_move, rollout)
            rollout_time.append(sum(f_output[0])/float(len(f_output[0])))
            rollout_score.append(f_output[1])

        avg_time = sum(rollout_time)/float(len(rollout_time))
        avg_score = sum(rollout_score)/float(len(rollout_score))
        print("Monte Carlo {0:5d} rollouts has avg runtime of {1:.4f}, with avg score {2:.4f}".format(rollout, avg_time,avg_score))
