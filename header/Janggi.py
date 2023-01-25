from JanggiTeam import *
from pygame.locals import Rect


class Janggi:
    def __init__(self):
        self._red_team = JanggiTeam(RED_TEAM)
        self._blue_team = JanggiTeam(BLUE_TEAM)
        self._init_board()
        self._turn = BLUE_TEAM
        self._running = True
        self._Surface = pygame.display.set_mode((JANGGI_BOARD_WIDTH * MAGNIFICATION_RATIO,
                                                 JANGGI_BOARD_HEIGHT * MAGNIFICATION_RATIO))

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

    def calc_movable_values(self, src_piece: JanggiPiece) -> list[tuple[int, int]]:
        src_piece_type = src_piece.get_piece_type()
        src_piece_team_type = src_piece.get_team_type()
        src_i, src_j = src_piece.get_pos()
        movable_values = []

        if src_piece_type == KING or src_piece_type == GUARD:
            if src_piece_team_type == BLUE_TEAM:
                if src_j + 1 <= 9 and (
                        self._board[src_j + 1][src_i] == 0 or
                        self._board[src_j + 1][src_i].get_team_type() != src_piece_team_type):
                    if self.is_legal_move(src_piece, (0, 1)):
                        movable_values.append((0, 1))
                if src_j - 1 >= 7 and (
                        self._board[src_j - 1][src_i] == 0 or
                        self._board[src_j - 1][src_i].get_team_type() != src_piece_team_type):
                    if self.is_legal_move(src_piece, (0, -1)):
                        movable_values.append((0, -1))
                if src_i + 1 <= 5 and src_j + 1 <= 9 and (
                        self._board[src_j + 1][src_i + 1] == 0 or
                        self._board[src_j + 1][src_i + 1].get_team_type() != src_piece_team_type):
                    if self.is_legal_move(src_piece, (1, 1)):
                        movable_values.append((1, 1))
                if src_i + 1 <= 5 and src_j - 1 >= 7 and (
                        self._board[src_j - 1][src_i + 1] == 0 or
                        self._board[src_j - 1][src_i + 1].get_team_type() != src_piece_team_type):
                    if self.is_legal_move(src_piece, (1, -1)):
                        movable_values.append((1, -1))
                if src_i - 1 >= 3 and src_j + 1 <= 9 and (
                        self._board[src_j + 1][src_i - 1] == 0 or
                        self._board[src_j + 1][src_i - 1].get_team_type() != src_piece_team_type):
                    if self.is_legal_move(src_piece, (-1, 1)):
                        movable_values.append((-1, 1))
                if src_i - 1 >= 3 and src_j - 1 >= 7 and (
                        self._board[src_j - 1][src_i - 1] == 0 or
                        self._board[src_j - 1][src_i - 1].get_team_type() != src_piece_team_type):
                    if self.is_legal_move(src_piece, (-1, -1)):
                        movable_values.append((-1, -1))
            else:
                if src_j + 1 <= 2 and (
                        self._board[src_j + 1][src_i] == 0 or
                        self._board[src_j + 1][src_i].get_team_type() != src_piece_team_type):
                    if self.is_legal_move(src_piece, (0, 1)):
                        movable_values.append((0, 1))
                if src_j - 1 >= 0 and (
                        self._board[src_j - 1][src_i] == 0 or
                        self._board[src_j - 1][src_i].get_team_type() != src_piece_team_type):
                    if self.is_legal_move(src_piece, (0, -1)):
                        movable_values.append((0, -1))
                if src_i + 1 <= 5 and src_j + 1 <= 2 and (
                        self._board[src_j + 1][src_i + 1] == 0 or
                        self._board[src_j + 1][src_i + 1].get_team_type() != src_piece_team_type):
                    if self.is_legal_move(src_piece, (1, 1)):
                        movable_values.append((1, 1))
                if src_i + 1 <= 5 and src_j - 1 >= 0 and (
                        self._board[src_j - 1][src_i + 1] == 0 or
                        self._board[src_j - 1][src_i + 1].get_team_type() != src_piece_team_type):
                    if self.is_legal_move(src_piece, (1, -1)):
                        movable_values.append((1, -1))
                if src_i - 1 >= 3 and src_j + 1 <= 2 and (
                        self._board[src_j + 1][src_i - 1] == 0 or
                        self._board[src_j + 1][src_i - 1].get_team_type() != src_piece_team_type):
                    if self.is_legal_move(src_piece, (-1, 1)):
                        movable_values.append((-1, 1))
                if src_i - 1 >= 3 and src_j - 1 >= 0 and (
                        self._board[src_j - 1][src_i - 1] == 0 or
                        self._board[src_j - 1][src_i - 1].get_team_type() != src_piece_team_type):
                    if self.is_legal_move(src_piece, (-1, -1)):
                        movable_values.append((-1, -1))
            if src_i + 1 <= 5 and (
                    self._board[src_j][src_i + 1] == 0 or
                    self._board[src_j][src_i].get_team_type() != src_piece_team_type):
                if self.is_legal_move(src_piece, (1, 0)):
                    movable_values.append((1, 0))
            if src_i - 1 >= 3 and (
                    self._board[src_j][src_i - 1] == 0 or
                    self._board[src_j][src_i].get_team_type() != src_piece_team_type):
                if self.is_legal_move(src_piece, (-1, 0)):
                    movable_values.append((-1, 0))
        elif src_piece_type == ROOK:
            for j in range(src_j + 1, 10):
                if self._board[j][src_i] == 0:
                    if self.is_legal_move(src_piece, (0, j - src_j)):
                        movable_values.append((0, j - src_j))
                elif self._board[j][src_i].get_team_type() == src_piece_team_type:
                    break
                else:
                    if self.is_legal_move(src_piece, (0, j - src_j)):
                        movable_values.append((0, j - src_j))
                    break
            for j in range(src_j - 1, -1, -1):
                if self._board[j][src_i] == 0:
                    if self.is_legal_move(src_piece, (0, j - src_j)):
                        movable_values.append((0, j - src_j))
                elif self._board[j][src_i].get_team_type() == src_piece_team_type:
                    break
                else:
                    if self.is_legal_move(src_piece, (0, j - src_j)):
                        movable_values.append((0, j - src_j))
                    break
            for i in range(src_i + 1, 9):
                if self._board[src_j][i] == 0:
                    if self.is_legal_move(src_piece, (i - src_i, 0)):
                        movable_values.append((i - src_i, 0))
                elif self._board[src_j][i].get_team_type() == src_piece_team_type:
                    break
                else:
                    if self.is_legal_move(src_piece, (i - src_i, 0)):
                        movable_values.append((i - src_i, 0))
                    break
            for i in range(src_i - 1, -1, -1):
                if self._board[src_j][i] == 0:
                    if self.is_legal_move(src_piece, (i - src_i, 0)):
                        movable_values.append((i - src_i, 0))
                elif self._board[src_j][i].get_team_type() == src_piece_team_type:
                    break
                else:
                    if self.is_legal_move(src_piece, (i - src_i, 0)):
                        movable_values.append((i - src_i, 0))
                    break
        elif src_piece_type == CANNON:
            for i in range(src_j + 1, 10):
                if self._board[i][src_i] == 0:
                    continue
                elif self._board[i][src_i].get_piece_type() != CANNON:
                    for j in range(i + 1, 10):
                        if self._board[j][src_i] == 0:
                            if self.is_legal_move(src_piece, (0, j - src_j)):
                                movable_values.append((0, j - src_j))
                        elif self._board[j][src_i].get_team_type() == src_piece_team_type or \
                                self._board[j][src_i].get_piece_type() == CANNON:
                            break
                        else:
                            if self.is_legal_move(src_piece, (0, j - src_j)):
                                movable_values.append((0, j - src_j))
                            break
                break
            for i in range(src_j - 1, -1, -1):
                if self._board[i][src_i] == 0:
                    continue
                elif self._board[i][src_i].get_piece_type() != CANNON:
                    for j in range(i - 1, -1, -1):
                        if self._board[j][src_i] == 0:
                            if self.is_legal_move(src_piece, (0, j - src_j)):
                                movable_values.append((0, j - src_j))
                        elif self._board[j][src_i].get_team_type() == src_piece_team_type or \
                                self._board[j][src_i].get_piece_type() == CANNON:
                            break
                        else:
                            if self.is_legal_move(src_piece, (0, j - src_j)):
                                movable_values.append((0, j - src_j))
                            break
                break
            for i in range(src_i + 1, 9):
                if self._board[src_j][i] == 0:
                    continue
                elif self._board[src_j][i].get_piece_type() != CANNON:
                    for j in range(i + 1, 9):
                        if self._board[src_j][j] == 0:
                            if self.is_legal_move(src_piece, (j - src_i, 0)):
                                movable_values.append((j - src_i, 0))
                        elif self._board[src_j][j].get_team_type() == src_piece_team_type or \
                                self._board[src_j][j].get_piece_type() == CANNON:
                            break
                        else:
                            if self.is_legal_move(src_piece, (j - src_i, 0)):
                                movable_values.append((j - src_i, 0))
                            break
                break
            for i in range(src_i - 1, -1, -1):
                if self._board[src_j][i] == 0:
                    continue
                elif self._board[src_j][i].get_piece_type() != CANNON:
                    for j in range(i - 1, -1, -1):
                        if self._board[src_j][j] == 0:
                            if self.is_legal_move(src_piece, (j - src_i, 0)):
                                movable_values.append((j - src_i, 0))
                        elif self._board[src_j][j].get_team_type() == src_piece_team_type or \
                                self._board[src_j][j].get_piece_type() == CANNON:
                            break
                        else:
                            if self.is_legal_move(src_piece, (j - src_i, 0)):
                                movable_values.append((j - src_i, 0))
                            break
                break
        elif src_piece_type == KNIGHT:
            if src_j + 2 <= 9 and self._board[src_j + 1][src_i] == 0:
                if src_i + 1 <= 8 and (
                        self._board[src_j + 2][src_i + 1] == 0 or
                        self._board[src_j + 2][src_i + 1].get_team_type() != src_piece_team_type):
                    if self.is_legal_move(src_piece, (1, 2)):
                        movable_values.append((1, 2))
                if src_i - 1 >= 0 and (
                        self._board[src_j + 2][src_i - 1] == 0 or
                        self._board[src_j + 2][src_i - 1].get_team_type() != src_piece_team_type):
                    if self.is_legal_move(src_piece, (-1, 2)):
                        movable_values.append((-1, 2))
            if src_j - 2 >= 0 and self._board[src_j - 1][src_i] == 0:
                if src_i + 1 <= 8 and (
                        self._board[src_j - 2][src_i + 1] == 0 or
                        self._board[src_j - 2][src_i + 1].get_team_type() != src_piece_team_type):
                    if self.is_legal_move(src_piece, (1, -2)):
                        movable_values.append((1, -2))
                if src_i - 1 >= 0 and (
                        self._board[src_j - 2][src_i - 1] == 0 or
                        self._board[src_j - 2][src_i - 1].get_team_type() != src_piece_team_type):
                    if self.is_legal_move(src_piece, (-1, -2)):
                        movable_values.append((-1, -2))
            if src_i + 2 <= 8 and self._board[src_j][src_i + 1] == 0:
                if src_j + 1 <= 9 and (
                        self._board[src_j + 1][src_i + 2] == 0 or
                        self._board[src_j + 1][src_i + 2].get_team_type() != src_piece_team_type):
                    if self.is_legal_move(src_piece, (2, 1)):
                        movable_values.append((2, 1))
                if src_j - 1 >= 0 and (
                        self._board[src_j - 1][src_i + 2] == 0 or
                        self._board[src_j - 1][src_i + 2].get_team_type() != src_piece_team_type):
                    if self.is_legal_move(src_piece, (2, -1)):
                        movable_values.append((2, -1))
            if src_i - 2 >= 0 and self._board[src_j][src_i - 1] == 0:
                if src_j + 1 <= 9 and (
                        self._board[src_j + 1][src_i - 2] == 0 or
                        self._board[src_j + 1][src_i - 2].get_team_type() != src_piece_team_type):
                    if self.is_legal_move(src_piece, (-2, 1)):
                        movable_values.append((-2, 1))
                if src_j - 1 >= 0 and (
                        self._board[src_j - 1][src_i - 2] == 0 or
                        self._board[src_j - 1][src_i - 2].get_team_type() != src_piece_team_type):
                    if self.is_legal_move(src_piece, (-2, -1)):
                        movable_values.append((-2, -1))
        elif src_piece_type == ELEPHANT:
            if src_j + 3 <= 9 and self._board[src_j + 1][src_i] == 0:
                if src_i + 2 <= 8 and self._board[src_j + 2][src_i + 1] == 0:
                    if self._board[src_j + 3][src_i + 2] == 0 or \
                            self._board[src_j + 3][src_i + 2].get_team_type() != src_piece_team_type:
                        if self.is_legal_move(src_piece, (2, 3)):
                            movable_values.append((2, 3))
                if src_i - 2 >= 0 and self._board[src_j + 2][src_i - 1] == 0:
                    if self._board[src_j + 3][src_i - 2] == 0 or \
                            self._board[src_j + 3][src_i - 2].get_team_type() != src_piece_team_type:
                        if self.is_legal_move(src_piece, (-2, 3)):
                            movable_values.append((-2, 3))
            if src_j - 3 >= 0 and self._board[src_j - 1][src_i] == 0:
                if src_i + 2 <= 8 and self._board[src_j - 2][src_i + 1] == 0:
                    if self._board[src_j - 3][src_i + 2] == 0 or \
                            self._board[src_j - 3][src_i + 2].get_team_type() != src_piece_team_type:
                        if self.is_legal_move(src_piece, (2, -3)):
                            movable_values.append((2, -3))
                if src_i - 2 >= 0 and self._board[src_j - 2][src_i - 1] == 0:
                    if self._board[src_j - 3][src_i - 2] == 0 or \
                            self._board[src_j - 3][src_i - 2].get_team_type() != src_piece_team_type:
                        if self.is_legal_move(src_piece, (-2, -3)):
                            movable_values.append((-2, -3))
            if src_i + 3 <= 8 and self._board[src_j][src_i + 1] == 0:
                if src_j + 2 <= 9 and self._board[src_j + 1][src_i + 2] == 0:
                    if self._board[src_j + 2][src_i + 3] == 0 or \
                            self._board[src_j + 2][src_i + 3].get_team_type() != src_piece_team_type:
                        if self.is_legal_move(src_piece, (3, 2)):
                            movable_values.append((3, 2))
                if src_j - 2 >= 0 and self._board[src_j - 1][src_i + 2] == 0:
                    if self._board[src_j - 2][src_i + 3] == 0 or \
                            self._board[src_j - 2][src_i + 3].get_team_type() != src_piece_team_type:
                        if self.is_legal_move(src_piece, (3, -2)):
                            movable_values.append((3, -2))
            if src_i - 3 >= 0 and self._board[src_j][src_i - 1] == 0:
                if src_j + 2 <= 9 and self._board[src_j + 1][src_i - 2] == 0:
                    if self._board[src_j + 2][src_i - 3] == 0 or \
                            self._board[src_j + 2][src_i - 3].get_team_type() != src_piece_team_type:
                        if self.is_legal_move(src_piece, (-3, 2)):
                            movable_values.append((-3, 2))
                if src_j - 2 >= 0 and self._board[src_j - 1][src_i - 2] == 0:
                    if self._board[src_j - 2][src_i - 3] == 0 or \
                            self._board[src_j - 2][src_i - 3].get_team_type() != src_piece_team_type:
                        if self.is_legal_move(src_piece, (-3, -2)):
                            movable_values.append((-3, -2))
        elif src_piece_type == PAWN:
            if src_piece_team_type == BLUE_TEAM:
                if src_j - 1 >= 0 and (
                        self._board[src_j - 1][src_i] == 0 or
                        self._board[src_j - 1][src_i].get_team_type() == RED_TEAM):
                    if self.is_legal_move(src_piece, (0, -1)):
                        movable_values.append((0, -1))
            else:
                if src_j + 1 <= 9 and (
                        self._board[src_j + 1][src_i] == 0 or
                        self._board[src_j + 1][src_i].get_team_type() == BLUE_TEAM):
                    if self.is_legal_move(src_piece, (0, 1)):
                        movable_values.append((0, 1))
            if src_i + 1 <= 8 and (
                    self._board[src_j][src_i + 1] == 0 or
                    self._board[src_j][src_i + 1].get_team_type() != src_piece_team_type):
                if self.is_legal_move(src_piece, (1, 0)):
                    movable_values.append((1, 0))
            if src_i - 1 >= 0 and (
                    self._board[src_j][src_i - 1] == 0 or
                    self._board[src_j][src_i - 1].get_team_type() != src_piece_team_type):
                if self.is_legal_move(src_piece, (-1, 0)):
                    movable_values.append((-1, 0))

        return movable_values

    def put_piece(self, src_piece: JanggiPiece, dst_pos: tuple[int, int]):
        dst_piece = self.get_piece_from_board(dst_pos)

        src_piece.set_pos(dst_pos)
        if dst_piece != 0:
            dst_piece.set_alive(False)

        self._init_board()

    def restore_put_piece(self, src_piece: JanggiPiece, dst_piece, restore_pos: tuple[int, int]):
        src_piece.set_pos(restore_pos)
        if dst_piece != 0:
            dst_piece.set_alive(True)

        self._init_board()

    def is_legal_move(self, src_piece: JanggiPiece, move_value: tuple[int, int]):
        dst_pos = (src_piece.get_i() + move_value[0], src_piece.get_j() + move_value[1])
        restore_pos = src_piece.get_pos()
        dst_piece = self.get_piece_from_board(dst_pos)
        enemy_team_type = src_piece.get_team_type() % 2 + 1

        self.put_piece(src_piece, dst_pos)

        is_ally_cheked = self.is_enemy_checked(enemy_team_type)
        self.restore_put_piece(src_piece, dst_piece, restore_pos)
        if is_ally_cheked:
            return False
        else:
            return True

    def is_horizontal_clear(self, src_pos: tuple[int, int], dst_pos: tuple[int, int]) -> bool:
        i, src_j = src_pos
        _, dst_j = dst_pos
        min_j = min(src_j, dst_j)
        max_j = max(src_j, dst_j)
        for j in range(min_j + 1, max_j):
            if self._board[j][i] != 0:
                return False
        return True

    def is_vertical_clear(self, src_pos: tuple[int, int], dst_pos: tuple[int, int]) -> bool:
        src_i, j = src_pos
        dst_i, _ = dst_pos
        min_i = min(src_i, dst_i)
        max_i = max(src_i, dst_i)
        for i in range(min_i + 1, max_i):
            if self._board[j][i] != 0:
                return False
        return True

    def is_horizontal_clear_for_cannon(self, src_pos: tuple[int, int], dst_pos: tuple[int, int]) -> bool:
        i, src_j = src_pos
        _, dst_j = dst_pos
        min_j = min(src_j, dst_j)
        max_j = max(src_j, dst_j)
        piece_cnt = 0
        for j in range(min_j + 1, max_j):
            if self._board[j][i] != 0:
                if self._board[j][i].get_piece_type() == CANNON:
                    return False
                else:
                    piece_cnt += 1
        if piece_cnt == 1:
            return True
        else:
            return False

    def is_vertical_clear_for_cannon(self, src_pos: tuple[int, int], dst_pos: tuple[int, int]) -> bool:
        src_i, j = src_pos
        dst_i, _ = dst_pos
        min_i = min(src_i, dst_i)
        max_i = max(src_i, dst_i)
        piece_cnt = 0
        for i in range(min_i + 1, max_i):
            if self._board[j][i] != 0:
                if self._board[j][i].get_piece_type() == CANNON:
                    return False
                else:
                    piece_cnt += 1
        if piece_cnt == 1:
            return True
        else:
            return False

    def is_possible_to_attack(self, src_piece: JanggiPiece, dst_piece: JanggiPiece) -> bool:
        src_piece_type = src_piece.get_piece_type()
        src_piece_team = src_piece.get_team_type()
        dst_piece_team = dst_piece.get_team_type()
        src_i, src_j = src_piece.get_pos()
        dst_i, dst_j = dst_piece.get_pos()
        diff_i = dst_i - src_i
        diff_j = dst_j - src_j

        if src_piece_team == dst_piece_team:
            return False
        if diff_i == 0 and diff_j == 0:
            return False

        if src_piece_type == KING or src_piece_type == GUARD:
            if not 3 <= dst_i <= 5:
                return False
            if src_piece_team == BLUE_TEAM:
                if not 7 <= dst_j <= 9:
                    return False
            else:
                if not 0 <= dst_j <= 2:
                    return False
            if abs(diff_i) <= 1 and abs(diff_j) <= 1:
                return True
            else:
                return False
        elif src_piece_type == ROOK:
            is_horizontal = src_i == dst_i and src_j != dst_j
            is_vertical = src_i != dst_i and src_j == dst_j
            if not (is_horizontal or is_vertical):
                return False
            if is_horizontal:
                if self.is_horizontal_clear((src_i, src_j), (dst_i, dst_j)):
                    return True
            elif is_vertical:
                if self.is_vertical_clear((src_i, src_j), (dst_i, dst_j)):
                    return True
            return False
        elif src_piece_type == CANNON:
            is_horizontal = src_i == dst_i and src_j != dst_j
            is_vertical = src_i != dst_i and src_j == dst_j
            if not (is_horizontal or is_vertical):
                return False
            if is_horizontal:
                if self.is_horizontal_clear_for_cannon((src_i, src_j), (dst_i, dst_j)):
                    return True
            elif is_vertical:
                if self.is_vertical_clear_for_cannon((src_i, src_j), (dst_i, dst_j)):
                    return True
            return False
        elif src_piece_type == KNIGHT:
            if not ((abs(diff_i) == 2 and abs(diff_j) == 1) or (abs(diff_i) == 1 and abs(diff_j) == 2)):
                return False
            if abs(diff_i) == 2:
                if diff_i > 0:
                    if self._board[src_j][src_i + 1] != 0:
                        return False
                    else:
                        return True
                else:
                    if self._board[src_j][src_i - 1] != 0:
                        return False
                    else:
                        return True
            elif abs(diff_j) == 2:
                if diff_j > 0:
                    if self._board[src_j + 1][src_i] != 0:
                        return False
                    else:
                        return True
                else:
                    if self._board[src_j - 1][src_i] != 0:
                        return False
                    else:
                        return True
        elif src_piece_type == ELEPHANT:
            if not ((abs(diff_i) == 2 and abs(diff_j) == 3) or (abs(diff_i) == 3 and abs(diff_j) == 2)):
                return False
            if abs(diff_i) == 3:
                if diff_i > 0:
                    if self._board[src_j][src_i + 1] != 0:
                        return False
                    if diff_j > 0:
                        if self._board[src_j + 1][src_i + 2] != 0:
                            return False
                        else:
                            return True
                    else:
                        if self._board[src_j - 1][src_i + 2] != 0:
                            return False
                        else:
                            return True
                else:
                    if self._board[src_j][src_i - 1] != 0:
                        return False
                    if diff_j > 0:
                        if self._board[src_j + 1][src_i - 2] != 0:
                            return False
                        else:
                            return True
                    else:
                        if self._board[src_j - 1][src_i - 2] != 0:
                            return False
                        else:
                            return True
            elif abs(diff_j) == 3:
                if diff_j > 0:
                    if self._board[src_j + 1][src_i] != 0:
                        return False
                    if diff_i > 0:
                        if self._board[src_j + 2][src_i + 1] != 0:
                            return False
                        else:
                            return True
                    else:
                        if self._board[src_j + 2][src_i - 1] != 0:
                            return False
                        else:
                            return True
                else:
                    if self._board[src_j - 1][src_i] != 0:
                        return False
                    if diff_i > 0:
                        if self._board[src_j - 2][src_i + 1] != 0:
                            return False
                        else:
                            return True
                    else:
                        if self._board[src_j - 2][src_i - 1] != 0:
                            return False
                        else:
                            return True
        elif src_piece_type == PAWN:
            if not ((abs(diff_i) == 1 and abs(diff_j) == 0) or (abs(diff_i) == 0 and abs(diff_j) == 1)):
                return False
            if src_piece.get_team_type() == BLUE_TEAM:
                if diff_j > 0:
                    return False
            else:
                if diff_j < 0:
                    return False
            return True

    def is_enemy_checked(self, ally_team_type: str) -> bool:
        ally_pieces = self.get_team(ally_team_type).get_pieces()
        enemy_team_type = ally_team_type % 2 + 1
        enemy_king_piece = self.get_team(enemy_team_type).get_king_piece()

        for piece in ally_pieces:
            if piece.get_alive():
                is_possible_to_attack = self.is_possible_to_attack(piece, enemy_king_piece)
                if is_possible_to_attack:
                    return True

        return False

    def is_enemy_checkmate(self, ally_team_type: str) -> bool:
        enemy_team_type = ally_team_type % 2 + 1
        enemy_pieces = self.get_team(enemy_team_type).get_pieces()

        for piece in enemy_pieces:
            if piece.get_alive():
                movable_pos_list = self.calc_movable_values(piece)
                if movable_pos_list:
                    return False

        return True

    def get_piece_from_board(self, pos: tuple[int, int]):
        return self._board[pos[1]][pos[0]]

    def get_turn(self) -> str:
        return self._turn

    def get_next_turn(self) -> str:
        return self._turn % 2 + 1

    def set_turn_to_next(self):
        self._turn = self._turn % 2 + 1

    def get_team(self, team_type: str) -> JanggiTeam:
        return self._red_team if team_type == RED_TEAM else self._blue_team

    def get_board(self):
        return self._board

    def get_running(self) -> bool:
        return self._running

    def set_running(self, running: bool):
        self._running = running

    def show_board(self):
        self._Surface.fill(BACKGROUND_COLOR)

        for x in range(9):
            start_pos = [(CELL_WIDTH * x + WHITE_SPACE_WIDTH) * MAGNIFICATION_RATIO,
                         WHITE_SPACE_HEIGHT * MAGNIFICATION_RATIO]
            end_pos = [(CELL_WIDTH * x + WHITE_SPACE_WIDTH) * MAGNIFICATION_RATIO,
                       (JANGGI_BOARD_HEIGHT - WHITE_SPACE_HEIGHT) * MAGNIFICATION_RATIO]
            pygame.draw.line(self._Surface, BLACK_COLOR, start_pos, end_pos, 1)

        for y in range(10):
            start_pos = [WHITE_SPACE_WIDTH * MAGNIFICATION_RATIO,
                         (CELL_HEIGHT * y + WHITE_SPACE_HEIGHT) * MAGNIFICATION_RATIO]
            end_pos = [(JANGGI_BOARD_WIDTH - WHITE_SPACE_WIDTH) * MAGNIFICATION_RATIO,
                       (CELL_HEIGHT * y + WHITE_SPACE_HEIGHT) * MAGNIFICATION_RATIO]
            pygame.draw.line(self._Surface, BLACK_COLOR, start_pos, end_pos, 1)

        pygame.draw.line(self._Surface, BLACK_COLOR,
                         [(CELL_WIDTH * 3 + WHITE_SPACE_WIDTH) * MAGNIFICATION_RATIO,
                          WHITE_SPACE_HEIGHT * MAGNIFICATION_RATIO],
                         [(CELL_WIDTH * 5 + WHITE_SPACE_WIDTH) * MAGNIFICATION_RATIO,
                          (CELL_HEIGHT * 2 + WHITE_SPACE_HEIGHT) * MAGNIFICATION_RATIO], 1)
        pygame.draw.line(self._Surface, BLACK_COLOR,
                         [(CELL_WIDTH * 3 + WHITE_SPACE_WIDTH) * MAGNIFICATION_RATIO,
                          (CELL_HEIGHT * 2 + WHITE_SPACE_HEIGHT) * MAGNIFICATION_RATIO],
                         [(CELL_WIDTH * 5 + WHITE_SPACE_WIDTH) * MAGNIFICATION_RATIO,
                          WHITE_SPACE_HEIGHT * MAGNIFICATION_RATIO], 1)
        pygame.draw.line(self._Surface, BLACK_COLOR,
                         [(CELL_WIDTH * 3 + WHITE_SPACE_WIDTH) * MAGNIFICATION_RATIO,
                          (JANGGI_BOARD_HEIGHT - (CELL_HEIGHT * 2 + WHITE_SPACE_HEIGHT)) * MAGNIFICATION_RATIO],
                         [(CELL_WIDTH * 5 + WHITE_SPACE_WIDTH) * MAGNIFICATION_RATIO,
                          (JANGGI_BOARD_HEIGHT - WHITE_SPACE_HEIGHT) * MAGNIFICATION_RATIO], 1)
        pygame.draw.line(self._Surface, BLACK_COLOR,
                         [(CELL_WIDTH * 3 + WHITE_SPACE_WIDTH) * MAGNIFICATION_RATIO,
                          (JANGGI_BOARD_HEIGHT - WHITE_SPACE_HEIGHT) * MAGNIFICATION_RATIO],
                         [(CELL_WIDTH * 5 + WHITE_SPACE_WIDTH) * MAGNIFICATION_RATIO,
                          (JANGGI_BOARD_HEIGHT - (CELL_HEIGHT * 2 + WHITE_SPACE_HEIGHT)) * MAGNIFICATION_RATIO], 1)

        for piece in self._red_team.get_pieces():
            if piece.get_alive():
                self.draw_piece(piece)
        for piece in self._blue_team.get_pieces():
            if piece.get_alive():
                self.draw_piece(piece)

        pygame.display.update()

    def show_movable_pos(self, selected_piece: JanggiPiece, movable_pos_list: list[tuple[int, int]]):
        i, j = selected_piece.get_pos()
        w = JANGGI_KING_PIECE_SIZE * MAGNIFICATION_RATIO
        h = JANGGI_KING_PIECE_SIZE * MAGNIFICATION_RATIO
        for (mi, mj) in movable_pos_list:
            x = ((i + mi) * CELL_WIDTH + WHITE_SPACE_WIDTH - JANGGI_KING_PIECE_SIZE / 2) * MAGNIFICATION_RATIO
            y = ((j + mj) * CELL_HEIGHT + WHITE_SPACE_HEIGHT - JANGGI_KING_PIECE_SIZE / 2) * MAGNIFICATION_RATIO
            pygame.draw.rect(self._Surface, (255, 0, 0), Rect(x, y, w, h), 2)

        x = (i * CELL_WIDTH + WHITE_SPACE_WIDTH - JANGGI_KING_PIECE_SIZE / 2) * MAGNIFICATION_RATIO
        y = (j * CELL_HEIGHT + WHITE_SPACE_HEIGHT - JANGGI_KING_PIECE_SIZE / 2) * MAGNIFICATION_RATIO
        pygame.draw.rect(self._Surface, (255, 0, 0), Rect(x, y, w, h), 2)

        pygame.display.update()

    def draw_piece(self, piece: JanggiPiece):
        img = piece.get_img()
        i, j = piece.get_pos()
        w, h = img.get_width(), img.get_height()
        self._Surface.blit(img, ((i * CELL_WIDTH + WHITE_SPACE_WIDTH) * MAGNIFICATION_RATIO - w / 2,
                                 (j * CELL_HEIGHT + WHITE_SPACE_HEIGHT) * MAGNIFICATION_RATIO - h / 2))

# 추가 구현해야 할 점
# 1. 함수 맹글링
# 2. is_*_clear, is_*_clear_for_cannon 함수 없애기
# 3. calc_movable_pos, is_possible_to_attack 함수 다듬기
