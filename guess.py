import random
num=random.randint(1,100)
count = 0
guess = input("猜一个1-100的数字，你总共有三次机会")
guess = int(guess)
while count < 3:
    if guess>100 or guess<1:
     print("请输入合法的数字") 
     break
    if guess == num:
        print("恭喜你猜对了！")
        break
    else:
      count = count + 1
      if int(count) == 3:
        print("你已经没有机会了，正确的数字是" + str(num))
        break
      if guess > num:
        print("你猜的数字大了")
      else:
        print("你猜的数字小了")
      guess = int(input("请重新试试,你还有" + str(3-count) + "次机会"))