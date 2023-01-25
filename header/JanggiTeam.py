from JanggiPiece import *

class JanggiTeam:
    def __init__(self, team_type: str):
        self._checked = False
        self._team_type = team_type
        self._pieces = []
        self._init_pieces()

    def _init_pieces(self):
        if self._team_type == RED_TEAM:
            for i in range(5):
                self._pieces.append(JanggiPiece(PAWN, RED_TEAM, (2 * i, 3), RED_PAWN_IMG_PATH))
            for i in range(2):
                self._pieces.append(JanggiPiece(ROOK, RED_TEAM, (i * 8, 0), RED_ROOK_IMG_PATH))
                self._pieces.append(JanggiPiece(KNIGHT, RED_TEAM, (i * 6 + 1, 0), RED_KNIGHT_IMG_PATH))
                self._pieces.append(JanggiPiece(ELEPHANT, RED_TEAM, (i * 4 + 2, 0), RED_ELEPHANT_IMG_PATH))
                self._pieces.append(JanggiPiece(GUARD, RED_TEAM, (i * 2 + 3, 0), RED_GUARD_IMG_PATH))
                self._pieces.append(JanggiPiece(CANNON, RED_TEAM, (i * 6 + 1, 2), RED_CANNON_IMG_PATH))
            self._pieces.append(JanggiPiece(KING, RED_TEAM, (4, 1), RED_KING_IMG_PATH))
        else:
            for i in range(5):
                self._pieces.append(JanggiPiece(PAWN, BLUE_TEAM, (2 * i, 6), BLUE_PAWN_IMG_PATH))
            for i in range(2):
                self._pieces.append(JanggiPiece(ROOK, BLUE_TEAM, (i * 8, 9), BLUE_ROOK_IMG_PATH))
                self._pieces.append(JanggiPiece(KNIGHT, BLUE_TEAM, (i * 6 + 1, 9), BLUE_KNIGHT_IMG_PATH))
                self._pieces.append(JanggiPiece(ELEPHANT, BLUE_TEAM, (i * 4 + 2, 9), BLUE_ELEPHANT_IMG_PATH))
                self._pieces.append(JanggiPiece(GUARD, BLUE_TEAM, (i * 2 + 3, 9), BLUE_GUARD_IMG_PATH))
                self._pieces.append(JanggiPiece(CANNON, BLUE_TEAM, (i * 6 + 1, 7), BLUE_CANNON_IMG_PATH))
            self._pieces.append(JanggiPiece(KING, BLUE_TEAM, (4, 8), BLUE_KING_IMG_PATH))

    def get_checked(self) -> bool:
        return self._checked

    def set_checked(self, checked: bool):
        self._checked = checked

    def get_pieces(self) -> list[JanggiPiece]:
        return self._pieces

    def get_king_piece(self) -> JanggiPiece:
        return self._pieces[-1]