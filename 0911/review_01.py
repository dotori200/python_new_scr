# 딕셔너리
    # .items()  .keys()   .values()
dict_1 = {
    '국어' : 100,
    '영어' : 80,
    '수학' : 88
}
print(dict_1)
# 정렬

    # .items()
print(dict_1.items())

    # sorted
# max
    # max()
# enumerate
fruits = ['apple', 'banana', 'cherry']

for index, fruit in enumerate(fruits):
    print(f"{index}: {fruit}")
    # 이때 enumerate(fruits)  라는 의미는 fruits 안에 있는 값들을 (인덱스, 값 형태로 변환해줌)
def print_n_times (value,n) : 
    for i in range(n) :
        

    # 순환문에서 리스트를 감싸면 (인덱스, 리스트의 값)
# zip()
    # 여러개,; iterable 들을 각 원소를 쌍으로 하는 집합
    # (1,2), ('사과','배')
    # [(1,'사과'),(2,'배)]
# map()
    # iterable한 객체의 각 요소의 특정 함수를 적용
    # map (int, ['1', '2'])  -> [1,2]

    import collections
datas = [1,1,1,1,2,1,3,4,1,2,4,1]
print(collections.Counter(datas))