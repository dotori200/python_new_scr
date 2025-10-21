import random
#print( random.randint(1,5))

# 함수 정의할 땐 def
# 매개변수 (parameter) : 함수가 전달받는 값
# 인자 (argument) : 함수를 호출할 때 전달하는 값
# 반환값 (Return value) : 함수가 작업을 마치고 호출한 곳으로 돌려주는 값
    
# 함수의 구성요소
def myCalc (num1, num2) :
    ''' 
    두 개의 값을 받아서 더하는 기능
    num1과 num2는 숫자
    '''
    result = num1+num2
    return result

#1. 매개변수와 반환값이 둘 다 없는 함수
def say_hello():
    print('안녕하세요!')
#2. 매개변수는 있는데 반환값이 없는 함수
def say_hello_name(name):
    print(f"{name}님 안녕하세요!")
#3. 매개변수 없고 반환값이 있는 함수
import datetime
def get_current_time():
    return datetime.datetime.now()

say_hello()
#print(get_current_time)

# myCalc 호출
print(myCalc (5,10))
