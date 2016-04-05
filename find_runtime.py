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

        reversi.make_move(board, move, cur_move);
        cur_move = reversi.get_other_player(cur_move);

    return timings

if __name__ == '__main__':
    # Run alpha-beta and minimax
    for f in [alpha_beta, minimax]:
        timings = time_func(f.get_move)
        avg_timing = sum(timings)/float(len(timings))
        print("{} has avg runtime of {}".format(f.__name__, avg_timing))

    # Run monte_carlo
    for rollout in [2,20,200,2000]:
        rollout_time = []
        # Do x runs per rollout
        for k in range(100):
            monte_carlo.all_nodes = {} # Reset nodes
            timings = time_func(f.get_move, rollout)
            rollout_time.append(sum(timings)/float(len(timings)))

        avg_time = sum(rollout_time)/float(len(rollout_time))
        print("Monte Carlo {} rollouts has avg runtime of {}".format(rollout, avg_time))
