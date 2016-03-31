from code import reversi;
from copy import deepcopy;


def get_move(board, player):
    print('Get move {}'.format(player));
    reversi.draw_board_with_moves(board, player);

    possibleMoves = reversi.get_valid_moves(board, player)
    # Terminate search at the bottom of the tree
    if len(possibleMoves) == 0:
        score = reversi.get_score(board)[player]
        print('No moves! score={}'.format(score));
        return None, score;

    other_player = reversi.get_other_player(player);

    bestScore = -1;
    for x, y in possibleMoves:
        dupeBoard = deepcopy(board);
        reversi.make_move(dupeBoard, x, y, player);
        move, score = get_move(dupeBoard, other_player);
        if score > bestScore:
            bestMove = (x, y);
            bestScore = score

    print("best move={}, score={}".format(bestMove, bestScore));
    return bestMove, score;


if __name__ == '__main__':
    board = reversi.make_board(4);
    cur_move = 'X';
    while reversi.get_valid_moves(board, cur_move):
        reversi.draw_board_with_moves(board, cur_move);
        (m_x, m_y), score = get_move(board, cur_move);
        print((m_x, m_y), score);
        reversi.make_move(board, m_x, m_y, cur_move);
        cur_move = reversi.get_other_player(cur_move);
    reversi.draw_board(board);
