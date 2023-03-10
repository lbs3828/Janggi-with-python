# 장기판 및 장기말 크기 상수
JANGGI_BOARD_WIDTH = 45         # 장기판 가로 : 45cm
JANGGI_BOARD_HEIGHT = 42        # 장기판 세로 : 42cm
CELL_WIDTH = 4.7                # 장기판 가로 한칸 : 4.7cm
CELL_HEIGHT = 4                 # 장기판 세로 한칸 : 4cm
WHITE_SPACE_WIDTH = 3.7         # 장기판 가로 여백 : 3.7cm
WHITE_SPACE_HEIGHT = 3          # 장기판 세로 여백 : 3cm
JANGGI_KING_PIECE_SIZE = 3.7    # 궁(將)크기 : 3.7cm
JANGGI_BIG_PIECE_SIZE = 3       # 대기물(大棋物)크기 : 3cm
JANGGI_SMALL_PIECE_SIZE = 2.3   # 소기물(小棋物)크기 : 2.3cm

# 색 상수
BACKGROUND_COLOR = (244, 176, 93)   # 장기판 배경색
BLACK_COLOR = (0, 0, 0)             # 검정색

# 팀 타입
BLUE_TEAM = 0   # 초나라 : 0
RED_TEAM = 1    # 한나라 : 1

# 장기판 세팅 타입
BOTTOM_BLUE = 0
BOTTOM_RED = 1

# 장기 판차림 세팅 타입
LEFT_ELEPHANT_SETTING = 0       # 왼상 차림 (귀마)
RIGHT_ELEPHANT_SETTING = 1      # 오른상 차림 (귀마)
INSIDE_ELEPHANT_SETTING = 2     # 안상 차림 (원앙마)
OUTSIDE_ELEPHANT_SETTING = 3    # 바깥상 차림 (양귀마)

# 장기판 확대 비율
MAGNIFICATION_RATIO = 15    # 장기판 확대 비율

# 장기말 타입
KING = 'King'      # 궁
GUARD = 'Guard'     # 사
CANNON = 'Cannon'    # 포
KNIGHT = 'Knight'    # 마
ELEPHANT = 'Elephant'  # 상
ROOK = 'Rook'      # 차
PAWN = 'Pawn'      # 졸, 병

# 장기말 이미지 경로
BLUE_KING_IMG_PATH = "janggi_new_piece_image/Blue_King.png"             # 초 궁 이미지 경로
BLUE_GUARD_IMG_PATH = "janggi_new_piece_image/Blue_Guard.png"           # 초 사 이미지 경로
BLUE_ROOK_IMG_PATH = "janggi_new_piece_image/Blue_Rook.png"             # 초 차 이미지 경로
BLUE_CANNON_IMG_PATH = "janggi_new_piece_image/Blue_Cannon.png"         # 초 포 이미지 경로
BLUE_KNIGHT_IMG_PATH = "janggi_new_piece_image/Blue_Knight.png"         # 초 마 이미지 경로
BLUE_ELEPHANT_IMG_PATH = "janggi_new_piece_image/Blue_Elephant.png"     # 초 상 이미지 경로
BLUE_PAWN_IMG_PATH = "janggi_new_piece_image/Blue_Pawn.png"             # 초 졸 이미지 경로
RED_KING_IMG_PATH = "janggi_new_piece_image/Red_King.png"               # 한 궁 이미지 경로
RED_GUARD_IMG_PATH = "janggi_new_piece_image/Red_Guard.png"             # 한 사 이미지 경로
RED_ROOK_IMG_PATH = "janggi_new_piece_image/Red_Rook.png"               # 한 차 이미지 경로
RED_CANNON_IMG_PATH = "janggi_new_piece_image/Red_Cannon.png"           # 한 포 이미지 경로
RED_KNIGHT_IMG_PATH = "janggi_new_piece_image/Red_Knight.png"           # 한 마 이미지 경로
RED_ELEPHANT_IMG_PATH = "janggi_new_piece_image/Red_Elephant.png"       # 한 상 이미지 경로
RED_PAWN_IMG_PATH = "janggi_new_piece_image/Red_Pawn.png"               # 한 병 이미지 경로

# 마우스 버튼 값
LEFT = 1    # 왼쪽 마우스 버튼
