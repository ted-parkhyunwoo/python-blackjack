import random
from numeric_input import NumericInput

SUITS = ['♠', '♣', '♥', '♦']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
TEN_SCORE = ["J", "Q", "K", "10"]

# NumericInput 클래스 상속.
class Cards(NumericInput):
    def __init__(self):
        super().__init__()
        self.player_score_deck = []
        self.dealer_score_deck = []
        self.player_cards_deck = []
        self.dealer_cards_deck = []

        # 플레이어가 사용할 덱의 갯수. 입력이 비어있다면 1.
        self.decks_used = self.get_numeric("How much used card decks? (default: Single = Enter) : ")
        if self.decks_used == "":
            self.decks_used = 1
        self.make_new_deck()


    #! 테스트용 출력 메서드.
    # desc("player", "total") 등으로 사용.
    # desc("cards", "remain") 남은카드 묘사. decks 는 사용중인 덱 디스플레이.
    # Todo. status (winner클래스의 어트리뷰츠) 사용 가능한지 검토.
    def desc(self, user, info):
        # 유저에 대한 describe.
        if user == "dealer":
            if info == "cards":
                return self.dealer_cards_deck
            elif info == "score":
                return self.dealer_score_deck
            elif info == "total":
                return sum(self.dealer_score_deck)
        elif user == "player":
            if info == "cards":
                return self.player_cards_deck
            elif info == "score":
                return self.player_score_deck
            elif info == "total":
                return sum(self.player_score_deck)
        # 카드에 대한 describe.    
        elif user == "cards":
            if info == "remain":
                return len(self.card_deck)
            elif info == "decks":
                return self.decks_used
            
            
            
    # 새 카드 덱을 만듬. (싱글,더블덱을 곱연산 함.)
    def make_new_deck(self):
        self.card_deck = [rank + suit for suit in SUITS for rank in RANKS] * self.decks_used
        random.shuffle(self.card_deck)        
 
    # 이전 덱 초기화 메서드.(한턴 끝날시 작동.)
    # 카드 부족시 선제적으로 카드 재보급 로직 추가.    
    def clear_decks(self):
        self.player_cards_deck = []
        self.player_score_deck = []
        self.dealer_cards_deck = []
        self.dealer_score_deck = []
        # 30% 미만의 카드만 남았을시, 
        # 25%로 했었으나, 싱글덱(52장) 사용중 사용자가 2,2,2,2,3,3,A,A,A,A stand(18점 10장), 딜러 3,3,4,4,4(16점룰) 로 최대 15장으로, 
        # 25%로는(13장) 게임이 문제를 일으킴. -물론 극악의 확률임.
        if len(self.card_deck) < (52 * self.decks_used)/100 * 30:
            print("New decks suffled.")
            self.make_new_deck()
        
    # 카드 분배 메서드. 파라미터에 "player" 등을 적어 사용.
    # 카드 덱 리스트 끝에서부터 pop 되어 (person)의 파라미터의 덱으로 쌓음. + 점수덱 생성
    def deal_card(self, person):
        
        # 스코어링 함수. 파라미터에 카드를 넣으면 점수로 return. 예시 : card_make_scoring("5♠") -> 5
        def card_make_score(card):
            # 문자를 점수화
            if "A" in card:
                result = 11
            elif all(TEN_SCORE for word in card):
                result = 10
            # 숫자를 result로 저장. 2~9까지.(10은 제외, ten_score에 추가됨.)
            for num in range(2, 10):
                if str(num) in card:
                    result = num
            return result
    
        current_card = self.card_deck.pop()

        if person == "player":
            self.player_cards_deck.append(current_card)
            self.player_score_deck.append(card_make_score(current_card))

        elif person == "dealer":
            self.dealer_cards_deck.append(current_card)
            self.dealer_score_deck.append(card_make_score(current_card))
            
    
    # 에이스 체인지 메서드. 유저의 아규먼트와 해당 유저 덱에 11이 포함되어야 작동.
    def ace_changer(self, person):
        if 11 in self.player_score_deck and person == "player":
            ace_index = self.player_score_deck.index(11)
            self.player_score_deck[ace_index] = 1
            self.player_cards_deck[ace_index] += "[1]"
            
        elif 11 in self.dealer_score_deck and person == "dealer":
            ace_index = self.dealer_score_deck.index(11)
            self.dealer_score_deck[ace_index] = 1
            self.dealer_cards_deck[ace_index] += "[1]"
            
    # 실행시 딜러가 16 초과까지 패를 받음 - ace_changer 메서드 첨부(딜러 용)
    def dealer_16(self):
        while self.desc("dealer", "total") < 17:
            self.deal_card("dealer")
            if self.desc("dealer", "total") > 21:
                if 11 in self.dealer_score_deck:
                    self.ace_changer("dealer")
