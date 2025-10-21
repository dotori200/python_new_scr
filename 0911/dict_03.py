my_bag = {'필통':'파란색', '공책':'수학공책', '지갑':'분홍색'}
# 출력
print(my_bag)

# 가방에서 필통을 꺼내서 출력
print(my_bag['필통'])

# 가방에서 공책을 꺼내서 출력
print(my_bag['공책'])

# 지갑이 오래되서 "가죽지갑" 변경  --> # my_bag['지갑'] = '가죽지갑'
my_bag['가죽지갑']='분홍색'
del my_bag['지갑']
print(my_bag['가죽지갑'])

# 물통을 추가 (하얀색)
my_bag['물통']='하얀색'
print(my_bag['물통'])

# 공책을 다써서 버려야 됌
del my_bag['공책']
print(my_bag)

# 순환문과 연결
for i in my_bag:
    print(f'key = {i} value = {my_bag[i]}')
