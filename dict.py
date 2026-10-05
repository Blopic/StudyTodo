#dict
input_grade = input("请依次输入姓名与成绩（用逗号分隔,不同人之间用冒号分隔）：")
grade_dict = {}
for grade in input_grade.split(":"):
    name, score = grade.split(",")
    grade_dict[name] = int(score)
print("录入的成绩为：", grade_dict)

#查找与统计
search_name = input("请输入要查找的学生姓名：")
if search_name in grade_dict:
    print(search_name, "的成绩为：", grade_dict[search_name])

print("总人数：", len(grade_dict))
print("及格人数：", len([score for score in grade_dict.values() if score >= 60]))