#2026-10-13 Created by Solo
#2026-10-17 Secondly Created by Solo
from Task import Task
from TodoList import TodoList


#优化任务显示格式
def ShowTodolist(Todolist):
    TaskList = []
    if not any(Todolist.tasks.values()):
        print("-----当前没有待办-----")
        return TaskList
    print("\n-----当前待办-----")
    for ListTitle, Tasks in Todolist.tasks.items():
        if not Tasks:
            continue
        print(f"\n【{ListTitle}】")
        for task in Tasks:
            TaskList.append((ListTitle, task))
            # 修改为读取对象属性，字典仅用于文件存储。
            status = "已完成" if task.status == "completed" else "待完成"
            print(f"{len(TaskList)}. {task.title}\n"
                  f" 内容：{task.description}\n"
                  f" 状态：{status}")
            if task.exittime:
                print(f" 完成时间：{task.exittime}")
    print("-------------------------")
    return TaskList


def ReportSave(Todolist, message):
    # 内存修改和文件保存是两件事，检查返回值后再提示成功。
    if Todolist.save():
        print(message)
        return True
    print("保存失败：修改仅保留在内存中，请检查文件权限；退出前会再次保存。")
    return False


def main():
    #读取失败就停止启动，避免把损坏文件当成空数据覆盖。
    try:
        Todolist = TodoList.load()
    except (OSError, ValueError) as error:
        print(f"读取待办失败：{error}。请检查数据文件，原文件不会被覆盖。")
        return

    while True:
        ShowTodolist(Todolist)
        menu = input("请选择操作：\n"
            "1. 新增待办\n"
            "2. 修改待办状态\n"
            "3. 删除待办\n"
            "4. 修改标题\n"
            "5. 退出程序\n"
            "请选择："
        ).strip()

        if menu == "1":
            while True:
                Tempstring = input(
                    "请输入待办标题与内容，可选输入列表标题，用中文逗号分隔，输入 exit 返回主页："
                ).strip()
                if Tempstring == "exit":
                    break
                Parts = [part.strip() for part in Tempstring.split("，")]
                #判断Parts是否接收到2-3个元素或有无标题或有无内容，异常输入判断ing
                if len(Parts) not in (2, 3) or not Parts[0] or not Parts[1]:
                    print("请输入合法内容")
                    continue
                Title, Content = Parts[:2]
                ListTitle = Parts[2] if len(Parts) == 3 else None
                try:
                    #这里要传入关键字参数，不然按顺序调用会将ListTitle传给stasus，导致覆盖掉status的默认状态
                    AddTask = Task(Title, Content, ListTitle=ListTitle)
                    Todolist.add(AddTask)
                except ValueError as error:
                    print(f"添加失败：{error}")
                    continue
                #状态报告
                ReportSave(Todolist, "添加成功")

        elif menu in ("2", "3", "4"):
            #新写法，三个操作共用编号检查，规范代码格式，优化代码效率
            TaskList = ShowTodolist(Todolist)
            if not TaskList:
                continue
            # 获取用户选择
            change = input("请输入需要操作的待办序号：")
            #输入内容判断
            try:
                index = int(change)
            except ValueError:
                print("请输入数字")
                continue
            #序号有效性判断
            if not 1 <= index <= len(TaskList):
                print("不存在这个序号")
                continue
            # 获取选中的分类和待办字典
            # 这里取得的是 Task 对象。
            ListTitle, SelectedTask = TaskList[index - 1]
            print(f"你选择了：{SelectedTask.title}")
            if menu == "3":
                Todolist.delete(ListTitle, SelectedTask)
                ReportSave(Todolist, "删除成功")
                continue
            if menu == "4":
                try:
                    SelectedTask.rename(input("请输入新标题："))
                except ValueError as error:
                    print(error)
                    continue
                ReportSave(Todolist, "标题修改成功")
                continue

            print(f"当前状态：{SelectedTask.status}")
            print("你可以选择下列序号进行状态修改：")
            # 选择新状态
            print("1. pending")
            print("2. completed")
            #去除空白，避免输入异常
            choice = input("请输入新的状态序号：").strip()
            #输入检测
            ChoiceStatus = {"1": "pending", "2": "completed"}
            if choice not in ChoiceStatus:
                print("无效的状态选项")
                continue
            #状态与时间由 Task 方法维护，不再直接修改字典，更加模块化。
            if ChoiceStatus[choice] == "completed":
                SelectedTask.mark_completed()
            else:
                SelectedTask.mark_pending()
            ReportSave(Todolist, "状态修改成功")

        elif menu == "5":
            #保存失败时留在菜单，让用户有机会处理问题后重试。
            if ReportSave(Todolist, "保存成功"):
                print("Created by Solo")
                break
        else:
            print("请输入有效选项")


# 导入模块时不启动菜单，直接运行此文件才进入程序,养成习惯。
if __name__ == "__main__":
    main()
