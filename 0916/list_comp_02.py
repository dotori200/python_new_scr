list_01 = []
print ([i for i in range(5) if i%2==0])  

list_02 = [1,2,3,1,2,3,5,4,8]
# 2에 해당하는 인덱스를 찾아라.

print([idx for idx, value in enumerate(list_02) if value == 2])


age = 18
if age >= 20:
    result  = "성인"
else:
    result = "미성년자"

result = "성인" if age >= 20 else "미성년자"
print(result)

list_03 = [10,20,40,10,50,30,20,10]
print( [ "성인" if i >=18  else "미성년자" for i in list_03] )
