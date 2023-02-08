    # max, min 함수
    def max(self, depth: int, alpha: int, beta: int) -> tuple[int, Piece, tuple[int, int]]:
        if depth >= 3:
            return self._red_team.get_total_piece_score() - self._blue_team.get_total_piece_score(), None, (0, 0)

        ally_turn = RED_TEAM
        if self.is_checkmate(ally_turn):
            return -999, None, (0, 0)

        candidate_result = []
        max_performance_value = -99999
        for piece in self.get_team(ally_turn).get_pieces():
            if piece.get_alive():
                for i, j in self.calc_movable_values(piece):
                    src_pos = piece.get_pos()
                    dst_pos = (i + src_pos[0], j + src_pos[1])
                    dst_piece = self._board[dst_pos[1]][dst_pos[0]]
                    self.put_piece(piece, dst_pos)
                    performance_value, _, _ = self.min(depth + 1, alpha, beta)
                    if performance_value >= max_performance_value:
                        if performance_value > max_performance_value:
                            candidate_result.clear()
                        max_performance_value = performance_value
                        max_piece = piece
                        max_dst_pos = dst_pos
                        candidate_result.append((max_performance_value, max_piece, max_dst_pos))
                    self.restore_put_piece(piece, dst_piece, src_pos)

                    if max_performance_value >= beta:
                        return max_performance_value, max_piece, max_dst_pos

                    if max_performance_value > alpha:
                        alpha = max_performance_value

        rand_num = random.randrange(0, len(candidate_result))
        if depth == 0:
            print("max :", candidate_result)
        return candidate_result[rand_num]

    def min(self, depth: int, alpha: int, beta: int) -> tuple[int, Piece, tuple[int, int]]:
        if depth >= 3:
            # 인공지능 팀이 바뀌면 수정해야 됨
            return self._red_team.get_total_piece_score() - self._blue_team.get_total_piece_score(), None, (0, 0)

        ally_turn = BLUE_TEAM
        if self.is_checkmate(ally_turn):
            return 999, None, (0, 0)

        candidate_result = []
        min_performance_value = 99999
        for piece in self.get_team(ally_turn).get_pieces():
            if piece.get_alive():
                for i, j in self.calc_movable_values(piece):
                    src_pos = piece.get_pos()
                    dst_pos = (i + src_pos[0], j + src_pos[1])
                    dst_piece = self._board[dst_pos[1]][dst_pos[0]]
                    self.put_piece(piece, dst_pos)
                    performance_value, _, _ = self.max(depth + 1, alpha, beta)
                    if performance_value <= min_performance_value:
                        if performance_value < min_performance_value:
                            candidate_result.clear()
                        min_performance_value = performance_value
                        min_piece = piece
                        min_dst_pos = dst_pos
                        candidate_result.append((min_performance_value, min_piece, min_dst_pos))
                    self.restore_put_piece(piece, dst_piece, src_pos)

                    if min_performance_value <= alpha:
                        return min_performance_value, min_piece, min_dst_pos

                    if min_performance_value < beta:
                        beta = min_performance_value

        rand_num = random.randrange(0, len(candidate_result))
        if depth == 0:
            print("min :", candidate_result)
        return candidate_result[rand_num]