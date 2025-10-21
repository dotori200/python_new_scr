# 가위 바위 보 게임을 클래스로 구현한다.
# 사용자로부터 입력을 받아 컴퓨터와 대결하는 간단한 가위바위보 게임을 구현한다.
# 사용자는 "가위", "바위", "보" 중 하나를 입력하고, 컴퓨터는 랜덤으로 선택한다.
# 게임의 승패를 판단하여 결과를 출력한다.
# 가위는 1, 바위는 2, 보는 3으로 표현한다.
# 게임이 끝나면 계속할 지 물어본다.
import random
class RPSGame:
    def __init__(self):
        self.choices = {1: "가위", 2: "바위", 3: "보"}
    
    def get_computer_choice(self):
        return random.randint(1, 3)
    
    def get_user_choice(self):
        while True:
            try:
                user_input = int(input("가위(1), 바위(2), 보(3) 중 하나를 선택하세요: "))
                if user_input in self.choices:
                    return user_input
                else:
                    print("잘못된 입력입니다. 다시 시도하세요.")
            except ValueError:
                print("숫자를 입력하세요.")
    
    def determine_winner(self, user_choice, computer_choice):
        if user_choice == computer_choice:
            return "무승부"
        elif (user_choice == 1 and computer_choice == 3) or \
             (user_choice == 2 and computer_choice == 1) or \
             (user_choice == 3 and computer_choice == 2):           return "사용자 승리"        
        else:
            return "컴퓨터 승리"    
    def play(self):
        