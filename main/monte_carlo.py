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
        self.parents = set();
        # Use None as a placeholder for nodes that have not yet been expanded.
        self.children = {m: None for m in reversi.get_valid_moves(board, player)};

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

        # Otherwise, see if this node already exists
        new_board = deepcopy(self.board);
        other_player = reversi.get_other_player(self.player);
        reversi.make_move(new_board, move, self.player);
        new_node = get_node(new_board, other_player);
        # Add the node to children and self to parents of the child
        self.children[move] = new_node;
        if new_node.score != float('-inf') and new_node.score != float('inf'):
            self.update_ancestors();
        new_node.parents.add(self);
        return new_node;

    def get_best_move(self):
        assert self.player == 'X' or self.player == 'O';
        sorted_moves = sorted(((k, v.score) for k, v in self.children.items() if v is not None), key=lambda i: i[1],
                              reverse=self.player == 'X');
        if len(sorted_moves) > 0:
            if sorted_moves[0][1] == float('-inf') or sorted_moves[0][1] == float('inf'):
                assert False;
            return sorted_moves[0];
        # I have no idea what to do, pick a random move!
        print('using random move');
        return random.choice(list(self.children.keys())), float('-inf') if self.player == 'X' else float('inf');

    def get_scores(self):
        return [v.score for k, v in self.children.items() if v is not None];

    def update_ancestors(self, score=None):
        # Update my own score
        score_before = self.score;
        if score is not None:
            assert len(self.children.items()) == 0;
            # First call
            self.score = score;
            assert self.score != float('-inf') and self.score != float('inf');
        else:
            # Recursive case
            if self.player == 'X':
                self.score = max(self.get_scores());
                if self.score == float('-inf'):
                    assert False;
            else:
                self.score = min(self.get_scores());
                if self.score == float('inf'):
                    assert False;

        # Propogate upwards
        if self.score != score_before:
            for p in self.parents:
                p.update_ancestors();

    def __repr__(self):
        return str(self.board) + str(self.player);

    def __hash__(self):
        return hash_board(self.board, self.player).__hash__();


def get_node(board, player):
    hash = hash_board(board, player);
    if hash in all_nodes:
        return all_nodes[hash];
    n = Node(board, player);
    all_nodes[hash] = n;
    return n;


def get_move(board, player, num_rollouts=100):
    # Find out where we are in the game tree
    node = get_node(board, player);

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
    # Backpropogate the new score up the tree as necessary.
    rollout[-1].update_ancestors(reversi.get_score_difference(rollout[-1].board));


if __name__ == '__main__':
    import minimax;
    import alpha_beta;
    from statistics import mean, stdev, mode;

    mc_player = "X";

    scores = {};
    for rollouts in [1, 10, 100, 1000, 10000, 50000]:
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
