# 가위바위보 게임 (컴퓨터 vs 화면)
# 가위 : 1, 바위 : 2, 보 : 3
# 규칙 : 컴퓨터가 임의로 숫자를 선택   = random
# 인간이 숫자를 입력                  = input
# 승패를 기록
# 3번마다 계속할 지 물어본다          = for

comp = random.randint (1,3)
human = int (input ("가위=1, 바위=2, 보=3 중에서 하나를 골라 숫자를 적으시오. : "))
if comp == human :
    print("비겼습니다.")
else:
    if (comp == 1 and human == 2) or \
       (comp == 2 and human == 3) or \
       (comp == 3 and human == 1):
       print("이겼습니다.")
    else:
        print("졌습니다.")




import random
comp = random in [0,2,5]
human = int (input ("가위=2, 바위=0, 보=5 중에서 하나를 골라 숫자를 적으시오. : "))
if comp == 0 and human == 0 :
    print ("비겼습니다.")
if comp == 0 and human == 2 :
    print ("패배")
if comp == 0 and human == 5 :
    print ("승리")
if comp == 2 and human == 0 :
    print ("승리")
if comp == 2 and human == 2 :
    print ("비겼습니다.")
if comp == 2 and human == 5 :
    print ("패배")
if comp == 5 and human == 0 :
    print ("패배")
if comp == 5 and human == 2 :
    print ("승리")
if comp == 5 and human == 5 :
    print ("비겼습니다.")


