# 가변 매개변수
    # 함수정의 할 때, 매개변수의 개수를 정의하지 않습니다.
    # 함수내부에서는 리스트로 간주합니다.
    # 함수를 호출하는 쪽에서는 편안하게.. 1,2,3,4 or 1,2,3,4,5,1,4,5

def myFunc1(args):
    for i in args:
        print(i)
myFunc1(10,20,50,60) #이러면 myFunc함수가 매개변수 하나만 받겠다고 했는데 내가 4개를 부여한 것이므로 error

def myFunc2(args):
    for i in args:
        print(i)
myFunc2([10,20,50,60]) #이러면 정상 작동

a,b = [10,20]