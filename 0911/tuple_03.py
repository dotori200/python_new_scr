# 튜플과 리스트의 관계
# 튜플과 리스트는 서로 변경이 가능하다.
list_a = [1,2,3]
tuple_a = (10,20,30)
print(f"type(list_a) = {type(list_a)}")
print(f"type(tuple_a) = {type(tuple_a)}")

print(tuple(list_a))  # => 원본이 바뀌는 게 아니라 그냥 반환값이 바뀐 거
list_a = tuple(list_a)  # => 원본을 바꿔주는 것