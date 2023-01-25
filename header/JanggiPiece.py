import pygame
from janggi_const import *


class JanggiPiece:
    def __init__(self, piece_type: str, team_type: str, idx: tuple[int, int], img_path: str):
        self._piece_type = piece_type
        self._team_type = team_type
        self._i = idx[0]
        self._j = idx[1]
        janggi_piece_size_dic = {
            KING: JANGGI_KING_PIECE_SIZE,
            ROOK: JANGGI_BIG_PIECE_SIZE,
            CANNON: JANGGI_BIG_PIECE_SIZE,
            KNIGHT: JANGGI_BIG_PIECE_SIZE,
            ELEPHANT: JANGGI_BIG_PIECE_SIZE,
            GUARD: JANGGI_SMALL_PIECE_SIZE,
            PAWN: JANGGI_SMALL_PIECE_SIZE
        }
        piece_size = janggi_piece_size_dic[piece_type]
        self._img = pygame.transform.scale(pygame.image.load(img_path), (piece_size * MAGNIFICATION_RATIO,
                                                                         piece_size * MAGNIFICATION_RATIO))
        self._alive = True

    def get_piece_type(self) -> str:
        return self._piece_type

    def get_team_type(self) -> str:
        return self._team_type

    def get_i(self) -> int:
        return self._i

    def get_j(self) -> int:
        return self._j

    def set_pos(self, pos: tuple[int, int]):
        self._i = pos[0]
        self._j = pos[1]

    def get_pos(self) -> tuple[int, int]:
        return self._i, self._j

    def get_img(self) -> pygame.Surface:
        return self._img

    def get_alive(self) -> bool:
        return self._alive

    def set_alive(self, alive: bool):
        self._alive = alive
