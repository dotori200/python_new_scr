# 람다가 사용되지 않는 상황

def add (a,b):
    return a+b

def minus (a,b):
    return a-b

def calc (func,a,b):
    return func (a,b)

print(calc(add,1,2)) #디버깅 했을 떄 왜 마지막에 calc 한번 거치는 지 
    