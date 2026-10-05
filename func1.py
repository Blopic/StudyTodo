def miniprogram():
    print("欢迎使用输入成绩计算输出一体小程序,默认return所有成绩，筛选及格成绩，统计及格人数的元组")
    input_grade = input("请输入成绩（不同成绩间用逗号分隔）：")
    grades = []
    for grade in input_grade.split(","):
        grades.append(int(grade))
        print("录入的成绩为：", grades)

#筛选
    choose_grades = [grade for grade in grades if grade >= 60]
    print("筛选后的及格的成绩有：", choose_grades)

#统计
    print("及格人数：", len(choose_grades))
    return (grades, choose_grades, len(choose_grades))

#miniprogram()