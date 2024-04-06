from numeric_input import NumericInput


# NumericInput 클래스 상속.
class Betting(NumericInput):
    
    #초기화 목록.
    def __init__(self):
        super().__init__()
        self.bank = float(1000)
        self.highest = float(1000)
        self.current_bet = 10
        self.last_bet = 10
        self.savebank = 0

    # 기록 불러오기
    def load_bank(self):
        with open("./user.cfg",  mode="r") as last_bank_file:
            self.last_bank = float(last_bank_file.read()) 
        if self.last_bank > self.bank:
            if input(f"Load saved data? (bank=${self.last_bank}, type 'n' to Reset=$1000.) : ").lower() == "n":
                pass
            else:
                self.bank = self.last_bank

    #기록 저장하기
    def save_bank(self):
        self.savebank = self.bank
        with open("./user.cfg", mode="w") as save_file:
            save_file.write(str(self.savebank))
        
    # 베팅할 금액의 크기.
    def bet_amount(self):
        #입력 검사.
        user_input = self.get_numeric(f"Your Bet (Previous bet: ${self.last_bet} = Enter): $")
        if user_input == "":
            user_bet = self.last_bet

        else:
            user_bet = int(user_input)

        # user_bet
        if self.bank >= user_bet:
            self.current_bet = user_bet
            self.last_bet = self.current_bet
            print(f"You have bet: ${user_bet}.")
            return True
        else:
            print("Not enough money.")
            return False

    
    # 결과에 따른 보상 메서드. winner의 result메서드 리턴을 사용 혹은, winner.game_result 사용.
    def settlement(self, game_result):
        if game_result == "win":
            self.bank += self.current_bet 
            print(f"Winning Price: + ${self.current_bet}, Total Bank: ${self.bank}")
        elif game_result == "blackjack":
            self.bank += self.current_bet * 0.5
            print(f"Winning Price: + ${self.current_bet * 0.5}, Total Bank: ${self.bank}")
        elif game_result == "lose":
            self.bank -= self.current_bet
            print(f"You lost: - $ {self.current_bet}, Total Bank: ${self.bank},")
        else:
            self.bank = self.bank
            print(f"You take money back. : ${self.current_bet}, Total Bank: ${self.bank}")
            
        # 결과보상 정산 후, 최고 금액 갱신시 기록.   
        if self.bank > self.highest:
            self.highest = self.bank
            
    
#~ todo. all-in 기능 첨부. - numeric_input 사용과 컨셉이 겹쳐서 계획 취소.
