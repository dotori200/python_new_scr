# 집합연산 가능

import random
list_a = random.sample(range(11), 7) # 0~10 까지의 수 중에서 중복되지 않은 임의의 7개
list_b = random.sample(range(11), 7)

# 중복을 허용하면서 0~10 임의의 7개 추출
# random.randint(0,10) -> 임의의 한 개 추출

list_c = []
for _ in range(7): # i의 역할이 없을 때는 그냥 언더바를 사용한다.
    list_c.append(random.randint(0,10))

# 합집합
    # 연산자 | (Enter키 위에 있음) -> 파이프 연산자 : or 이라는 뜻
set_a = {1,2,3}
set_b = {3,4,5}
union_set = set_a | set_b
print(union_set)
    # 메서드  ->  .union()  : 함수랑 다르게 변수 뒤에 붙어서 함수처럼 쓰이는 것
union_set = set_a.union(set_b)
print(union_set)

# 교집합
set_a, set_b = {1,2,3,4},{2,3,5}
    # 연산자 &  ->  and 라는 뜻
print(set_a & set_b)    
    #  메서드  .intersection()
print(set_a.intersection(set_b))    

# 차집합    
    # 연산자 - 
print(set_a  - set_b)    
    #  메서드  .difference()
print(set_a.difference(set_b))    
    

