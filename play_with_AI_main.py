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


pygame.init()
janggi = Game()
is_piece_clicked = False
player_turn = BLUE_TEAM
ai_turn = RED_TEAM
ai_dst_pos = None

janggi.show_board()
while janggi.get_running():
    for event in pygame.event.get():
        if event.type == QUIT:
            janggi.set_running(False)
            break

        if janggi.get_turn() == player_turn:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
                mi, mj = event.pos[0] / MAGNIFICATION_RATIO, event.pos[1] / MAGNIFICATION_RATIO
                is_valid_pos, i, j = mouse_pos_to_board_idx(mi, mj)
                print("마우스 클릭 위치 -" + " i :", str(i) + ", j :", j)
                if not is_valid_pos:
                    is_piece_clicked = False
                    janggi.show_board()
                    if ai_dst_pos is not None:
                        janggi.show_ai_move_pos(ai_dst_pos)
                elif not is_piece_clicked:
                    src_piece = janggi.get_piece_from_board((i, j))
                    if isinstance(src_piece, Piece):
                        if src_piece.get_team_type() == janggi.get_turn():
                            is_piece_clicked = True
                            movable_values = janggi.calc_movable_values(src_piece)
                            print("movable_pos_list :", movable_values)
                            janggi.show_board()
                            if ai_dst_pos is not None:
                                janggi.show_ai_move_pos(ai_dst_pos)
                            janggi.show_movable_pos(src_piece, movable_values)
                        else:
                            if BLUE_TEAM == janggi.get_turn():
                                print("초나라 차례입니다.")
                            else:
                                print("한나라 차례입니다.")
                else:
                    src_pos = src_piece.get_pos()
                    if (i - src_pos[0], j - src_pos[1]) in movable_values:
                        janggi.put_piece(src_piece, (i, j))
                        janggi.show_board()

                        if janggi.is_enemy_checked(janggi.get_turn()):
                            if janggi.is_enemy_checkmate(janggi.get_turn()):
                                print("외통수! 게임 종료")
                                janggi.set_running(False)
                                continue
                            else:
                                print("장군!")
                        janggi.set_turn_to_next()
                    else:
                        janggi.show_board()
                        if ai_dst_pos is not None:
                            janggi.show_ai_move_pos(ai_dst_pos)
                        is_piece_clicked = False

        else:
            print("AI 계산중")
            performance_value, ai_selected_piece, ai_dst_i, ai_dst_j = janggi.max(0, -200, 200)
            ai_dst_pos = (ai_dst_i, ai_dst_j)
            print("AI 계산 완료")
            print("AI performance_value :", str(performance_value) + ", src_piece :", str(ai_selected_piece.get_piece_type()) + ", i :", str(ai_dst_i) + ", j :", ai_dst_j)
            janggi.put_piece(ai_selected_piece, ai_dst_pos)
            janggi.show_board()
            janggi.show_ai_move_pos(ai_dst_pos)

            if janggi.is_enemy_checked(janggi.get_turn()):
                if janggi.is_enemy_checkmate(janggi.get_turn()):
                    print("외통수! 게임 종료")
                    janggi.set_running(False)
                    continue
                else:
                    print("장군!")

            is_piece_clicked = False
            janggi.set_turn_to_next()

            # 장기판 출력
            # for line in janggi.get_board():
            #     for piece in line:
            #         if piece == 0:
            #             print(0, end='  ')
            #         else:
            #             print(piece.get_piece_type(), end='  ')
            #     print()

exit = False
while not exit:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit = True
pygame.quit()
