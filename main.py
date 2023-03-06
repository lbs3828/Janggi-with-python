from pygame.locals import QUIT
from Janggi import *

# 작동 순서
# 1. Janggi 클래스 생성
# 2. 반복문을 돌며 마우스 이벤트 체크
# 3. 왼쪽 마우스 버튼이 눌러졌을 경우 mouse_pos_to_board_idx 함수로 마우스 클릭 위치가 유효한지 검사
# 4-1. 만약 유효하지 않다면 pass
# 4-2. 마우스 클릭 위치가 유효하고 이전에 선택된 장기말이 없는 경우(처음 장기말을 선택) 선택한 장기말이 움직일 수 있는 위치를
#      janggi.calc_movable_values 함수로 계산
# 4-3. 마우스 클릭 위치가 유효하고 이전에 선택된 장기말이 있는 경우 janggi.put_piece 함수를 이용해 마우스 클릭 위치로 이동
# 5. 외통수가 나거나 프로그램 종료 버튼을 누르면 종료

pygame.init()
janggi = Game(BOTTOM_BLUE, LEFT_ELEPHANT_SETTING, OUTSIDE_ELEPHANT_SETTING)
display = Display()
is_piece_clicked = False
is_clicked_quit_button = False

display.show_board(janggi)
while not is_clicked_quit_button:
    for event in pygame.event.get():
        if event.type == QUIT:
            is_clicked_quit_button = True
            break

        if janggi.is_running() and event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
            mi, mj = event.pos[0] / MAGNIFICATION_RATIO, event.pos[1] / MAGNIFICATION_RATIO
            is_valid_pos, i, j = mouse_pos_to_board_idx(mi, mj)
            print("마우스 클릭 위치 -" + " i :", str(i) + ", j :", j)

            if not is_valid_pos:
                is_piece_clicked = False
                display.show_board(janggi)
            elif not is_piece_clicked:
                src_piece = janggi.get_piece_from_board((i, j))
                if isinstance(src_piece, Piece):
                    if src_piece.get_team_type() == janggi.get_current_turn():
                        is_piece_clicked = True
                        movable_values = janggi.calc_movable_values(src_piece)
                        print("movable_pos_list :", movable_values)
                        display.show_board(janggi)
                        display.show_movable_pos(src_piece, movable_values)
                    else:
                        if BLUE_TEAM == janggi.get_current_turn():
                            print("초나라 차례입니다.")
                        else:
                            print("한나라 차례입니다.")
            else:
                src_pos = src_piece.get_pos()
                is_piece_clicked = False
                if (i - src_pos[0], j - src_pos[1]) in movable_values:
                    janggi.put_piece(src_piece, (i, j))
                    janggi.increment_games_played()
                    janggi.switch_current_turn()
                    print(janggi.get_games_played(), "수째 진행 중")
                    display.show_board(janggi)

                    if janggi.is_game_over():
                        janggi.set_running(False)
                        print("게임 종료")
                        continue
                else:
                    display.show_board(janggi)

            # 장기판 출력
            # for line in janggi.get_board():
            #     for piece in line:
            #         if piece == 0:
            #             print(0, end='  ')
            #         else:
            #             print(piece.get_piece_type(), end='  ')
            #     print()

# 추가 구현해야 하는 것들
# 1. 마, 상 위치 선택 기능 추가
# 2. 초나라, 한나라 위치 선택 기능 추가
# 3. 한수쉼
