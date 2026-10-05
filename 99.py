'''
用 while 循环实现九九乘法表
before = 1
while before <= 9:
    after = 1
    while after <= before:
      print(before,"*",after,"=",before*after,end="  ")
      after += 1
    print()
    before += 1
'''



#用 for 循环实现九九乘法表
for i in range(1, 10):
    for j in range(1, i + 1):
        print(j, "*", i, "=", i * j, end="  ")
    print()


