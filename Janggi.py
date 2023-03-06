import pygame, copy, random
from Janggi_utils import *
from janggi_const import *
from pygame.locals import Rect


class Piece:
    def __init__(self, piece_type: str, team_type: int, score: int, pos: tuple[int, int]):
        self._piece_type = piece_type
        self._team_type = team_type
        self._score = score
        self._pos = pos
        self._alive = True

    def get_piece_type(self) -> str:
        return self._piece_type

    def get_team_type(self) -> str:
        return self._team_type

    def get_score(self) -> int:
        return self._score

    def get_pos(self) -> tuple[int, int]:
        return self._pos

    def set_pos(self, pos: tuple[int, int]):
        self._pos = pos

    def is_alive(self) -> bool:
        return self._alive

    def set_alive(self, alive: bool):
        self._alive = alive


class Team:
    def __init__(self, team_type: int, board_setting_type: int, piece_setting_type: int):
        self._team_type = team_type
        self._board_setting_type = board_setting_type
        self._pieces_setting_type = piece_setting_type
        self._pieces = []
        self._init_pieces()

    def _init_pieces(self):
        base_y_pos = 9 if (self._team_type == BLUE_TEAM and self._board_setting_type == BOTTOM_BLUE) or \
                          (self._team_type == RED_TEAM and self._board_setting_type == BOTTOM_RED) else 0
        y_direction = 1 if base_y_pos == 0 else -1

        pieces_settings = {
            LEFT_ELEPHANT_SETTING: (2, 1, 5, 5),
            OUTSIDE_ELEPHANT_SETTING: (2, 1, 4, 6),
            RIGHT_ELEPHANT_SETTING: (1, 2, 5, 5),
            INSIDE_ELEPHANT_SETTING: (1, 2, 6, 4)
        }
        base_knight_x_pos, base_elephant_x_pos, diff_between_knights, diff_between_elephants = \
            pieces_settings[self._pieces_setting_type]

        for i in range(5):
            self._pieces.append(Piece(PAWN, self._team_type, 2, (2 * i, base_y_pos + y_direction * 3)))
        for i in range(2):
            self._pieces.append(Piece(ROOK, self._team_type, 13, (i * 8, base_y_pos)))
            self._pieces.append(Piece(CANNON, self._team_type, 7, (i * 6 + 1, base_y_pos + y_direction * 2)))
            self._pieces.append(Piece(KNIGHT, self._team_type, 5,
                                      (i * diff_between_knights + base_knight_x_pos, base_y_pos)))
            self._pieces.append(Piece(ELEPHANT, self._team_type, 3,
                                      (i * diff_between_elephants + base_elephant_x_pos, base_y_pos)))
            self._pieces.append(Piece(GUARD, self._team_type, 3, (i * 2 + 3, base_y_pos)))
        self._pieces.append(Piece(KING, self._team_type, 0, (4, base_y_pos + y_direction)))

    def get_alive_pieces(self) -> list[Piece]:
        return [piece for piece in self._pieces if piece.is_alive()]

    def get_total_alive_piece_score(self) -> float:
        total_piece_score = 1.5 if self._team_type == RED_TEAM else 0
        alive_pieces_score = [piece.get_score() for piece in self._pieces if piece.is_alive()]
        total_piece_score += sum(alive_pieces_score)
        return total_piece_score

    def get_king_piece(self) -> Piece:
        return self._pieces[-1]


