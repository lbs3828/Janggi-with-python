from janggi_const import *


def is_in_fortress(pos: tuple[int, int]) -> bool:
    # pos가 궁성 안에 있는지 검사
    if not ((3 <= pos[0] <= 5) and ((7 <= pos[1] <= 9) or (0 <= pos[1] <= 2))):
        return False
    else:
        return True


def is_in_board(pos: tuple[int, int]) -> bool:
    # pos가 장기판 안에 있는지 검사
    if not ((0 <= pos[0] <= 8) and (0 <= pos[1] <= 9)):
        return False
    else:
        return True


def mouse_pos_to_board_idx(x: int, y: int) -> tuple[bool, int, int]:
    boardI, boardJ = -1, -1

    horizontal_line_list = [CELL_WIDTH * i + WHITE_SPACE_WIDTH for i in range(9)]
    vertical_line_list = [CELL_HEIGHT * j + WHITE_SPACE_HEIGHT for j in range(10)]

    adjacent_i_value = min(horizontal_line_list, key=lambda i: abs(i - x))
    adjacent_j_value = min(vertical_line_list, key=lambda j: abs(j - y))

    gap = JANGGI_KING_PIECE_SIZE / 2
    if adjacent_i_value - gap <= x <= adjacent_i_value + gap and adjacent_j_value - gap <= y <= adjacent_j_value + gap:
        boardI = horizontal_line_list.index(adjacent_i_value)
        boardJ = vertical_line_list.index(adjacent_j_value)
        return True, boardI, boardJ

    return False, boardI, boardJ