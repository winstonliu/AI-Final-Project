from main import reversi;
import random;
from copy import deepcopy;
import itertools;

all_nodes = {};


class Node(object):
    def __init__(self, board, player):
        '''Build a new node object with no parents.
        Children will automatically be initialized to all valid moves, but thier nodes will not be searched.'''
        self.board = board;
        self.player = player;
        # The score starts at the worst possible score.
        self.score = float('-inf') if player == 'X' else float('inf');
        # Use None as a placeholder for nodes that have not yet been expanded.
        self.children = {m: None for m in reversi.get_valid_moves(board, player)};

        # Cache parts of the game tree TODO need a better way of doing this
        # There are a lot of conflicts with this method
        global all_nodes;
        all_nodes[hash_board(board, player)] = self;

    def get_child(self):
        possible_moves = list(self.children.keys());
        # If there are no new (unexplored) children, return None
        if len(possible_moves) == 0:
            return None;

        # Choose a random move
        move = random.choice(possible_moves);

        # If this child was previously explored, go down a node
        if self.children[move] is not None:
            return self.children[move];

        # Otherwise, initialize a new node and return it
        new_board = deepcopy(self.board);
        reversi.make_move(new_board, move, self.player);
        new_hash = hash_board(new_board, reversi.get_other_player(self.player));
        global all_nodes;
        if new_hash in all_nodes:
            new_node = all_nodes[new_hash];
        else:
            new_node = Node(new_board, reversi.get_other_player(self.player));
        self.children[move] = new_node;
        return new_node;

    def get_best_move(self):
        assert self.player == 'X' or self.player == 'O';
        sorted_moves = sorted(((k, v.score) for k, v in self.children.items() if v is not None), key=lambda i: i[1],
                              reverse=self.player == 'X');
        if len(sorted_moves) > 0:
            return sorted_moves[0];
        # I have no idea what to do, pick a random move!
        return random.choice(list(self.children.keys())), float('-inf') if self.player == 'X' else float('inf');

    def get_scores(self):
        return (v.score for k, v in self.children.items() if v is not None);

    def __repr__(self):
        return str(self.board) + str(self.player);

    def __hash__(self):
        return self.children.__hash__();


def get_move(board, player, num_rollouts=100000):
    # Find out where we are in the game tree
    global all_nodes;
    hash = hash_board(board, player);
    if hash not in all_nodes:
        Node(board, player);
    node = all_nodes[hash_board(board, player)];

    # Do lots of rollouts to show that this converges to minmax.
    for i in range(num_rollouts):
        do_rollout(node);

    # Get the best move so far from the evaluation
    return node.get_best_move();


def hash_board(board, player):
    '''Hashes a board state for later retrieval'''
    return str(board) + player;


def do_rollout(root):
    '''Makes one depth-first evaluation.'''
    # Do selection and expansion all the way down to a leaf node
    rollout = [root];
    while True:
        child = rollout[-1].get_child();
        if child is None:
            break;
        rollout.append(child);
    # Evaluate the leaf node
    rollout[-1].score = reversi.get_score_difference(rollout[-1].board);

    # Backpropogate the new score up the tree as necessary.
    for n in reversed(rollout[:-1]):
        assert n.player == 'X' or n.player == 'O';
        # Update the score for the min or max player. The score of a node is the min(max) of its children.
        # Note that we cannot perform alpha-beta pruning there because we haven't exhaustively expanded anything yet.
        score_before = n.score;
        if n.player == 'X':
            n.score = max(itertools.chain([float('-inf')], n.get_scores()));
        else:
            n.score = min(itertools.chain([float('inf')], n.get_scores()));
        # Stop propogation if we didn't change anything
        if n.score == score_before:
            break;


if __name__ == '__main__':
    import minimax;
    import alpha_beta;
    from statistics import mean, stdev, mode;

    mc_player = "X";

    scores = {};
    for rollouts in [2000, 5000, 10000, 50000, 100000]:
        scores[rollouts] = [];
        for game_num in range(100):
            # Reset the game tree search
            all_nodes = {};
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
                # reversi.draw_board_with_moves(board, cur_move);
                if cur_move == mc_player:
                    move, score = get_move(board, cur_move, num_rollouts=rollouts);
                else:
                    move, score = alpha_beta.get_move(board, cur_move);
                # print(move, score);

                reversi.make_move(board, move, cur_move);
                cur_move = reversi.get_other_player(cur_move);
            # Final outcome
            # reversi.draw_board(board);
            diff = reversi.get_score_difference(board);
            scores[rollouts].append(diff);

            print("#rollouts={}, game={}".format(rollouts, game_num));

    print("MCTS playing {} --".format(mc_player));
    for rollouts in sorted(scores.keys()):
        results = scores[rollouts];
        # print("{}: {} W/{} L".format(rollouts, sum(r == -8 for r in results), len(results)));
        print(str(rollouts) + " " + " ".join([str(r) for r in results]));
        # print("Mean score={}, stddev={}, mode={}".format(mean(results), stdev(results)));
