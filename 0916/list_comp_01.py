import random
total = []
for i in range (5):
    total.append(random.randint(1,10))
print(total)


print ([ i for i in range(5)] ) # 0~4
print ([random.randint(1,10) for i in range(5)])  # 1~10 난수 5개
