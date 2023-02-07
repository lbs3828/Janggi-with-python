from pygame.locals import QUIT
from Janggi import *


def mouse_pos_to_board_idx(mi: int, mj: int) -> tuple[bool, int, int]:
    i, j = -1, -1

    horizontal_line_list = [CELL_WIDTH * i + WHITE_SPACE_WIDTH for i in range(9)]
    vertical_line_list = [CELL_HEIGHT * j + WHITE_SPACE_HEIGHT for j in range(10)]
    adjacent_i_value = sorted(horizontal_line_list, key=lambda i: abs(i - mi))[0]
    adjacent_j_value = sorted(vertical_line_list, key=lambda j: abs(j - mj))[0]

    gap = JANGGI_KING_PIECE_SIZE / 2
    if adjacent_i_value - gap <= mi <= adjacent_i_value + gap and \
            adjacent_j_value - gap <= mj <= adjacent_j_value + gap:
        i = horizontal_line_list.index(adjacent_i_value)
        j = vertical_line_list.index(adjacent_j_value)
        return True, i, j
    else:
        return False, i, j


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
janggi = Game()
player_turn = BLUE_TEAM
ai_selected_piece = None
is_piece_clicked = False
is_clicked_quit_button = False

janggi.show_board()
while not is_clicked_quit_button:
    for event in pygame.event.get():
        if event.type == QUIT:
            is_clicked_quit_button = True
            break

        if janggi.get_turn() == player_turn:
            if janggi.get_running() and event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
                mi, mj = event.pos[0] / MAGNIFICATION_RATIO, event.pos[1] / MAGNIFICATION_RATIO
                is_valid_pos, i, j = mouse_pos_to_board_idx(mi, mj)
                print("마우스 클릭 위치 -" + " i :", str(i) + ", j :", j)

                if not is_valid_pos:
                    is_piece_clicked = False
                    janggi.show_board()
                    if ai_selected_piece is not None:
                        janggi.show_ai_move_pos(ai_dst_pos)
                elif not is_piece_clicked:
                    src_piece = janggi.get_piece_from_board((i, j))
                    if isinstance(src_piece, Piece):
                        if src_piece.get_team_type() == janggi.get_turn():
                            is_piece_clicked = True
                            movable_values = janggi.calc_movable_values(src_piece)
                            print("movable_pos_list :", movable_values)
                            janggi.show_board()
                            janggi.show_movable_pos(src_piece, movable_values)
                            if ai_selected_piece is not None:
                                janggi.show_ai_move_pos(ai_dst_pos)
                        else:
                            if BLUE_TEAM == janggi.get_turn():
                                print("초나라 차례입니다.")
                            else:
                                print("한나라 차례입니다.")
                else:
                    src_pos = src_piece.get_pos()
                    is_piece_clicked = False
                    if (i - src_pos[0], j - src_pos[1]) in movable_values:
                        janggi.put_piece(src_piece, (i, j))
                        janggi.show_board()
                        janggi.set_turn_to_next()

                        is_game_over = janggi.is_game_over()
                        if is_game_over == 2:
                            print("외통수! 게임 종료")
                            janggi.set_running(False)
                            continue
                        elif is_game_over == 1:
                            print("장군!")
                    else:
                        janggi.show_board()
        else:
            print("mcts 계산중")
            winning_rate, ai_selected_piece, ai_dst_pos = janggi.get_mcts_pick()
            ai_dst_i = ai_dst_pos[0]
            ai_dst_j = ai_dst_pos[1]
            print("mcts 계산 완료")
            print("승률 :", winning_rate)
            print("src_piece :", str(ai_selected_piece.get_piece_type()) + ", i :", str(ai_dst_i) + ", j :", ai_dst_j)
            janggi.put_piece(ai_selected_piece, ai_dst_pos)
            janggi.set_turn_to_next()
            janggi.show_board()
            janggi.show_ai_move_pos(ai_dst_pos)

            is_game_over = janggi.is_game_over()
            if is_game_over == 2:
                print("외통수! 게임 종료")
                janggi.set_running(False)
                continue
            elif is_game_over == 1:
                print("장군!")

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