class Game:
    def __init__(self, board_setting_type: int, blue_team_piece_setting_type: int, red_team_piece_setting_type: int):
        self._red_team = Team(RED_TEAM, board_setting_type, red_team_piece_setting_type)
        self._blue_team = Team(BLUE_TEAM, board_setting_type, blue_team_piece_setting_type)
        self._board = []
        self.update_board()
        self._current_turn = BLUE_TEAM
        self._games_played = 0
        self._running = True

    def update_board(self):
        self._board = [[0] * 9 for _ in range(10)]

        for piece in self._red_team.get_alive_pieces():
            i, j = piece.get_pos()
            self._board[j][i] = piece

        for piece in self._blue_team.get_alive_pieces():
            i, j = piece.get_pos()
            self._board[j][i] = piece

    def is_possible_king_and_guard_move(self, src_piece: Piece, move_value: tuple[int, int]) -> bool:
        x, y = move_value
        dst_pos = tuple(sum(elem) for elem in zip(src_piece.get_pos(), move_value))
        fortress_center = (4, 8) if src_piece.get_team_type() == BLUE_TEAM else (4, 1)

        # 예외 처리
        if not (abs(x) <= 1 and abs(y) <= 1):
            return False
        if not is_in_fortress(dst_pos):
            return False
        dst_piece = self._board[dst_pos[1]][dst_pos[0]]
        if isinstance(dst_piece, Piece) and src_piece.get_team_type() == dst_piece.get_team_type():
            return False

        # 예외 통과
        if abs(x) == abs(y) == 1:
            if src_piece.get_pos() == fortress_center or dst_pos == fortress_center:
                return True
            else:
                return False
        if abs(x) + abs(y) == 1:
            return True

        return False

    def is_possible_diagonal_rook_move(self, src_piece: Piece, move_value: tuple[int, int]):
        x, y = move_value
        src_pos = src_piece.get_pos()
        dst_pos = tuple(sum(elem) for elem in zip(src_pos, move_value))
        fortress_center = (4, 1) if 0 <= src_pos[1] <= 2 else (4, 8)

        # 예외 처리
        if not (abs(x) == abs(y) and (abs(x) == 1 or abs(x) == 2)):
            return False
        if not (is_in_fortress(src_pos) and is_in_fortress(dst_pos)):
            return False
        dst_piece = self._board[dst_pos[1]][dst_pos[0]]
        if isinstance(dst_piece, Piece) and src_piece.get_team_type() == dst_piece.get_team_type():
            return False

        # 예외 통과
        if abs(x) == 2:
            fortress_center_piece = self._board[fortress_center[1]][fortress_center[0]]
            if not isinstance(fortress_center_piece, Piece):
                return True
            else:
                return False
        else:
            if src_pos == fortress_center or dst_pos == fortress_center:
                return True
            else:
                return False

    def is_possible_diagonal_cannon_move(self, src_piece: Piece, move_value: tuple[int, int]):
        x, y = move_value
        src_pos = src_piece.get_pos()
        dst_pos = tuple(sum(elem) for elem in zip(src_pos, move_value))
        fortress_center = (4, 1) if 0 <= src_pos[1] <= 2 else (4, 8)
        fortress_center_piece = self._board[fortress_center[1]][fortress_center[0]]

        # 예외 처리
        if not (abs(x) == abs(y) == 2):
            return False
        if not (is_in_fortress(src_pos) and is_in_fortress(dst_pos)):
            return False
        dst_piece = self._board[dst_pos[1]][dst_pos[0]]
        if isinstance(dst_piece, Piece) and src_piece.get_team_type() == dst_piece.get_team_type():
            return False

        # 예외 통과
        if isinstance(fortress_center_piece, Piece) and fortress_center_piece.get_piece_type() != CANNON:
            return True
        else:
            return False

    def is_possible_knight_move(self, src_piece: Piece, move_value: tuple[int, int]) -> bool:
        x, y = move_value
        src_pos = src_piece.get_pos()
        dst_pos = tuple(sum(elem) for elem in zip(src_pos, move_value))

        # 예외 처리
        if not ((abs(x) == 2 and abs(y) == 1) or (abs(x) == 1 and abs(y) == 2)):
            return False
        if not is_in_board(dst_pos):
            return False
        dst_piece = self._board[dst_pos[1]][dst_pos[0]]
        if isinstance(dst_piece, Piece) and src_piece.get_team_type() == dst_piece.get_team_type():
            return False

        # 예외 통과
        if abs(x) == 2:
            return not isinstance(self._board[src_pos[1]][src_pos[0] + x // 2], Piece)
        else:
            return not isinstance(self._board[src_pos[1] + y // 2][src_pos[0]], Piece)

    def is_possible_elephant_move(self, src_piece: Piece, move_value: tuple[int, int]) -> bool:
        x, y = move_value
        src_pos = src_piece.get_pos()
        dst_pos = tuple(sum(elem) for elem in zip(src_pos, move_value))

        # 예외 처리
        if not ((abs(x) == 3 and abs(y) == 2) or (abs(x) == 2 and abs(y) == 3)):
            return False
        if not is_in_board(dst_pos):
            return False
        dst_piece = self._board[dst_pos[1]][dst_pos[0]]
        if isinstance(dst_piece, Piece) and src_piece.get_team_type() == dst_piece.get_team_type():
            return False

        # 예외 통과
        if abs(x) == 3:
            if isinstance(self._board[src_pos[1]][src_pos[0] + x // 3], Piece):
                return False
            if isinstance(self._board[src_pos[1] + y // 2][src_pos[0] + x * 2 // 3], Piece):
                return False
        else:
            if isinstance(self._board[src_pos[1] + y // 3][src_pos[0]], Piece):
                return False
            if isinstance(self._board[src_pos[1] + y * 2 // 3][src_pos[0] + x // 2], Piece):
                return False

        return True

    def is_possible_pawn_move(self, src_piece: Piece, move_value: tuple[int, int]) -> bool:
        x, y = move_value
        src_pos = src_piece.get_pos()
        dst_pos = tuple(sum(elem) for elem in zip(src_pos, move_value))
        fortress_center = (4, 8) if src_piece.get_team_type() == RED_TEAM else (4, 1)

        # 예외 처리
        if not (abs(x) <= 1 and abs(y) <= 1):
            return False
        if (src_piece.get_team_type() == BLUE_TEAM and y > 0) or (src_piece.get_team_type() == RED_TEAM and y < 0):
            return False
        if not is_in_board(dst_pos):
            return False
        dst_piece = self._board[dst_pos[1]][dst_pos[0]]
        if isinstance(dst_piece, Piece) and src_piece.get_team_type() == dst_piece.get_team_type():
            return False

        # 예외 통과
        if abs(x) == 1 and abs(y) == 1:
            return src_pos == fortress_center or dst_pos == fortress_center

        return abs(x) + abs(y) == 1

    def is_possible_to_attack(self, src_piece: Piece, target_piece: Piece) -> bool:
        src_piece_type = src_piece.get_piece_type()
        src_piece_team = src_piece.get_team_type()
        target_piece_team = target_piece.get_team_type()
        src_pos = src_piece.get_pos()
        target_pos = target_piece.get_pos()
        diff_pos = tuple(elem[0] - elem[1] for elem in zip(target_pos, src_pos))

        # 예외 상황
        if src_piece_team == target_piece_team:
            return False
        if not target_piece.is_alive():
            return False

        # 예외 통과
        if src_piece_type in [KING, GUARD]:
            return self.is_possible_king_and_guard_move(src_piece, diff_pos)
        elif src_piece_type == ROOK:
            is_horizontal = diff_pos[0] != 0 and diff_pos[1] == 0
            is_vertical = diff_pos[0] == 0 and diff_pos[1] != 0
            is_diagonal = abs(diff_pos[0]) == abs(diff_pos[1])
            if is_horizontal:
                min_i, max_i = min(src_pos[0], target_pos[0]), max(src_pos[0], target_pos[0])
                return all(not isinstance(self._board[src_pos[1]][i], Piece) for i in range(min_i + 1, max_i))
            elif is_vertical:
                min_j, max_j = min(src_pos[1], target_pos[1]), max(src_pos[1], target_pos[1])
                return all(not isinstance(self._board[j][src_pos[0]], Piece) for j in range(min_j + 1, max_j))
            elif is_diagonal:
                return self.is_possible_diagonal_rook_move(src_piece, diff_pos)
            else:
                return False
        elif src_piece_type == CANNON:
            is_horizontal = diff_pos[0] != 0 and diff_pos[1] == 0
            is_vertical = diff_pos[0] == 0 and diff_pos[1] != 0
            is_diagonal = abs(diff_pos[0]) == abs(diff_pos[1])

            if is_horizontal:
                min_i, max_i = min(src_pos[0], target_pos[0]), max(src_pos[0], target_pos[0])
                inside_pieces = [ele for ele in self._board[src_pos[1]][min_i + 1:max_i] if isinstance(ele, Piece)]
                if len(inside_pieces) == 1 and inside_pieces[0].get_piece_type() != CANNON:
                    return True
                return False
            elif is_vertical:
                min_j, max_j = min(src_pos[1], target_pos[1]), max(src_pos[1], target_pos[1])
                inside_pieces = [row[src_pos[0]] for row in self._board[min_j + 1:max_j]
                                 if isinstance(row[src_pos[0]], Piece)]
                if len(inside_pieces) == 1 and inside_pieces[0].get_piece_type() != CANNON:
                    return True
                return False
            elif is_diagonal:
                return self.is_possible_diagonal_cannon_move(src_piece, diff_pos)
            else:
                return False
        elif src_piece_type == KNIGHT:
            return self.is_possible_knight_move(src_piece, diff_pos)
        elif src_piece_type == ELEPHANT:
            return self.is_possible_elephant_move(src_piece, diff_pos)
        elif src_piece_type == PAWN:
            return self.is_possible_pawn_move(src_piece, diff_pos)

    def is_check(self, ally_team_type: int) -> bool:
        ally_king_piece = self.get_team(ally_team_type).get_king_piece()
        enemy_team_type = (ally_team_type + 1) % 2
        enemy_pieces = self.get_team(enemy_team_type).get_alive_pieces()

        return any(self.is_possible_to_attack(enemy_piece, ally_king_piece) for enemy_piece in enemy_pieces)

    def is_checkmate(self, ally_team_type: int) -> bool:
        ally_pieces = self.get_team(ally_team_type).get_alive_pieces()

        return all(not self.calc_movable_values(piece) for piece in ally_pieces)

    def is_game_over(self) -> bool:
        team = self.get_team(self._current_turn)

        if not team.get_king_piece().is_alive() or self._games_played >= 200 \
                or (self.is_check(self._current_turn) and self.is_checkmate(self._current_turn)):
            return True

        return False

    def is_legal_move(self, src_piece: Piece, move_value: tuple[int, int]) -> bool:
        # 수를 놓았을 때 자신이 장군 상태가 된다면 그 수는 불법(?)적인 수
        src_pos = src_piece.get_pos()
        dst_pos = (src_pos[0] + move_value[0], src_pos[1] + move_value[1])
        dst_piece = self._board[dst_pos[1]][dst_pos[0]]
        ally_team_type = src_piece.get_team_type()

        self.put_piece(src_piece, dst_pos)
        is_ally_checked = self.is_check(ally_team_type)
        self.restore_put_piece(src_piece, dst_piece, src_pos)

        return not is_ally_checked

    def calc_movable_values(self, src_piece: Piece) -> list[tuple[int, int]]:
        # src_piece가 이동할 수 있는 위치를 계산
        src_piece_type = src_piece.get_piece_type()
        src_piece_team_type = src_piece.get_team_type()
        src_x, src_y = src_piece.get_pos()
        movable_values = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        diagonal_directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        if src_piece_type == KING or src_piece_type == GUARD:
            for dx, dy in directions + diagonal_directions:
                if self.is_possible_king_and_guard_move(src_piece, (dx, dy)) \
                        and self.is_legal_move(src_piece, (dx, dy)):
                    movable_values.append((dx, dy))
        elif src_piece_type == ROOK:
            for dx, dy in directions:
                for i in range(1, 10):
                    target_x, target_y = src_x + dx * i, src_y + dy * i
                    if not is_in_board((target_x, target_y)):
                        break
                    target_piece = self._board[target_y][target_x]
                    if isinstance(target_piece, Piece):
                        if target_piece.get_team_type() != src_piece_team_type and \
                                self.is_legal_move(src_piece, (dx * i, dy * i)):
                            movable_values.append((dx * i, dy * i))
                        break
                    if self.is_legal_move(src_piece, (dx * i, dy * i)):
                        movable_values.append((dx * i, dy * i))

            for dx, dy in diagonal_directions:
                for i in range(1, 3):
                    if self.is_possible_diagonal_rook_move(src_piece, (dx * i, dy * i)) and \
                            self.is_legal_move(src_piece, (dx * i, dy * i)):
                        movable_values.append((dx * i, dy * i))
        elif src_piece_type == CANNON:
            for dx, dy in directions:
                is_cannon_jumped = False
                for i in range(1, 10):
                    target_x, target_y = src_x + dx * i, src_y + dy * i
                    if not is_in_board((target_x, target_y)):
                        break
                    target_piece = self._board[target_y][target_x]
                    if is_cannon_jumped:
                        if isinstance(target_piece, Piece):
                            if not (target_piece.get_team_type() == src_piece_team_type or
                                    target_piece.get_piece_type() == CANNON) and \
                                    self.is_legal_move(src_piece, (dx * i, dy * i)):
                                movable_values.append((dx * i, dy * i))
                            break
                        else:
                            if self.is_legal_move(src_piece, (dx * i, dy * i)):
                                movable_values.append((dx * i, dy * i))
                    else:
                        if isinstance(target_piece, Piece):
                            if target_piece.get_piece_type() == CANNON:
                                break
                            else:
                                is_cannon_jumped = True

            for dx, dy in diagonal_directions:
                if self.is_possible_diagonal_cannon_move(src_piece, (dx, dy)) and \
                        self.is_legal_move(src_piece, (dx, dy)):
                    movable_values.append((dx, dy))
        elif src_piece_type == KNIGHT:
            knight_moves = [(1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1)]
            for move in knight_moves:
                if self.is_possible_knight_move(src_piece, move) and self.is_legal_move(src_piece, move):
                    movable_values.append(move)
        elif src_piece_type == ELEPHANT:
            elephant_moves = [(2, 3), (2, -3), (-2, 3), (-2, -3), (3, 2), (3, -2), (-3, 2), (-3, -2)]
            for move in elephant_moves:
                if self.is_possible_elephant_move(src_piece, move) and self.is_legal_move(src_piece, move):
                    movable_values.append(move)
        elif src_piece_type == PAWN:
            for dx, dy in directions + diagonal_directions:
                if self.is_possible_pawn_move(src_piece, (dx, dy)) and self.is_legal_move(src_piece, (dx, dy)):
                    movable_values.append((dx, dy))

        return movable_values

    def put_piece(self, src_piece: Piece, dst_pos: tuple[int, int]):
        # 장기말을 dst_pos 위치로 이동
        src_piece.set_pos(dst_pos)

        dst_piece = self._board[dst_pos[1]][dst_pos[0]]
        if isinstance(dst_piece, Piece):
            dst_piece.set_alive(False)

        self.update_board()

    def restore_put_piece(self, src_piece: Piece, dst_piece, restore_pos: tuple[int, int]):
        # 장기말을 이동시켰던 것을 다시 원상복구 시키는 함수
        src_piece.set_pos(restore_pos)

        if isinstance(dst_piece, Piece):
            dst_piece.set_alive(True)

        self.update_board()

    def get_piece_from_board(self, pos: tuple[int, int]):
        return self._board[pos[1]][pos[0]]

    def get_current_turn(self) -> str:
        return self._current_turn

    def switch_current_turn(self):
        self._current_turn = (self._current_turn + 1) % 2

    def get_games_played(self) -> int:
        return self._games_played

    def increment_games_played(self):
        self._games_played += 1

    def get_team(self, team_type: int) -> Team:
        return self._red_team if team_type == RED_TEAM else self._blue_team

    def get_board(self):
        return self._board

    def is_running(self) -> bool:
        return self._running

    def set_running(self, running: bool):
        self._running = running

    # max, min 함수
    # def max_random(self, depth: int) -> tuple[int, Piece, tuple[int, int]]:
    #     ally_turn = RED_TEAM
    #     enemy_turn = BLUE_TEAM
    #     if self.is_check(ally_turn) and self.is_checkmate(ally_turn):
    #         return -999, None, (0, 0)
    #     if depth >= 2:
    #         return self._red_team.get_total_alive_piece_score() - self._blue_team.get_total_alive_piece_score(), None, (0, 0)
    #
    #     candidate_results = []
    #     max_performance_value = -900
    #     for piece in self.get_team(ally_turn).get_alive_pieces():
    #         for i, j in self.calc_movable_values(piece):
    #             src_pos = piece.get_pos()
    #             dst_pos = (i + src_pos[0], j + src_pos[1])
    #             dst_piece = self._board[dst_pos[1]][dst_pos[0]]
    #             self.put_piece(piece, dst_pos)
    #             performance_value, _, _ = self.min_random(depth + 1)
    #             if self.is_check(enemy_turn):
    #                 performance_value += 0.005
    #             if isinstance(dst_piece, Piece):
    #                 if dst_piece.get_piece_type() == KING:
    #                     performance_value += 500
    #                 performance_value += 0.01
    #             if performance_value >= max_performance_value:
    #                 if performance_value > max_performance_value:
    #                     candidate_results.clear()
    #                 max_performance_value = performance_value
    #                 max_piece = piece
    #                 max_dst_pos = dst_pos
    #                 candidate_results.append((max_performance_value, max_piece, max_dst_pos))
    #             self.restore_put_piece(piece, dst_piece, src_pos)
    #
    #     if max_performance_value == -900:
    #         return -900, None, None
    #
    #     rand_num = random.randrange(0, len(candidate_results))
    #     return candidate_results[rand_num]
    #
    # def min_random(self, depth: int) -> tuple[int, Piece, tuple[int, int]]:
    #     ally_turn = BLUE_TEAM
    #     enemy_turn = RED_TEAM
    #     if self.is_check(ally_turn) and self.is_checkmate(ally_turn):
    #         return 999, None, (0, 0)
    #     if depth >= 2:
    #         return self._red_team.get_total_alive_piece_score() - self._blue_team.get_total_alive_piece_score(), None, (0, 0)
    #
    #     candidate_results = []
    #     min_performance_value = 900
    #     for piece in self.get_team(ally_turn).get_alive_pieces():
    #         for i, j in self.calc_movable_values(piece):
    #             src_pos = piece.get_pos()
    #             dst_pos = (i + src_pos[0], j + src_pos[1])
    #             dst_piece = self._board[dst_pos[1]][dst_pos[0]]
    #             self.put_piece(piece, dst_pos)
    #             performance_value, _, _ = self.max_random(depth + 1)
    #             if self.is_check(enemy_turn):
    #                 performance_value -= 0.005
    #             if isinstance(dst_piece, Piece):
    #                 if dst_piece.get_piece_type() == KING:
    #                     performance_value += 500
    #                 performance_value -= 0.01
    #             if performance_value <= min_performance_value:
    #                 if performance_value < min_performance_value:
    #                     candidate_results.clear()
    #                 min_performance_value = performance_value
    #                 min_piece = piece
    #                 min_dst_pos = dst_pos
    #                 candidate_results.append((min_performance_value, min_piece, min_dst_pos))
    #             self.restore_put_piece(piece, dst_piece, src_pos)
    #
    #     if min_performance_value == 900:
    #         return 900, None, None
    #
    #     rand_num = random.randrange(0, len(candidate_results))
    #     return candidate_results[rand_num]
    #
    # def max_alpha_beta(self, depth: int, alpha: int, beta: int) -> tuple[int, Piece, tuple[int, int]]:
    #     ally_turn = RED_TEAM
    #     enemy_turn = BLUE_TEAM
    #     if self.is_check(ally_turn) and self.is_checkmate(ally_turn):
    #         return -999, None, (0, 0)
    #     if depth >= 3:
    #         return self._red_team.get_total_alive_piece_score() - self._blue_team.get_total_alive_piece_score(), None, (0, 0)
    #
    #     max_performance_value = -900
    #     for piece in self.get_team(ally_turn).get_alive_pieces():
    #         for i, j in self.calc_movable_values(piece):
    #             src_pos = piece.get_pos()
    #             dst_pos = (i + src_pos[0], j + src_pos[1])
    #             dst_piece = self._board[dst_pos[1]][dst_pos[0]]
    #             self.put_piece(piece, dst_pos)
    #             performance_value, _, _ = self.min_alpha_beta(depth + 1, alpha, beta)
    #             if self.is_check(enemy_turn):
    #                 performance_value += 0.005
    #             if isinstance(dst_piece, Piece):
    #                 if dst_piece.get_piece_type() == KING:
    #                     performance_value += 500
    #                 performance_value += 0.01
    #             if performance_value > max_performance_value:
    #                 max_performance_value = performance_value
    #                 max_piece = piece
    #                 max_dst_pos = dst_pos
    #             self.restore_put_piece(piece, dst_piece, src_pos)
    #
    #             if max_performance_value >= beta:
    #                 return max_performance_value, max_piece, max_dst_pos
    #
    #             if max_performance_value > alpha:
    #                 alpha = max_performance_value
    #
    #     if max_performance_value == -900:
    #         max_piece = None
    #         max_dst_pos = None
    #
    #     return max_performance_value, max_piece, max_dst_pos
    #
    # def min_alpha_beta(self, depth: int, alpha: int, beta: int) -> tuple[int, Piece, tuple[int, int]]:
    #     ally_turn = BLUE_TEAM
    #     enemy_turn = RED_TEAM
    #     if self.is_check(ally_turn) and self.is_checkmate(ally_turn):
    #         return 999, None, (0, 0)
    #     if depth >= 3:
    #         return self._red_team.get_total_alive_piece_score() - self._blue_team.get_total_alive_piece_score(), None, (0, 0)
    #
    #     min_performance_value = 900
    #     for piece in self.get_team(ally_turn).get_alive_pieces():
    #         for i, j in self.calc_movable_values(piece):
    #             src_pos = piece.get_pos()
    #             dst_pos = (i + src_pos[0], j + src_pos[1])
    #             dst_piece = self._board[dst_pos[1]][dst_pos[0]]
    #             self.put_piece(piece, dst_pos)
    #             performance_value, _, _ = self.max_alpha_beta(depth + 1, alpha, beta)
    #             if self.is_check(enemy_turn):
    #                 performance_value -= 0.005
    #             if isinstance(dst_piece, Piece):
    #                 if dst_piece.get_piece_type() == KING:
    #                     performance_value -= 500
    #                 performance_value -= 0.01
    #             if performance_value < min_performance_value:
    #                 min_performance_value = performance_value
    #                 min_piece = piece
    #                 min_dst_pos = dst_pos
    #             self.restore_put_piece(piece, dst_piece, src_pos)
    #
    #             if min_performance_value <= alpha:
    #                 return min_performance_value, min_piece, min_dst_pos
    #
    #             if min_performance_value < beta:
    #                 beta = min_performance_value
    #
    #     if min_performance_value == 900:
    #         min_piece = None
    #         min_dst_pos = None
    #
    #     return min_performance_value, min_piece, min_dst_pos
    #
    # def get_mcts_pick(self) -> tuple[int, Piece, tuple[int, int]]:
    #     ai_turn = self.get_current_turn()
    #     child_actions = []
    #     pieces = self.get_team(ai_turn).get_alive_pieces()
    #     for piece in pieces:
    #         movable_values = self.calc_movable_values(piece)
    #         child_actions.append(movable_values)
    #
    #     result_dst_positions = [0 for _ in range(len(pieces))]
    #     winning_rates = [-1 for _ in range(len(pieces))]
    #     for i, piece in enumerate(pieces):
    #         movable_values = child_actions[i]
    #         for movable_value in movable_values:
    #             copy_game = copy.deepcopy(self)
    #             copy_piece = copy_game.get_piece_from_board(piece.get_pos())
    #
    #             src_pos = copy_piece.get_pos()
    #             dst_pos = (src_pos[0] + movable_value[0], src_pos[1] + movable_value[1])
    #             copy_game.put_piece(copy_piece, dst_pos)
    #             copy_game.switch_current_turn()
    #             copy_game.increment_games_played()
    #
    #             winning_rate, k = 0, 2
    #             print("시뮬레이션 시작!")
    #             print("src_piece :", str(copy_piece.get_piece_type()) + ", movable_value :", movable_value,
    #                   ", src_pos :", src_pos, ", dst_pos :", dst_pos)
    #             for _ in range(k):
    #                 winning_rate += mcts_simulation(copy_game)
    #             print("시뮬레이션 종료!, winning_rate :", winning_rate)
    #
    #             if winning_rates[i] < winning_rate:
    #                 winning_rates[i] = winning_rate
    #                 result_dst_positions[i] = dst_pos
    #
    #             del copy_game
    #
    #     if winning_rates == [-1 for _ in range(len(pieces))]:
    #         return -1, None, None
    #     else:
    #         print("winning_rates :", winning_rates)
    #         print("pieces :", pieces)
    #         print("result_dst_positions :", result_dst_positions)
    #
    #     max_rate = max(winning_rates)
    #     valid_winning_rates = [rate for rate in winning_rates if rate == max_rate]
    #     valid_winning_rates_idx = [i for i, rate in enumerate(winning_rates) if rate == max_rate]
    #     rand_num = random.randrange(0, len(valid_winning_rates))
    #     print("rand_num :", rand_num, ", valid_winning_rates_idx[rand_num] :", valid_winning_rates_idx[rand_num])
    #     return valid_winning_rates[rand_num], pieces[valid_winning_rates_idx[rand_num]], result_dst_positions[valid_winning_rates_idx[rand_num]]


class Display:
    def __init__(self):
        self._Surface = pygame.display.set_mode((JANGGI_BOARD_WIDTH * MAGNIFICATION_RATIO,
                                                 JANGGI_BOARD_HEIGHT * MAGNIFICATION_RATIO))

        self._blue_king_img = \
            pygame.transform.scale(pygame.image.load(BLUE_KING_IMG_PATH),
                                   (JANGGI_KING_PIECE_SIZE * MAGNIFICATION_RATIO,
                                    JANGGI_KING_PIECE_SIZE * MAGNIFICATION_RATIO))
        self._blue_rook_img = \
            pygame.transform.scale(pygame.image.load(BLUE_ROOK_IMG_PATH),
                                   (JANGGI_BIG_PIECE_SIZE * MAGNIFICATION_RATIO,
                                    JANGGI_BIG_PIECE_SIZE * MAGNIFICATION_RATIO))
        self._blue_cannon_img = \
            pygame.transform.scale(pygame.image.load(BLUE_CANNON_IMG_PATH),
                                   (JANGGI_BIG_PIECE_SIZE * MAGNIFICATION_RATIO,
                                    JANGGI_BIG_PIECE_SIZE * MAGNIFICATION_RATIO))
        self._blue_knight_img = \
            pygame.transform.scale(pygame.image.load(BLUE_KNIGHT_IMG_PATH),
                                   (JANGGI_BIG_PIECE_SIZE * MAGNIFICATION_RATIO,
                                    JANGGI_BIG_PIECE_SIZE * MAGNIFICATION_RATIO))
        self._blue_elephant_img = \
            pygame.transform.scale(pygame.image.load(BLUE_ELEPHANT_IMG_PATH),
                                   (JANGGI_BIG_PIECE_SIZE * MAGNIFICATION_RATIO,
                                    JANGGI_BIG_PIECE_SIZE * MAGNIFICATION_RATIO))
        self._blue_guard_img = \
            pygame.transform.scale(pygame.image.load(BLUE_GUARD_IMG_PATH),
                                   (JANGGI_SMALL_PIECE_SIZE * MAGNIFICATION_RATIO,
                                    JANGGI_SMALL_PIECE_SIZE * MAGNIFICATION_RATIO))
        self._blue_pawn_img = \
            pygame.transform.scale(pygame.image.load(BLUE_PAWN_IMG_PATH),
                                   (JANGGI_SMALL_PIECE_SIZE * MAGNIFICATION_RATIO,
                                    JANGGI_SMALL_PIECE_SIZE * MAGNIFICATION_RATIO))
        self._red_king_img = \
            pygame.transform.scale(pygame.image.load(RED_KING_IMG_PATH),
                                   (JANGGI_KING_PIECE_SIZE * MAGNIFICATION_RATIO,
                                    JANGGI_KING_PIECE_SIZE * MAGNIFICATION_RATIO))
        self._red_rook_img = \
            pygame.transform.scale(pygame.image.load(RED_ROOK_IMG_PATH),
                                   (JANGGI_BIG_PIECE_SIZE * MAGNIFICATION_RATIO,
                                    JANGGI_BIG_PIECE_SIZE * MAGNIFICATION_RATIO))
        self._red_cannon_img = \
            pygame.transform.scale(pygame.image.load(RED_CANNON_IMG_PATH),
                                   (JANGGI_BIG_PIECE_SIZE * MAGNIFICATION_RATIO,
                                    JANGGI_BIG_PIECE_SIZE * MAGNIFICATION_RATIO))
        self._red_knight_img = \
            pygame.transform.scale(pygame.image.load(RED_KNIGHT_IMG_PATH),
                                   (JANGGI_BIG_PIECE_SIZE * MAGNIFICATION_RATIO,
                                    JANGGI_BIG_PIECE_SIZE * MAGNIFICATION_RATIO))
        self._red_elephant_img = \
            pygame.transform.scale(pygame.image.load(RED_ELEPHANT_IMG_PATH),
                                   (JANGGI_BIG_PIECE_SIZE * MAGNIFICATION_RATIO,
                                    JANGGI_BIG_PIECE_SIZE * MAGNIFICATION_RATIO))
        self._red_guard_img = \
            pygame.transform.scale(pygame.image.load(RED_GUARD_IMG_PATH),
                                   (JANGGI_SMALL_PIECE_SIZE * MAGNIFICATION_RATIO,
                                    JANGGI_SMALL_PIECE_SIZE * MAGNIFICATION_RATIO))
        self._red_pawn_img = \
            pygame.transform.scale(pygame.image.load(RED_PAWN_IMG_PATH),
                                   (JANGGI_SMALL_PIECE_SIZE * MAGNIFICATION_RATIO,
                                    JANGGI_SMALL_PIECE_SIZE * MAGNIFICATION_RATIO))

    def show_board(self, game: Game):
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

        for piece in game.get_team(RED_TEAM).get_alive_pieces():
            self.draw_piece(piece)
        for piece in game.get_team(BLUE_TEAM).get_alive_pieces():
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
        if piece.get_team_type() == BLUE_TEAM:
            if piece.get_piece_type() == KING:
                img = self._blue_king_img
            elif piece.get_piece_type() == ROOK:
                img = self._blue_rook_img
            elif piece.get_piece_type() == CANNON:
                img = self._blue_cannon_img
            elif piece.get_piece_type() == KNIGHT:
                img = self._blue_knight_img
            elif piece.get_piece_type() == ELEPHANT:
                img = self._blue_elephant_img
            elif piece.get_piece_type() == GUARD:
                img = self._blue_guard_img
            elif piece.get_piece_type() == PAWN:
                img = self._blue_pawn_img
        else:
            if piece.get_piece_type() == KING:
                img = self._red_king_img
            elif piece.get_piece_type() == ROOK:
                img = self._red_rook_img
            elif piece.get_piece_type() == CANNON:
                img = self._red_cannon_img
            elif piece.get_piece_type() == KNIGHT:
                img = self._red_knight_img
            elif piece.get_piece_type() == ELEPHANT:
                img = self._red_elephant_img
            elif piece.get_piece_type() == GUARD:
                img = self._red_guard_img
            elif piece.get_piece_type() == PAWN:
                img = self._red_pawn_img

        i, j = piece.get_pos()
        w, h = img.get_width(), img.get_height()
        self._Surface.blit(img, ((i * CELL_WIDTH + WHITE_SPACE_WIDTH) * MAGNIFICATION_RATIO - w / 2,
                                 (j * CELL_HEIGHT + WHITE_SPACE_HEIGHT) * MAGNIFICATION_RATIO - h / 2))

# def mcts_simulation(game: Game) -> int:
#     ai_turn = game.get_current_turn() % 2 + 1
#     for i in range(4):
#         if game.get_current_turn() == BLUE_TEAM:
#             performance_value, ai_selected_piece, ai_dst_pos = game.min_random(0)
#
#             if ai_selected_piece is None:
#                 game.switch_current_turn()
#                 game.increment_games_played()
#                 continue
#
#             game.put_piece(ai_selected_piece, ai_dst_pos)
#             game.increment_games_played()
#             game.switch_current_turn()
#
#             is_game_over = game.is_game_over()
#             if is_game_over == 0 or is_game_over == 2:
#                 if ai_turn == BLUE_TEAM:
#                     return 1
#                 else:
#                     return 0
#             elif is_game_over == 1:
#                 if game.get_team(RED_TEAM).get_total_alive_piece_score() > game.get_team(BLUE_TEAM).get_total_alive_piece_score():
#                     if ai_turn == BLUE_TEAM:
#                         return 0
#                     else:
#                         return 1
#                 elif game.get_team(RED_TEAM).get_total_alive_piece_score() < game.get_team(BLUE_TEAM).get_total_alive_piece_score():
#                     if ai_turn == BLUE_TEAM:
#                         return 1
#                     else:
#                         return 0
#         elif game.get_current_turn() == RED_TEAM:
#             performance_value, ai_selected_piece, ai_dst_pos = game.max_random(0)
#
#             if ai_selected_piece is None:
#                 game.switch_current_turn()
#                 game.increment_games_played()
#                 continue
#
#             game.put_piece(ai_selected_piece, ai_dst_pos)
#             game.increment_games_played()
#             game.switch_current_turn()
#
#             is_game_over = game.is_game_over()
#             if is_game_over == 0 or is_game_over == 2:
#                 if ai_turn == BLUE_TEAM:
#                     return 0
#                 else:
#                     return 1
#             elif is_game_over == 1:
#                 if game.get_team(RED_TEAM).get_total_alive_piece_score() > game.get_team(BLUE_TEAM).get_total_alive_piece_score():
#                     if ai_turn == BLUE_TEAM:
#                         return 0
#                     else:
#                         return 1
#                 elif game.get_team(RED_TEAM).get_total_alive_piece_score() < game.get_team(BLUE_TEAM).get_total_alive_piece_score():
#                     if ai_turn == BLUE_TEAM:
#                         return 1
#                     else:
#                         return 0
#
#     if game.get_team(RED_TEAM).get_total_alive_piece_score() > game.get_team(BLUE_TEAM).get_total_alive_piece_score():
#         if ai_turn == BLUE_TEAM:
#             return 0
#         else:
#             return 1
#     elif game.get_team(RED_TEAM).get_total_alive_piece_score() < game.get_team(BLUE_TEAM).get_total_alive_piece_score():
#         if ai_turn == BLUE_TEAM:
#             return 1
#         else:
#             return 0

# 추가 구현해야 할 점
# 1. 함수 맹글링
