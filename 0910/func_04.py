# 다양한 매개변수
    #기본 매개변수 default parameter

#def myADD (num1,num2=0,num3):
   # return num1 + num2 + num3

# result = myADD(10,20)
# print(f'result = {result}')  
#이렇게 하면 로직에 문제가 있음 because 파라미터(매개변수)는 항상 괄호 안 첫번째부터 순서대로 부여되는데
#num2에 0을 부여해버렸지만 result 괄호 안에 2개의 값만 부여했으니 꼬여버리는 것

def myADD (num1=0,num2=0,num3=0):
    return num1 + num2 + num3

result1 = myADD()
result2 = myADD(1)
result3 = myADD(1,2)
result4 = myADD(1,2,3)

print("result1,result2,result3,result4")  
