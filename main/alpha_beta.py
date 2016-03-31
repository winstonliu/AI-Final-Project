from copy import deepcopy;

from main import reversi


def get_move(board, player, alpha=float('-inf'), beta=float('inf'), passed=False):
    # Terminate search at the bottom of the tree
    if len(reversi.get_valid_moves(board, player)) == 0:
        if passed:
            result = reversi.get_score(board);
            return None, result['X'] - result['O'];
        else:
            return get_move(board, reversi.get_other_player(player), passed=True);

    if player == 'X':
        best_score = float('-inf');
        for x, y in reversi.get_valid_moves(board, 'X'):
            dupeBoard = deepcopy(board);
            reversi.make_move(dupeBoard, x, y, 'X');
            move, score = get_move(dupeBoard, 'O', alpha, beta);
            if score > best_score:
                best_move = (x, y);
                best_score = score;
            alpha = max(alpha, score);
            if alpha > beta:
                break;
        return best_move, best_score;
    else:
        best_score = float('inf');
        for x, y in reversi.get_valid_moves(board, 'O'):
            dupeBoard = deepcopy(board);
            reversi.make_move(dupeBoard, x, y, 'O');
            move, score = get_move(dupeBoard, 'X', alpha, beta);
            if score < best_score:
                best_move = (x, y);
                best_score = score;
            beta = min(beta, score);
            if alpha > beta:
                break;
        return best_move, best_score;
    return best_move, score;


if __name__ == '__main__':
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
        reversi.draw_board_with_moves(board, cur_move);
        (m_x, m_y), score = get_move(board, cur_move);
        print((m_x, m_y), score);
        reversi.make_move(board, m_x, m_y, cur_move);
        cur_move = reversi.get_other_player(cur_move);
    # Final outcome
    reversi.draw_board(board);
    print(reversi.get_score(board));
