import random

def get_com_num(start=1, end=3):
    '''
    랜덤값출력(start ~ end)    
    '''
    return random.randint(start,end)

def get_human_num():
    return int(input("입력(1:가위 2:바위 3:보) :"))

def check_winner(com_choince, human_choice):
    if com_choince == human_choice:
        print('비겼습니다.')
    else:
        if (com_choince == 1 and human_choice ==2) or \
            (com_choince == 2 and human_choice ==3) or \
            (com_choince == 3 and human_choice ==1):
            print("당신이 이겼습니다.")
        else:
            print("당신이 졌습니다.")


# 랜덤하게 선택한 컴퓨터의 값
com_choince = get_com_num()
# 사용자의 값
human_choice = get_human_num()
# 승패 확인
# print(com_choince)   # 디버깅용.. 개발이 완료되면 삭제
check_winner(com_choince,human_choice)