import pygame, copy
from janggi_const import *
from pygame.locals import Rect

class Piece:
    def __init__(self, piece_type: str, team_type: int, pos: tuple[int, int], img_path: str):
        self._piece_type = piece_type
        self._team_type = team_type
        self._pos = pos
        self._alive = True

        if piece_type == KING:
            self._score = 1.5 if team_type == RED_TEAM else 0
        elif piece_type == ROOK:
            self._score = 13
        elif piece_type == CANNON:
            self._score = 7
        elif piece_type == KNIGHT:
            self._score = 5
        elif piece_type == ELEPHANT or piece_type == GUARD:
            self._score = 3
        else:
            self._score = 2

        if piece_type == KING:
            piece_size = JANGGI_KING_PIECE_SIZE
        elif piece_type == GUARD or piece_type == PAWN:
            piece_size = JANGGI_SMALL_PIECE_SIZE
        else:
            piece_size = JANGGI_BIG_PIECE_SIZE

        self._img = pygame.transform.scale(pygame.image.load(img_path), (piece_size * MAGNIFICATION_RATIO,
                                                                         piece_size * MAGNIFICATION_RATIO))

    def get_piece_type(self) -> str:
        return self._piece_type

    def get_team_type(self) -> str:
        return self._team_type

    def get_pos(self) -> tuple[int, int]:
        return self._pos

    def set_pos(self, pos: tuple[int, int]):
        self._pos = pos

    def get_img(self) -> pygame.Surface:
        return self._img

    def get_alive(self) -> bool:
        return self._alive

    def set_alive(self, alive: bool):
        self._alive = alive

    def get_score(self) -> int:
        return self._score


class Team:
    def __init__(self, team_type: int):
        self._team_type = team_type
        self._pieces = []
        self._init_pieces()

    def _init_pieces(self):
        if self._team_type == RED_TEAM:
            for i in range(5):
                self._pieces.append(Piece(PAWN, RED_TEAM, (2 * i, 3), RED_PAWN_IMG_PATH))
            for i in range(2):
                self._pieces.append(Piece(ROOK, RED_TEAM, (i * 8, 0), RED_ROOK_IMG_PATH))
                self._pieces.append(Piece(CANNON, RED_TEAM, (i * 6 + 1, 2), RED_CANNON_IMG_PATH))
                self._pieces.append(Piece(KNIGHT, RED_TEAM, (i * 6 + 1, 0), RED_KNIGHT_IMG_PATH))
                self._pieces.append(Piece(ELEPHANT, RED_TEAM, (i * 4 + 2, 0), RED_ELEPHANT_IMG_PATH))
                self._pieces.append(Piece(GUARD, RED_TEAM, (i * 2 + 3, 0), RED_GUARD_IMG_PATH))
            self._pieces.append(Piece(KING, RED_TEAM, (4, 1), RED_KING_IMG_PATH))
        else:
            for i in range(5):
                self._pieces.append(Piece(PAWN, BLUE_TEAM, (2 * i, 6), BLUE_PAWN_IMG_PATH))
            for i in range(2):
                self._pieces.append(Piece(ROOK, BLUE_TEAM, (i * 8, 9), BLUE_ROOK_IMG_PATH))
                self._pieces.append(Piece(CANNON, BLUE_TEAM, (i * 6 + 1, 7), BLUE_CANNON_IMG_PATH))
                self._pieces.append(Piece(KNIGHT, BLUE_TEAM, (i * 5 + 1, 9), BLUE_KNIGHT_IMG_PATH))
                self._pieces.append(Piece(ELEPHANT, BLUE_TEAM, (i * 5 + 2, 9), BLUE_ELEPHANT_IMG_PATH))
                self._pieces.append(Piece(GUARD, BLUE_TEAM, (i * 2 + 3, 9), BLUE_GUARD_IMG_PATH))
            self._pieces.append(Piece(KING, BLUE_TEAM, (4, 8), BLUE_KING_IMG_PATH))

    def get_pieces(self) -> list[Piece]:
        return self._pieces

    def get_alive_pieces(self) -> list[Piece]:
        alive_pieces = []
        for piece in self._pieces:
            if piece.get_alive():
                alive_pieces.append(piece)
        return alive_pieces

    def get_total_piece_score(self):
        total_piece_score = 0
        for piece in self._pieces:
            if piece.get_alive():
                total_piece_score += piece.get_score()

        return total_piece_score

    def get_king_piece(self) -> Piece:
        return self._pieces[-1]

