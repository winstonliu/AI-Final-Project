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
        # Pick a move leading to the maximum score
        sorted_moves = sorted(((k, v.score) for k, v in self.children.items() if v is not None), key=lambda i: i[1],
                              reverse=self.player == 'X');
        if len(sorted_moves) > 0:
            assert sorted_moves[0][1] != float('-inf') and sorted_moves[0][1] != float('inf')
            return sorted_moves[0];
        # No rollouts have been performed! Pick a random move
        return random.choice(list(self.children.keys())), float('-inf') if self.player == 'X' else float('inf');

    def get_scores(self):
        ''' Gets the scores of all explored children of this node. '''
        return (v.score for k, v in self.children.items() if v is not None);

    def update_ancestors(self, score=None):
        ''' Updates the current node with the given score, then propogates the score as necessary to all ancestors of this node. '''

        score_before = self.score;
        if score is not None:
            # Update my own score
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
    from main import minimax;
    from main import alpha_beta;
    from statistics import mean, stdev, mode;

    num_games = 100;
    rollouts_selection = [0, 2, 5];
    # Play as both X and O
    for mc_player in ['X', 'O']:
        print("MCTS playing {} --".format(mc_player));
        for rollouts in rollouts_selection:
            # Keep track of the scores for this configuration
            scores = [];
            ## Play n games
            for game_num in range(num_games):
                # Reset the game tree search
                all_nodes = {};
                # The board we are playing on
                board = reversi.make_board(4);
                # Always start as player X
                cur_move = 'X';
                # Flag that keeps track of if the previous player had passed (made no move)
                passed = False;
                # Loop until the game is over
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

                    # Play a regular move
                    if cur_move == mc_player:
                        move, score = get_move(board, cur_move, num_rollouts=rollouts);
                    else:
                        move, score = alpha_beta.get_move(board, cur_move);
                    reversi.make_move(board, move, cur_move);
                    cur_move = reversi.get_other_player(cur_move);
                # Final outcome of the game
                scores.append(reversi.get_score_difference(board));

            # Output data
            print(str(rollouts) + " " + " ".join([str(r) for r in scores]));
