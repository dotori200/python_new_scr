# 셋은 집합 연산이 가능하다.
import random
list_a = random.sample(range(10), 6)
list_b = random.sample(range(10), 4)
find_list = []
for a in list_a :
    for b in list_b :
        if a==b :
            find_list.append(a)

print(f'list_a = {list_a}')            
print(f'list_b = {list_b}')            
print(f'find_list = {find_list}')         
print(f'set(find_list) = {set(find_list)}')

# 13라인에서 set을 사용하지 않고 원래 로직(6~9라인)을 개선해서 
# find_list에 중복값이 저장되지 않도록 하여라.

