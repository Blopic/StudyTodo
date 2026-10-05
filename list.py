while True:
    choose = input(
            "请选择功能：\n"
            "1. 录入成绩\n"
            "2. 筛选成绩\n"
            "3. 统计成绩\n"
            "4. 退出程序\n"
            "请输入选项："
        )
    
    if choose == "4":
        break
    elif choose == "1":
    #录入成绩
        grades = []
        input_grade = input("请输入成绩（不同成绩间用逗号分隔）：")
        for grade in input_grade.split(","):
            grades.append(float(grade))
        print("录入的成绩为：", grades)

    elif choose == "2":
        #筛选
        Excellent_grades = [grade for grade in grades if grade >= 90]
        Good_grades = [grade for grade in grades if 80 <= grade < 90]
        Normal_grades = [grade for grade in grades if 70 <= grade < 80]
        Pass_grades = [grade for grade in grades if 60 <= grade < 70]
        Fail_grades = [grade for grade in grades if grade < 60]
        print("筛选后的优秀成绩有：", Excellent_grades)
        print("筛选后的良好成绩有：", Good_grades)
        print("筛选后的中等成绩有：", Normal_grades)
        print("筛选后的及格成绩有：", Pass_grades)
        print("筛选后的不及格成绩有：", Fail_grades)

    elif choose == "3":
        #统计
        print("总人数：", len(grades))
        print("优秀人数：", len(Excellent_grades))
        print("良好人数：", len(Good_grades))
        print("中等人数：", len(Normal_grades))
        print("及格人数：", len(Pass_grades))
        print("不及格人数：", len(Fail_grades))
