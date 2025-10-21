# 저금통
list_a = [100,500,10,500,100,50,500,10]
# 저금통에 들어있는 동전의 종류 ->10,50,100,500

# 셋
set_a = {1,2,3,1,2,3,1}
print (f"set_a = {set_a}")

#중복을 제거(허용하지 않는다)한다.
print (set(list_a))

#셋은 순서를 신경쓰지 않는다 => 무의미하다
set_b ={1,2}
 # print(set_b[0]) -> 셋은 순서를 모르기 때문에 0번째 인덱스를 출력하지 못하는 것
set_b.add(3)
print(set_b)

set_b.remove(2)
print(set_b)