class Game:
    def __init__(self):
        self._red_team = Team(RED_TEAM)
        self._blue_team = Team(BLUE_TEAM)
        self._init_board()
        self._turn = BLUE_TEAM
        self._running = True
        self._Surface = pygame.display.set_mode((JANGGI_BOARD_WIDTH * MAGNIFICATION_RATIO,
                                                 JANGGI_BOARD_HEIGHT * MAGNIFICATION_RATIO))
        print(type(self._Surface))

    def _init_board(self):
        self._board = [[0] * 9 for _ in range(10)]

        for piece in self._red_team.get_alive_pieces():
            i, j = piece.get_pos()
            self._board[j][i] = piece

        for piece in self._blue_team.get_alive_pieces():
            i, j = piece.get_pos()
            self._board[j][i] = piece

    def is_possible_king_and_guard_move(self, src_piece: Piece, move_value: tuple[int, int]) -> bool:
        if not ((abs(move_value[0]) == 0 or abs(move_value[0]) == 1) and
                (abs(move_value[1]) == 0 or abs(move_value[1]) == 1)):
            return False

        src_pos = src_piece.get_pos()
        dst_pos = (src_pos[0] + move_value[0], src_pos[1] + move_value[1])
        if not is_pos_in_fortress(dst_pos):
            return False

        dst_piece = self._board[dst_pos[1]][dst_pos[0]]
        if isinstance(dst_piece, Piece):
            if src_piece.get_team_type() == dst_piece.get_team_type():
                return False

        fortress_center = (4, 8) if src_piece.get_team_type() == BLUE_TEAM else (4, 1)
        if abs(move_value[0]) == 1 and abs(move_value[1]) == 1:
            if src_pos == fortress_center or dst_pos == fortress_center:
                return True
            else:
                return False
        if abs(move_value[0]) + abs(move_value[1]) == 1:
            return True

        return False

    def is_possible_diagonal_rook_move(self, src_piece: Piece, move_value: tuple[int, int]):
        if not (abs(move_value[0]) == abs(move_value[1]) and (abs(move_value[0]) == 1 or abs(move_value[0]) == 2)):
            return False

        src_pos = src_piece.get_pos()
        dst_pos = (src_pos[0] + move_value[0], src_pos[1] + move_value[1])
        if not (is_pos_in_fortress(src_pos) and
                is_pos_in_fortress(dst_pos)):
            return False

        dst_piece = self._board[dst_pos[1]][dst_pos[0]]
        if isinstance(dst_piece, Piece):
            if src_piece.get_team_type() == dst_piece.get_team_type():
                return False

        fortress_center = (4, 1) if 0 <= src_pos[1] <= 2 else (4, 8)
        if abs(move_value[0]) == 2:
            fortress_center_piece = self._board[fortress_center[1]][fortress_center[0]]
            if fortress_center_piece == 0:
                return True
            if isinstance(fortress_center_piece, Piece):
                return False
        if abs(move_value[0]) == 1:
            if src_pos == fortress_center:
                return True
            if dst_pos == fortress_center:
                return True
            else:
                return False

    def is_possible_diagonal_cannon_move(self, src_piece: Piece, move_value: tuple[int, int]):
        if not (abs(move_value[0]) == abs(move_value[1]) and abs(move_value[0]) == 2):
            return False

        src_pos = src_piece.get_pos()
        dst_pos = (src_pos[0] + move_value[0], src_pos[1] + move_value[1])
        if not (is_pos_in_fortress(src_pos) and
                is_pos_in_fortress(dst_pos)):
            return False

        dst_piece = self._board[dst_pos[1]][dst_pos[0]]
        if isinstance(dst_piece, Piece):
            if src_piece.get_team_type() == dst_piece.get_team_type():
                return False

        fortress_center = (4, 1) if 0 <= src_pos[1] <= 2 else (4, 8)
        fortress_center_piece = self._board[fortress_center[1]][fortress_center[0]]
        if fortress_center_piece == 0:
            return False
        if isinstance(fortress_center_piece, Piece) and fortress_center_piece.get_piece_type() != CANNON:
            return True
        else:
            return False

    def is_possible_knight_move(self, src_piece: Piece, move_value: tuple[int, int]) -> bool:
        if not ((abs(move_value[0]) == 2 and abs(move_value[1]) == 1) or
                (abs(move_value[0]) == 1 and abs(move_value[1]) == 2)):
            return False

        src_pos = src_piece.get_pos()
        dst_pos = (src_pos[0] + move_value[0], src_pos[1] + move_value[1])
        if not is_pos_in_board(dst_pos):
            return False

        dst_piece = self._board[dst_pos[1]][dst_pos[0]]
        if isinstance(dst_piece, Piece):
            if src_piece.get_team_type() == dst_piece.get_team_type():
                return False

        if abs(move_value[0]) == 2:
            if move_value[0] > 0:
                if isinstance(self._board[src_pos[1]][src_pos[0] + 1], Piece):
                    return False
                else:
                    return True
            else:
                if isinstance(self._board[src_pos[1]][src_pos[0] - 1], Piece):
                    return False
                else:
                    return True
        if abs(move_value[1]) == 2:
            if move_value[1] > 0:
                if isinstance(self._board[src_pos[1] + 1][src_pos[0]], Piece):
                    return False
                else:
                    return True
            else:
                if isinstance(self._board[src_pos[1] - 1][src_pos[0]], Piece):
                    return False
                else:
                    return True

    def is_possible_elephant_move(self, src_piece: Piece, move_value: tuple[int, int]) -> bool:
        if not ((abs(move_value[0]) == 3 and abs(move_value[1]) == 2) or
                (abs(move_value[0]) == 2 and abs(move_value[1]) == 3)):
            return False

        src_pos = src_piece.get_pos()
        dst_pos = (src_pos[0] + move_value[0], src_pos[1] + move_value[1])
        if not is_pos_in_board(dst_pos):
            return False

        dst_piece = self._board[dst_pos[1]][dst_pos[0]]
        if isinstance(dst_piece, Piece):
            if src_piece.get_team_type() == dst_piece.get_team_type():
                return False

        if abs(move_value[0]) == 3:
            if move_value[0] > 0:
                if isinstance(self._board[src_pos[1]][src_pos[0] + 1], Piece):
                    return False
                if move_value[1] > 0:
                    if isinstance(self._board[src_pos[1] + 1][src_pos[0] + 2], Piece):
                        return False
                    else:
                        return True
                else:
                    if isinstance(self._board[src_pos[1] - 1][src_pos[0] + 2], Piece):
                        return False
                    else:
                        return True
            else:
                if isinstance(self._board[src_pos[1]][src_pos[0] - 1], Piece):
                    return False
                if move_value[1] > 0:
                    if isinstance(self._board[src_pos[1] + 1][src_pos[0] - 2], Piece):
                        return False
                    else:
                        return True
                else:
                    if isinstance(self._board[src_pos[1] - 1][src_pos[0] - 2], Piece):
                        return False
                    else:
                        return True
        if abs(move_value[1]) == 3:
            if move_value[1] > 0:
                if isinstance(self._board[src_pos[1] + 1][src_pos[0]], Piece):
                    return False
                if move_value[0] > 0:
                    if isinstance(self._board[src_pos[1] + 2][src_pos[0] + 1], Piece):
                        return False
                    else:
                        return True
                else:
                    if isinstance(self._board[src_pos[1] + 2][src_pos[0] - 1], Piece):
                        return False
                    else:
                        return True
            else:
                if isinstance(self._board[src_pos[1] - 1][src_pos[0]], Piece):
                    return False
                if move_value[0] > 0:
                    if isinstance(self._board[src_pos[1] - 2][src_pos[0] + 1], Piece):
                        return False
                    else:
                        return True
                else:
                    if isinstance(self._board[src_pos[1] - 2][src_pos[0] - 1], Piece):
                        return False
                    else:
                        return True

    def is_possible_pawn_move(self, src_piece: Piece, move_value: tuple[int, int]) -> bool:
        if not ((abs(move_value[0]) == 0 or abs(move_value[0]) == 1) and
                (abs(move_value[1]) == 0 or abs(move_value[1]) == 1)):
            return False
        if (src_piece.get_team_type() == BLUE_TEAM and move_value[1] > 0) or \
                (src_piece.get_team_type() == RED_TEAM and move_value[1] < 0):
            return False

        src_pos = src_piece.get_pos()
        dst_pos = (src_pos[0] + move_value[0], src_pos[1] + move_value[1])
        if not is_pos_in_board(dst_pos):
            return False

        dst_piece = self._board[dst_pos[1]][dst_pos[0]]
        if isinstance(dst_piece, Piece):
            if src_piece.get_team_type() == dst_piece.get_team_type():
                return False

        fortress_center = (4, 8) if src_piece.get_team_type() == RED_TEAM else (4, 1)
        if abs(move_value[0]) == 1 and abs(move_value[1]) == 1:
            if src_pos == fortress_center or dst_pos == fortress_center:
                return True
            else:
                return False
        if abs(move_value[0]) + abs(move_value[1]) == 1:
            return True

        return False

    def is_possible_to_attack(self, src_piece: Piece, dst_piece: Piece) -> bool:
        # src_piece가 dst_piece를 공격 가능한지 검사
        # 거의 대부분 적의 왕을 타격할 수 있는지 검사할 때 이 함수를 사용
        src_piece_type = src_piece.get_piece_type()
        src_piece_team = src_piece.get_team_type()
        dst_piece_team = dst_piece.get_team_type()
        src_pos = src_piece.get_pos()
        dst_pos = dst_piece.get_pos()
        diff_pos = (dst_pos[0] - src_pos[0], dst_pos[1] - src_pos[1])

        if src_piece_team == dst_piece_team:
            return False
        if diff_pos == (0, 0):
            return False

        if src_piece_type == KING or src_piece_type == GUARD:
            if self.is_possible_king_and_guard_move(src_piece, diff_pos):
                return True
            else:
                return False
        elif src_piece_type == ROOK:
            is_horizontal = diff_pos[0] != 0 and diff_pos[1] == 0
            is_vertical = diff_pos[0] == 0 and diff_pos[1] != 0
            is_diagonal = abs(diff_pos[0]) == abs(diff_pos[1])
            if is_horizontal:
                min_i = min(src_pos[0], dst_pos[0])
                max_i = max(src_pos[0], dst_pos[0])
                for i in range(min_i + 1, max_i):
                    if isinstance(self._board[src_pos[1]][i], Piece):
                        return False
                return True
            elif is_vertical:
                min_j = min(src_pos[1], dst_pos[1])
                max_j = max(src_pos[1], dst_pos[1])
                for j in range(min_j + 1, max_j):
                    if isinstance(self._board[j][src_pos[0]], Piece):
                        return False
                return True
            elif is_diagonal:
                if self.is_possible_diagonal_rook_move(src_piece, diff_pos):
                    return True
                else:
                    return False
            else:
                return False
        elif src_piece_type == CANNON:
            is_horizontal = diff_pos[0] != 0 and diff_pos[1] == 0
            is_vertical = diff_pos[0] == 0 and diff_pos[1] != 0
            is_diagonal = abs(diff_pos[0]) == abs(diff_pos[1])
            piece_cnt = 0
            if is_horizontal:
                min_i = min(src_pos[0], dst_pos[0])
                max_i = max(src_pos[0], dst_pos[0])
                for i in range(min_i + 1, max_i):
                    if isinstance(self._board[src_pos[1]][i], Piece):
                        if self._board[src_pos[1]][i].get_piece_type() == CANNON:
                            return False
                        else:
                            piece_cnt += 1
                if piece_cnt == 1:
                    return True
                else:
                    return False
            elif is_vertical:
                min_j = min(src_pos[1], dst_pos[1])
                max_j = max(src_pos[1], dst_pos[1])
                for j in range(min_j + 1, max_j):
                    if isinstance(self._board[j][src_pos[0]], Piece):
                        if self._board[j][src_pos[0]].get_piece_type() == CANNON:
                            return False
                        else:
                            piece_cnt += 1
                if piece_cnt == 1:
                    return True
                else:
                    return False
            elif is_diagonal:
                if self.is_possible_diagonal_cannon_move(src_piece, diff_pos):
                    return True
                else:
                    return False
            else:
                return False
        elif src_piece_type == KNIGHT:
            if self.is_possible_knight_move(src_piece, diff_pos):
                return True
            else:
                return False
        elif src_piece_type == ELEPHANT:
            if self.is_possible_elephant_move(src_piece, diff_pos):
                return True
            else:
                return False
        elif src_piece_type == PAWN:
            if self.is_possible_pawn_move(src_piece, diff_pos):
                return True
            else:
                return False

    def is_checked(self, ally_team_type: int) -> bool:
        # 적이 장군 상태인지 검사
        ally_king_piece = self.get_team(ally_team_type).get_king_piece()
        enemy_team_type = ally_team_type % 2 + 1
        enemy_pieces = self.get_team(enemy_team_type).get_alive_pieces()

        for piece in enemy_pieces:
            is_possible_to_attack = self.is_possible_to_attack(piece, ally_king_piece)
            if is_possible_to_attack:
                return True

        return False

    def is_checkmate(self, ally_team_type: int) -> bool:
        ally_pieces = self.get_team(ally_team_type).get_alive_pieces()

        for piece in ally_pieces:
            movable_pos_list = self.calc_movable_values(piece)
            if movable_pos_list:
                return False

        return True

    def is_game_over(self) -> int:
        if self.is_checked(self._turn):
            if self.is_checkmate(self._turn):
                return 2
            else:
                return 1

        return 0

    def is_legal_move(self, src_piece: Piece, move_value: tuple[int, int]):
        # 수를 놓았을 때 자신이 장군 상태가 된다면 그 수는 불법(?)적인 수
        src_pos = src_piece.get_pos()
        dst_pos = (src_pos[0] + move_value[0], src_pos[1] + move_value[1])
        dst_piece = self._board[dst_pos[1]][dst_pos[0]]
        ally_team_type = src_piece.get_team_type()

        self.put_piece(src_piece, dst_pos)
        is_ally_checked = self.is_checked(ally_team_type)
        self.restore_put_piece(src_piece, dst_piece, src_pos)

        if is_ally_checked:
            return False
        else:
            return True

    def calc_movable_values(self, src_piece: Piece) -> list[tuple[int, int]]:
        # src_piece가 이동할 수 있는 위치를 계산
        src_piece_type = src_piece.get_piece_type()
        src_piece_team_type = src_piece.get_team_type()
        src_i, src_j = src_piece.get_pos()
        movable_values = []

        if src_piece_type == KING or src_piece_type == GUARD:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if self.is_possible_king_and_guard_move(src_piece, (i, j)) and self.is_legal_move(src_piece, (i, j)):
                        movable_values.append((i, j))
        elif src_piece_type == ROOK:
            for j in range(src_j + 1, 10):
                if isinstance(self._board[j][src_i], Piece):
                    if self._board[j][src_i].get_team_type() != src_piece_team_type and \
                            self.is_legal_move(src_piece, (0, j - src_j)):
                        movable_values.append((0, j - src_j))
                    break
                if self.is_legal_move(src_piece, (0, j - src_j)):
                    movable_values.append((0, j - src_j))
            for j in range(src_j - 1, -1, -1):
                if isinstance(self._board[j][src_i], Piece):
                    if self._board[j][src_i].get_team_type() != src_piece_team_type and \
                            self.is_legal_move(src_piece, (0, j - src_j)):
                        movable_values.append((0, j - src_j))
                    break
                if self.is_legal_move(src_piece, (0, j - src_j)):
                    movable_values.append((0, j - src_j))
            for i in range(src_i + 1, 9):
                if isinstance(self._board[src_j][i], Piece):
                    if self._board[src_j][i].get_team_type() != src_piece_team_type and \
                            self.is_legal_move(src_piece, (i - src_i, 0)):
                        movable_values.append((i - src_i, 0))
                    break
                if self.is_legal_move(src_piece, (i - src_i, 0)):
                    movable_values.append((i - src_i, 0))
            for i in range(src_i - 1, -1, -1):
                if isinstance(self._board[src_j][i], Piece):
                    if self._board[src_j][i].get_team_type() != src_piece_team_type and \
                            self.is_legal_move(src_piece, (i - src_i, 0)):
                        movable_values.append((i - src_i, 0))
                    break
                if self.is_legal_move(src_piece, (i - src_i, 0)):
                    movable_values.append((i - src_i, 0))
            for i in range(1, 3):
                for _ in range(2):
                    i *= -1
                    j = i
                    for _ in range(2):
                        j *= -1
                        if self.is_possible_diagonal_rook_move(src_piece, (i, j)) and \
                                self.is_legal_move(src_piece, (i, j)):
                            movable_values.append((i, j))
        elif src_piece_type == CANNON:
            for j in range(src_j + 1, 10):
                if not isinstance(self._board[j][src_i], Piece):
                    continue
                elif self._board[j][src_i].get_piece_type() == CANNON:
                    break
                else:
                    for k in range(j + 1, 10):
                        if not isinstance(self._board[k][src_i], Piece):
                            if self.is_legal_move(src_piece, (0, k - src_j)):
                                movable_values.append((0, k - src_j))
                        elif self._board[k][src_i].get_team_type() == src_piece_team_type or \
                                self._board[k][src_i].get_piece_type() == CANNON:
                            break
                        else:
                            if self.is_legal_move(src_piece, (0, k - src_j)):
                                movable_values.append((0, k - src_j))
                            break
                    break
            for j in range(src_j - 1, -1, -1):
                if not isinstance(self._board[j][src_i], Piece):
                    continue
                elif self._board[j][src_i].get_piece_type() == CANNON:
                    break
                else:
                    for k in range(j - 1, -1, -1):
                        if not isinstance(self._board[k][src_i], Piece):
                            if self.is_legal_move(src_piece, (0, k - src_j)):
                                movable_values.append((0, k - src_j))
                        elif self._board[k][src_i].get_team_type() == src_piece_team_type or \
                                self._board[k][src_i].get_piece_type() == CANNON:
                            break
                        else:
                            if self.is_legal_move(src_piece, (0, k - src_j)):
                                movable_values.append((0, k - src_j))
                            break
                    break
            for i in range(src_i + 1, 9):
                if not isinstance(self._board[src_j][i], Piece):
                    continue
                elif self._board[src_j][i].get_piece_type() == CANNON:
                    break
                else:
                    for k in range(i + 1, 9):
                        if not isinstance(self._board[src_j][k], Piece):
                            if self.is_legal_move(src_piece, (k - src_i, 0)):
                                movable_values.append((k - src_i, 0))
                        elif self._board[src_j][k].get_team_type() == src_piece_team_type or \
                                self._board[src_j][k].get_piece_type() == CANNON:
                            break
                        else:
                            if self.is_legal_move(src_piece, (k - src_i, 0)):
                                movable_values.append((k - src_i, 0))
                            break
                    break
            for i in range(src_i - 1, -1, -1):
                if not isinstance(self._board[src_j][i], Piece):
                    continue
                elif self._board[src_j][i].get_piece_type() == CANNON:
                    break
                else:
                    for k in range(i - 1, -1, -1):
                        if self._board[src_j][k] == 0:
                            if self.is_legal_move(src_piece, (k - src_i, 0)):
                                movable_values.append((k - src_i, 0))
                        elif self._board[src_j][k].get_team_type() == src_piece_team_type or \
                                self._board[src_j][k].get_piece_type() == CANNON:
                            break
                        else:
                            if self.is_legal_move(src_piece, (k - src_i, 0)):
                                movable_values.append((k - src_i, 0))
                            break
                    break
            i = 2
            for _ in range(2):
                i *= -1
                j = i
                for _ in range(2):
                    j *= -1
                    if self.is_possible_diagonal_cannon_move(src_piece, (i, j)) and \
                            self.is_legal_move(src_piece, (i, j)):
                        movable_values.append((i, j))
        elif src_piece_type == KNIGHT:
            # 바보같은 코드 (반복문으로 하면 되는데..)
            if self.is_possible_knight_move(src_piece, (1, 2)) and self.is_legal_move(src_piece, (1, 2)):
                movable_values.append((1, 2))
            if self.is_possible_knight_move(src_piece, (1, -2)) and self.is_legal_move(src_piece, (1, -2)):
                movable_values.append((1, -2))
            if self.is_possible_knight_move(src_piece, (-1, 2)) and self.is_legal_move(src_piece, (-1, 2)):
                movable_values.append((-1, 2))
            if self.is_possible_knight_move(src_piece, (-1, -2)) and self.is_legal_move(src_piece, (-1, -2)):
                movable_values.append((-1, -2))
            if self.is_possible_knight_move(src_piece, (2, 1)) and self.is_legal_move(src_piece, (2, 1)):
                movable_values.append((2, 1))
            if self.is_possible_knight_move(src_piece, (2, -1)) and self.is_legal_move(src_piece, (2, -1)):
                movable_values.append((2, -1))
            if self.is_possible_knight_move(src_piece, (-2, 1)) and self.is_legal_move(src_piece, (-2, 1)):
                movable_values.append((-2, 1))
            if self.is_possible_knight_move(src_piece, (-2, -1)) and self.is_legal_move(src_piece, (-2, -1)):
                movable_values.append((-2, -1))
        elif src_piece_type == ELEPHANT:
            # 바보같은 코드 (반복문으로 하면 되는데..)
            if self.is_possible_elephant_move(src_piece, (2, 3)) and self.is_legal_move(src_piece, (2, 3)):
                movable_values.append((2, 3))
            if self.is_possible_elephant_move(src_piece, (2, -3)) and self.is_legal_move(src_piece, (2, -3)):
                movable_values.append((2, -3))
            if self.is_possible_elephant_move(src_piece, (-2, 3)) and self.is_legal_move(src_piece, (-2, 3)):
                movable_values.append((-2, 3))
            if self.is_possible_elephant_move(src_piece, (-2, -3)) and self.is_legal_move(src_piece, (-2, -3)):
                movable_values.append((-2, -3))
            if self.is_possible_elephant_move(src_piece, (3, 2)) and self.is_legal_move(src_piece, (3, 2)):
                movable_values.append((3, 2))
            if self.is_possible_elephant_move(src_piece, (3, -2)) and self.is_legal_move(src_piece, (3, -2)):
                movable_values.append((3, -2))
            if self.is_possible_elephant_move(src_piece, (-3, 2)) and self.is_legal_move(src_piece, (-3, 2)):
                movable_values.append((-3, 2))
            if self.is_possible_elephant_move(src_piece, (-3, -2)) and self.is_legal_move(src_piece, (-3, -2)):
                movable_values.append((-3, -2))
        elif src_piece_type == PAWN:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if self.is_possible_pawn_move(src_piece, (i, j)) and self.is_legal_move(src_piece, (i, j)):
                        movable_values.append((i, j))

        return movable_values

    def put_piece(self, src_piece: Piece, dst_pos: tuple[int, int]):
        # 장기말을 dst_pos 위치로 이동
        dst_piece = self._board[dst_pos[1]][dst_pos[0]]

        src_piece.set_pos(dst_pos)
        if isinstance(dst_piece, Piece):
            dst_piece.set_alive(False)

        self._init_board()

    def restore_put_piece(self, src_piece: Piece, dst_piece, restore_pos: tuple[int, int]):
        # 장기말을 이동시켰던 것을 다시 원상복구 시키는 함수
        src_piece.set_pos(restore_pos)
        if isinstance(dst_piece, Piece):
            dst_piece.set_alive(True)

        self._init_board()

    def get_piece_from_board(self, pos: tuple[int, int]):
        return self._board[pos[1]][pos[0]]

    def get_turn(self) -> str:
        return self._turn

    def set_turn_to_next(self):
        self._turn = self._turn % 2 + 1

    def get_team(self, team_type: int) -> Team:
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

        for piece in self._red_team.get_alive_pieces():
            self.draw_piece(piece)
        for piece in self._blue_team.get_alive_pieces():
            self.draw_piece(piece)

        pygame.display.update()

    def show_movable_pos(self, selected_piece: Piece, movable_pos_list: list[tuple[int, int]]):
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

    def show_ai_move_pos(self, move_pos: tuple[int, int]):
        i, j = move_pos
        x = (i * CELL_WIDTH + WHITE_SPACE_WIDTH - JANGGI_KING_PIECE_SIZE / 2) * MAGNIFICATION_RATIO
        y = (j * CELL_HEIGHT + WHITE_SPACE_HEIGHT - JANGGI_KING_PIECE_SIZE / 2) * MAGNIFICATION_RATIO
        w = JANGGI_KING_PIECE_SIZE * MAGNIFICATION_RATIO
        h = JANGGI_KING_PIECE_SIZE * MAGNIFICATION_RATIO
        pygame.draw.rect(self._Surface, (0, 0, 255), Rect(x, y, w, h), 2)

        pygame.display.update()

    def draw_piece(self, piece: Piece):
        img = piece.get_img()
        i, j = piece.get_pos()
        w, h = img.get_width(), img.get_height()
        self._Surface.blit(img, ((i * CELL_WIDTH + WHITE_SPACE_WIDTH) * MAGNIFICATION_RATIO - w / 2,
                                 (j * CELL_HEIGHT + WHITE_SPACE_HEIGHT) * MAGNIFICATION_RATIO - h / 2))

    def get_mcts_pick(self) -> tuple[int, Piece, tuple[int, int]]:
        ai_turn = self.get_turn()
        child_actions = []
        pieces = self.get_team(ai_turn).get_alive_pieces()
        for piece in pieces:
            movable_values = self.calc_movable_values(piece)
            child_actions.append(movable_values)

        result_dst_positions = [0 for _ in range(len(pieces))]
        winning_rates = [-1 for _ in range(len(pieces))]
        for i, src_piece in enumerate(pieces):
            movable_values = child_actions[i]
            for movable_value in movable_values:
                copy_game = copy.deepcopy(self)
                src_pos = piece.get_pos()
                dst_pos = (src_pos[0] + movable_value[0], src_pos[1] + movable_value[1])
                copy_game.put_piece(src_piece, dst_pos)

                winning_rate, k = 0, 100
                for _ in range(k):
                    winning_rate += simulation(copy_game)

                if winning_rates[i] < winning_rate:
                    winning_rates[i] = winning_rate
                    result_dst_positions[i] = dst_pos

                del copy_game

        max_winning_rate = -1
        for i in range(len(pieces)):
            if max_winning_rate < winning_rates[i]:
                max_winning_rate = winning_rates[i]
                result_piece = pieces[i]
                result_dst_pos = result_dst_positions[i]

        return max_winning_rate, result_piece, result_dst_pos


    # max, min 함수
    def max(self, depth: int, alpha: int, beta: int) -> tuple[int, Piece, tuple[int, int]]:
        if depth >= 3:
            return self._red_team.get_total_piece_score() - self._blue_team.get_total_piece_score(), None, (0, 0)

        ally_turn = RED_TEAM
        if self.is_checkmate(ally_turn):
            return -999, None, (0, 0)

        max_performance_value = -99999
        for piece in self.get_team(ally_turn).get_pieces():
            if piece.get_alive():
                for i, j in self.calc_movable_values(piece):
                    src_pos = piece.get_pos()
                    dst_pos = (i + src_pos[0], j + src_pos[1])
                    dst_piece = self._board[dst_pos[1]][dst_pos[0]]
                    self.put_piece(piece, dst_pos)
                    performance_value, _, _ = self.min(depth + 1, alpha, beta)
                    if performance_value > max_performance_value:
                        max_performance_value = performance_value
                        max_piece = piece
                        max_i, max_j = i, j
                    self.restore_put_piece(piece, dst_piece, src_pos)

                    max_pos = max_piece.get_pos()
                    if max_performance_value >= beta:
                        return max_performance_value, max_piece, (max_i + max_pos[0], max_j + max_pos[1])

                    if max_performance_value > alpha:
                        alpha = max_performance_value

        max_pos = max_piece.get_pos()
        return max_performance_value, max_piece, (max_i + max_pos[0], max_j + max_pos[1])

    def min(self, depth: int, alpha: int, beta: int) -> tuple[int, Piece, tuple[int, int]]:
        if depth >= 3:
            # 인공지능 팀이 바뀌면 수정해야 됨
            return self._red_team.get_total_piece_score() - self._blue_team.get_total_piece_score(), None, (0, 0)

        ally_turn = BLUE_TEAM
        if self.is_checkmate(ally_turn):
            return 999, None, (0, 0)

        min_performance_value = 99999
        for piece in self.get_team(ally_turn).get_pieces():
            if piece.get_alive():
                for i, j in self.calc_movable_values(piece):
                    src_pos = piece.get_pos()
                    dst_pos = (i + src_pos[0], j + src_pos[1])
                    dst_piece = self._board[dst_pos[1]][dst_pos[0]]
                    self.put_piece(piece, dst_pos)
                    performance_value, _, _ = self.max(depth + 1, alpha, beta)
                    if performance_value < min_performance_value:
                        min_performance_value = performance_value
                        min_piece = piece
                        min_i, min_j = i, j
                    self.restore_put_piece(piece, dst_piece, src_pos)

                    min_pos = min_piece.get_pos()
                    if min_performance_value <= alpha:
                        return min_performance_value, min_piece, (min_i + min_pos[0], min_j + min_pos[1])

                    if min_performance_value < beta:
                        beta = min_performance_value

        min_pos = min_piece.get_pos()
        return min_performance_value, min_piece, (min_i + min_pos[0], min_j + min_pos[1])


def is_pos_in_fortress(pos: tuple[int, int]) -> bool:
    # pos가 궁성 안에 있는지 검사
    if not ((3 <= pos[0] <= 5) and ((7 <= pos[1] <= 9) or (0 <= pos[1] <= 2))):
        return False
    else:
        return True


def is_pos_in_board(pos: tuple[int, int]) -> bool:
    # pos가 장기판 안에 있는지 검사
    if not ((0 <= pos[0] <= 8) and (0 <= pos[1] <= 9)):
        return False
    else:
        return True


# def simulation(game: Game):


# 추가 구현해야 할 점
# 1. 함수 맹글링
