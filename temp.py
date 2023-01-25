from JanggiTeam import *
from pygame.locals import Rect

class Janggi:
    def __init__(self):
        self._init_board()
        self._turn = BLUE_TEAM
        self._red_team = JanggiTeam(RED_TEAM)
        self._blue_team = JanggiTeam(BLUE_TEAM)
        self._Surface = pygame.display.set_mode((JANGGI_BOARD_WIDTH * MAGNIFICATION_RATIO,
                                                 JANGGI_BOARD_HEIGHT * MAGNIFICATION_RATIO))
        self._running = True

    def _init_board(self):
        self._board = [[0] * 9 for _ in range(10)]
        for piece in self._red_team.get_pieces():
            if piece.get_alive():
                i, j = piece.get_pos()
                self._board[j][i] = piece

        for piece in self._blue_team.get_pieces():
            if piece.get_alive():
                i, j = piece.get_pos()
                self._board[j][i] = piece

    def calc_movable_pos(self, src_piece: JanggiPiece) -> list[tuple[int, int]]:
        src_piece_type = src_piece.get_team_type()
        src_piece_team = src_piece.get_team_type()
        src_i, src_j = src_piece.get_pos()
        movable_pos_list = []

        if src_piece_type == 'K' or src_piece_type == 'G':
            if src_piece_team == BLUE_TEAM:
                if src_j + 1 <= 9 and (
                        self._board[src_j + 1][src_i] == 0 or self._board[src_j + 1][src_i].get_team_type() != src_piece_team):
                    movable_pos_list.append((0, 1))
                if src_j - 1 >= 7 and (
                        self._board[src_j - 1][src_i] == 0 or self._board[src_j - 1][src_i].get_team_type() != src_piece_team):
                    movable_pos_list.append((0, -1))
                if src_i + 1 <= 5 and src_j + 1 <= 9 and (
                        self._board[src_j + 1][src_i + 1] == 0 or self._board[src_j + 1][src_i + 1].get_team_type() != src_piece_team):
                    movable_pos_list.append((1, 1))
                if src_i + 1 <= 5 and src_j - 1 >= 7 and (
                        self._board[src_j - 1][src_i + 1] == 0 or self._board[src_j - 1][src_i + 1].get_team_type() != src_piece_team):
                    movable_pos_list.append((1, -1))
                if src_i - 1 >= 3 and src_j + 1 <= 9 and (
                        self._board[src_j + 1][src_i - 1] == 0 or self._board[src_j + 1][src_i - 1].get_team_type() != src_piece_team):
                    movable_pos_list.append((-1, 1))
                if src_i - 1 >= 3 and src_j - 1 >= 7 and (
                        self._board[src_j - 1][src_i - 1] == 0 or self._board[src_j - 1][src_i - 1].get_team_type() != src_piece_team):
                    movable_pos_list.append((-1, -1))
            else:
                if src_j + 1 <= 2 and (
                        self._board[src_j + 1][src_i] == 0 or self._board[src_j + 1][src_i].get_team_type() != src_piece_team):
                    movable_pos_list.append((0, 1))
                if src_j - 1 >= 0 and (
                        self._board[src_j - 1][src_i] == 0 or self._board[src_j - 1][src_i].get_team_type() != src_piece_team):
                    movable_pos_list.append((0, -1))
                if src_i + 1 <= 5 and src_j + 1 <= 2 and (
                        self._board[src_j + 1][src_i + 1] == 0 or self._board[src_j + 1][src_i + 1].get_team_type() != src_piece_team):
                    movable_pos_list.append((1, 1))
                if src_i + 1 <= 5 and src_j - 1 >= 0 and (
                        self._board[src_j - 1][src_i + 1] == 0 or self._board[src_j - 1][src_i + 1].get_team_type() != src_piece_team):
                    movable_pos_list.append((1, -1))
                if src_i - 1 >= 3 and src_j + 1 <= 2 and (
                        self._board[src_j + 1][src_i - 1] == 0 or self._board[src_j + 1][src_i - 1].get_team_type() != src_piece_team):
                    movable_pos_list.append((-1, 1))
                if src_i - 1 >= 3 and src_j - 1 >= 0 and (
                        self._board[src_j - 1][src_i - 1] == 0 or self._board[src_j - 1][src_i - 1].get_team_type() != src_piece_team):
                    movable_pos_list.append((-1, -1))
            if src_i + 1 <= 5 and (self._board[src_j][src_i + 1] == 0 or self._board[src_j][src_i].get_team_type() != src_piece_team):
                movable_pos_list.append((1, 0))
            if src_i - 1 >= 3 and (self._board[src_j][src_i - 1] == 0 or self._board[src_j][src_i].get_team_type() != src_piece_team):
                movable_pos_list.append((-1, 0))
        elif src_piece_type == 'R':
            for i in range(src_j + 1, 10):
                if self._board[i][src_i] == 0:
                    movable_pos_list.append((0, i - src_j))
                elif self._board[i][src_i].get_team_type() == src_piece_team:
                    break
                else:
                    movable_pos_list.append((0, i - src_j))
                    break
            for i in range(src_j - 1, -1, -1):
                if self._board[i][src_i] == 0:
                    movable_pos_list.append((0, i - src_j))
                elif self._board[i][src_i].get_team_type() == src_piece_team:
                    break
                else:
                    movable_pos_list.append((0, i - src_j))
                    break
            for i in range(src_i + 1, 9):
                if self._board[src_j][i] == 0:
                    movable_pos_list.append((i - src_i, 0))
                elif self._board[src_j][i].get_team_type() == src_piece_team:
                    break
                else:
                    movable_pos_list.append((i - src_i, 0))
                    break
            for i in range(src_i - 1, -1, -1):
                if self._board[src_j][i] == 0:
                    movable_pos_list.append((i - src_i, 0))
                elif self._board[src_j][i].get_team_type() == src_piece_team:
                    break
                else:
                    movable_pos_list.append((i - src_i, 0))
                    break
        elif src_piece_type == 'C':
            for i in range(src_j + 1, 10):
                if self._board[i][src_i] == 0:
                    continue
                elif self._board[i][src_i].get_piece_type() != 'C':
                    for j in range(i + 1, 10):
                        if self._board[j][src_i] == 0:
                            movable_pos_list.append((0, j - src_j))
                        elif self._board[j][src_i].get_team_type() == src_piece_team or self._board[j][src_i].get_team_type() == 'C':
                            break
                        else:
                            movable_pos_list.append((0, j - src_j))
                            break
                break
            for i in range(src_j - 1, -1, -1):
                if self._board[i][src_i] == 0:
                    continue
                elif self._board[i][src_i].get_piece_type() != 'C':
                    for j in range(i - 1, -1, -1):
                        if self._board[j][src_i] == 0:
                            movable_pos_list.append((0, j - src_j))
                        elif self._board[j][src_i].get_team_type() == src_piece_team or self._board[j][src_i].get_team_type() == 'C':
                            break
                        else:
                            movable_pos_list.append((0, j - src_j))
                            break
                break
            for i in range(src_i + 1, 9):
                if self._board[src_j][i] == 0:
                    continue
                elif self._board[src_j][i].get_piece_type() != 'C':
                    for j in range(i + 1, 9):
                        if self._board[src_j][j] == 0:
                            movable_pos_list.append((j - src_i, 0))
                        elif self._board[src_j][j].get_team_type() == src_piece_team or self._board[src_j][j].get_team_type() == 'C':
                            break
                        else:
                            movable_pos_list.append((j - src_i, 0))
                            break
                break
            for i in range(src_i - 1, -1, -1):
                if self._board[src_j][i] == 0:
                    continue
                elif self._board[src_j][i].get_piece_type() != 'C':
                    for j in range(i - 1, -1, -1):
                        if self._board[src_j][j] == 0:
                            movable_pos_list.append((j - src_i, 0))
                        elif self._board[src_j][j].get_team_type() == src_piece_team or self._board[src_j][j].get_team_type() == 'C':
                            break
                        else:
                            movable_pos_list.append((j - src_i, 0))
                            break
                break
        elif src_piece_type == 'N':
            if src_j + 2 <= 9 and self._board[src_j + 1][src_i] == 0:
                if src_i + 1 <= 8 and (
                        self._board[src_j + 2][src_i + 1] == 0 or self._board[src_j + 2][src_i + 1].get_team_type() != src_piece_team):
                    movable_pos_list.append((1, 2))
                if src_i - 1 >= 0 and (
                        self._board[src_j + 2][src_i - 1] == 0 or self._board[src_j + 2][src_i - 1].get_team_type() != src_piece_team):
                    movable_pos_list.append((-1, 2))
            if src_j - 2 >= 0 and self._board[src_j - 1][src_i] == 0:
                if src_i + 1 <= 8 and (
                        self._board[src_j - 2][src_i + 1] == 0 or self._board[src_j - 2][src_i + 1].get_team_type() != src_piece_team):
                    movable_pos_list.append((1, -2))
                if src_i - 1 >= 0 and (
                        self._board[src_j - 2][src_i - 1] == 0 or self._board[src_j - 2][src_i - 1].get_team_type() != src_piece_team):
                    movable_pos_list.append((-1, -2))
            if src_i + 2 <= 8 and self._board[src_j][src_i + 1] == 0:
                if src_j + 1 <= 9 and (
                        self._board[src_j + 1][src_i + 2] == 0 or self._board[src_j + 1][src_i + 2].get_team_type() != src_piece_team):
                    movable_pos_list.append((2, 1))
                if src_j - 1 >= 0 and (
                        self._board[src_j - 1][src_i + 2] == 0 or self._board[src_j - 1][src_i + 2].get_team_type() != src_piece_team):
                    movable_pos_list.append((2, -1))
            if src_i - 2 >= 0 and self._board[src_j][src_i - 1] == 0:
                if src_j + 1 <= 9 and (
                        self._board[src_j + 1][src_i - 2] == 0 or self._board[src_j + 1][src_i - 2].get_team_type() != src_piece_team):
                    movable_pos_list.append((-2, 1))
                if src_j - 1 >= 0 and (
                        self._board[src_j - 1][src_i - 2] == 0 or self._board[src_j - 1][src_i - 2].get_team_type() != src_piece_team):
                    movable_pos_list.append((-2, -1))
        elif src_piece_type == 'E':
            if src_j + 3 <= 9 and self._board[src_j + 1][src_i] == 0:
                if src_i + 2 <= 8 and self._board[src_j + 2][src_i + 1] == 0:
                    if self._board[src_j + 3][src_i + 2] == 0 or self._board[src_j + 3][src_i + 2].get_team_type() != src_piece_team:
                        movable_pos_list.append((2, 3))
                if src_i - 2 >= 0 and self._board[src_j + 2][src_i - 1] == 0:
                    if self._board[src_j + 3][src_i - 2] == 0 or self._board[src_j + 3][src_i - 2].get_team_type() != src_piece_team:
                        movable_pos_list.append((-2, 3))
            if src_j - 3 >= 0 and self._board[src_j - 1][src_i] == 0:
                if src_i + 2 <= 8 and self._board[src_j - 2][src_i + 1] == 0:
                    if self._board[src_j - 3][src_i + 2] == 0 or self._board[src_j - 3][src_i + 2].get_team_type() != src_piece_team:
                        movable_pos_list.append((2, -3))
                if src_i - 2 >= 0 and self._board[src_j - 2][src_i - 1] == 0:
                    if self._board[src_j - 3][src_i - 2] == 0 or self._board[src_j - 3][src_i - 2].get_team_type() != src_piece_team:
                        movable_pos_list.append((-2, -3))
            if src_i + 3 <= 8 and self._board[src_j][src_i + 1] == 0:
                if src_j + 2 <= 9 and self._board[src_j + 1][src_i + 2] == 0:
                    if self._board[src_j + 2][src_i + 3] == 0 or self._board[src_j + 2][src_i + 3].get_team_type() != src_piece_team:
                        movable_pos_list.append((3, 2))
                if src_j - 2 >= 0 and self._board[src_j - 1][src_i + 2] == 0:
                    if self._board[src_j - 2][src_i + 3] == 0 or self._board[src_j - 2][src_i + 3].get_team_type() != src_piece_team:
                        movable_pos_list.append((3, -2))
            if src_i - 3 >= 0 and self._board[src_j][src_i - 1] == 0:
                if src_j + 2 <= 9 and self._board[src_j + 1][src_i - 2] == 0:
                    if self._board[src_j + 2][src_i - 3] == 0 or self._board[src_j + 2][src_i - 3].get_team_type() != src_piece_team:
                        movable_pos_list.append((-3, 2))
                if src_j - 2 >= 0 and self._board[src_j - 1][src_i - 2] == 0:
                    if self._board[src_j - 2][src_i - 3] == 0 or self._board[src_j - 2][src_i - 3].get_team_type() != src_piece_team:
                        movable_pos_list.append((-3, -2))
        elif src_piece_type == 'P':
            if src_piece_team == BLUE_TEAM:
                if src_j - 1 >= 0 and (self._board[src_j - 1][src_i] == 0 or self._board[src_j - 1][src_i].get_team_type() == 2):
                    movable_pos_list.append((0, -1))
            else:
                if src_j + 1 <= 9 and (self._board[src_j + 1][src_i] == 0 or self._board[src_j + 1][src_i].get_team_type() == 1):
                    movable_pos_list.append((0, 1))
            if src_i + 1 <= 8 and (
                    self._board[src_j][src_i + 1] == 0 or self._board[src_j][src_i + 1].get_team_type() != src_piece_team):
                movable_pos_list.append((1, 0))
            if src_i - 1 >= 0 and (
                    self._board[src_j][src_i - 1] == 0 or self._board[src_j][src_i - 1].get_team_type() != src_piece_team):
                movable_pos_list.append((-1, 0))

        return movable_pos_list
