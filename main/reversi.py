import itertools;
from copy import deepcopy;


def make_board(size):
    board = [[' ' for y in range(size)] for x in range(size)];
    c = size // 2;
    board[c - 1][c - 1] = 'O';
    board[c - 1][c] = 'X';
    board[c][c - 1] = 'X';
    board[c][c] = 'O';
    return board;


def draw_board(board):
    for row in range(len(board)):
        print("+-" * len(board) + "+");
        for col in range(len(board[row])):
            c = board[col][row];
            print("|" + c, end='');
        print("|");
    print("+-" * len(board) + "+");


def draw_board_with_moves(board, player):
    moves = get_valid_moves(board, player);
    for row in range(len(board)):
        print("+-" * len(board) + "+");
        for col in range(len(board[row])):
            c = board[col][row];
            c = '.' if (col, row) in moves else c;
            print("|" + c, end='');
        print("|");
    print("+-" * len(board) + "+");


def get_other_player(player):
    return 'X' if player == 'O' else 'O' if player == 'X' else None;


def get_valid_moves(board, player, prev_passed=False):
    board_size = len(board);
    other_player = get_other_player(player);
    moves = [];
    # For all spaces on the board
    for x, y in itertools.product(range(board_size), range(board_size)):
        # If the space is already occupied, try another
        if board[x][y] != ' ':
            continue;
        # For all connected directions (game is 8-connected)
        for dx, dy in [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]:
            # x_ moves in one direction along the x-axis
            x_ = x;
            # y_ moves in one direction along the y-axis
            y_ = y;
            # If this move is valid, we don't have to check any other directions. Skip to next move.
            valid_move_found = False;
            # A flag to keep track of if we have encountered any opposing pieces to capture in this direction.
            found_other_player = False;
            while True:
                x_ += dx;
                y_ += dy;
                # If x_ or y_ falls outside the board, this direction is invalid
                if x_ < 0 or x_ >= board_size or y_ < 0 or y_ >= board_size:
                    break;
                # If we find at least one piece belonging to the other player, keep going
                elif board[x_][y_] == other_player:
                    found_other_player = True;
                # If we had previously found a piece belonging to another player, we may be able to prove this is a valid move
                elif found_other_player and board[x_][y_] == player:
                    moves.append((x, y));
                    valid_move_found = True;
                    break;
                # If we encounter an empty space or ourselves, this direction is invalid
                elif board[x_][y_] == ' ' or board[x_][y_] == player:
                    break;
            if valid_move_found:
                break;
    # If you have no valid moves, but the other player does, you must pass.
    if len(moves) == 0 and not prev_passed and len(get_valid_moves(board, other_player, prev_passed=True)) > 0:
        return [None];
    return moves;


def make_move(board, move, player):
    # If this move is a pass, do nothing
    if move is None:
        return;

    x, y = move;

    board_size = len(board);
    board[x][y] = player;
    other_player = get_other_player(player);
    for dx, dy in [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]:
        # x_ moves in one direction along the x-axis
        x_ = x;
        # y_ moves in one direction along the y-axis
        y_ = y;
        # A flag to keep track of if we have encountered any opposing pieces to capture in this direction.
        found_other_player = False;
        while True:
            x_ += dx;
            y_ += dy;
            # If x_ or y_ falls outside the board, this direction is invalid
            if x_ < 0 or x_ >= board_size or y_ < 0 or y_ >= board_size:
                break;
            # If we find at least one piece belonging to the other player, keep going
            elif board[x_][y_] == other_player:
                found_other_player = True;
            # If we had previously found a piece belonging to another player, we may be able to prove this is a valid move
            elif found_other_player and board[x_][y_] == player:
                # Flip all pieces enclosed
                while x_ != x or y_ != y:
                    board[x_][y_] = player;
                    x_ -= dx;
                    y_ -= dy;
                break;
            # If we encounter an empty space or ourselves, this direction is invalid
            elif board[x_][y_] == ' ' or board[x_][y_] == player:
                break;
    return;


def get_score(board):
    ''' Return the score of the current board.
    Returns Dictionary {'X': score_x, 'O': score_y}. '''
    xs = 0;
    os = 0;
    for row in board:
        for c in row:
            if c == 'X':
                xs += 1;
            elif c == 'O':
                os += 1;
    return {'X': xs, 'O': os};


if __name__ == '__main__':
    board = make_board(4);
    draw_board_with_moves(board, 'X');
    make_move(board, (2, 0), 'X');
    draw_board_with_moves(board, 'O');
    make_move(board, (1, 0), 'O');
    draw_board_with_moves(board, 'X');
    make_move(board, (0, 0), 'X');
    draw_board_with_moves(board, 'O');

    print('end');
