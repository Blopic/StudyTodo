def miniprogram():

    input_grade = input(
        "请依次输入成绩与姓名（用逗号分隔,不同人之间用冒号分隔）："
    )

    grade_dict = {}

    for grade in input_grade.split(":"):
        name, score = grade.split(",")
        grade_dict[name] = int(score)

    # 平均分
    average = sum(grade_dict.values()) / len(grade_dict)

    # 最高分
    max_score = max(grade_dict.values())

    # 等级统计
    excellent_count = 0
    good_count = 0
    normal_count = 0
    pass_count = 0
    fail_count = 0

    for value in grade_dict.values():
        if value >= 90:
            excellent_count += 1
        elif value >= 80:
            good_count += 1
        elif value >= 70:
            normal_count += 1
        elif value >= 60:
            pass_count += 1
        else:
            fail_count += 1

    level_count = {
        "优秀": excellent_count,
        "良好": good_count,
        "中等": normal_count,
        "及格": pass_count,
        "不及格": fail_count
    }

    return average, max_score, level_count

print(miniprogram())