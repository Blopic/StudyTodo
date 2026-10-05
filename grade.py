grade = int(input("请输入成绩："))
if grade >= 90:
    print("优秀")   
if grade >= 80 and grade < 90:
    print("良好")
if grade >= 70 and grade < 80:
    print("中等")
if grade >= 60 and grade < 70:  
    print("及格")
if grade < 60:
    print("不及格") 

'''
elif 写法

grade = int(input("请输入成绩："))
if grade >= 90:
    print("优秀")
elif grade >= 80:
    print("良好")
elif grade >= 70:
    print("中等")
elif grade >= 60:
    print("及格")
else:
    print("不及格")

'''