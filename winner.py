class Winner:

    def __init__(self):
        self.status_dealer = ""
        self.status_player = ""
        self.game_result = ""

    # 이전 게임의 상태를 초기화 함.
    def clear_status(self):
        self.status_player = ""
        self.status_dealer = ""

    # 승패 결정 메서드. status를 갱신하고 return엔 승자 혹은 draw 됨.
    # 고차 함수로 아래 result가 사용되니, return은 지우지 않도록 함.
    def result(self, dealer_totalscore, player_totalscore, dealer_cards_len, player_cards_len):

        # * 버스트에 대한 로직 체크- 확인됨.
        # 플레이어 버스트시 - hit 시에만 bust가 생김. 딜러는 패를 까지도 않고 플레이어 패배처리함.
        # 딜러 버스트시 - 플레이어가 stand 시에만 발생하므로, 플레이어 bust로 인한 draw에 대한 검토는 하지 않아도 됨.

        # 플레이어 버스트
        if player_totalscore > 21:
            self.status_player = "bust"
            self.game_result = "lose"
            return "lose"

        # 딜러 버스트 
        elif dealer_totalscore > 21:
            self.status_dealer = "bust"
            self.game_result = "win"
            return "win"

        # 유저 21 or blackjack
        elif player_totalscore == 21:
            # 유저 블랙잭
            if player_cards_len == 2:
                self.status_player = "blackjack"
                # 딜러도 블랙잭
                if dealer_totalscore == 21 and dealer_cards_len == 2:
                    self.status_dealer = "blackjack"
                    self.game_result = "draw"
                    return "draw"
                # 딜러 노멀21
                elif dealer_totalscore == 21:
                    self.status_dealer = "normal_21"
                    self.game_result = "blackjack"
                    return "blackjack"
                # 다른조건(블랙잭 제외)은 무조건 플레이어 승.
                else:
                    self.game_result = "win"
                    return "win"
            # 유저 노멀 21
            else:
                # 유저 노멀 21 상태 설정.
                self.status_player = "normal_21"
                # 딜러 블랙잭
                if dealer_totalscore == 21 and dealer_cards_len == 2:
                    self.status_dealer = "blackjack"
                    self.game_result = "lose"
                    return "lose"
                # 딜러 노멀21
                elif dealer_totalscore == 21:
                    self.status_dealer = "normal_21"
                    self.game_result = "draw"
                    return "draw"
                # 딜러 그 이하시
                else:
                    self.game_result = "win"
                    return "win"

        # 딜러 21 or blackjack  -- 
        # todo. 최적화. 일부 로직 검토 필요.(플레이어에서 사용된 코드가 재사용 될 가능성 있음.)
        elif dealer_totalscore == 21:
            # 딜러 블랙잭
            if dealer_cards_len == 2:
                self.status_dealer = "blackjack"
                # 플레이어도 블랙잭
                if player_totalscore == 21 and player_cards_len == 2:
                    self.status_player = "blackjack"
                    self.game_result = "draw"
                    return "draw"
                # 유저 노멀21 포함 
                elif player_totalscore == 21:
                    self.status_player = "normal_21"
                    self.game_result = "lose"
                    return "lose"
                # 다른조건 (블랙잭 제외) 무조건 딜러 승.
                else:
                    self.game_result = "lose"
                    return "lose"
            # 딜러 노멀 21
            else:
                # 유저 블랙잭
                self.status_dealer = "normal_21"
                if player_totalscore == 21 and player_cards_len == 2:
                    self.status_player = "blackjack"
                    self.game_result = "blackjack"
                    return "blackjack"
                # 유저 노멀 21
                elif player_totalscore == 21:
                    self.status_player = "normal_21"
                    self.game_result = "draw"
                    return "draw"
                # 유저 그 이하시
                else:
                    self.game_result = "lose"
                    return "lose"

        # 위 특수상항 제외 단순 점수비교
        else:
            if player_totalscore > dealer_totalscore:
                self.status_player = "higher"
                self.game_result = "win"
                return "win"
            elif player_totalscore < dealer_totalscore:
                self.status_dealer = "higher"
                self.game_result = "lose"
                return "lose"
            elif player_totalscore == dealer_totalscore:
                self.status_player = "same_score"
                self.status_dealer = "same_score"
                self.game_result = "draw"
                return "draw"

