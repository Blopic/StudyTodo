from datetime import datetime

from Task import Task
from storage import LoadTodolist, SaveTodolist


class TodoList:
    #集合保存 Task 对象；只有读写文件时才转换成字典。
    def __init__(self):
        self.tasks = {}

    #添加待办
    def add(self, task):
        ListTitle = task.ListTitle
        if not ListTitle:
            ListTitle = f"Todotask_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        task.ListTitle = ListTitle
        #setdefault用于获取指定键的值，如果键不存在，则将其设置为默认值（这里是一个空列表），并返回该默认值。
        self.tasks.setdefault(ListTitle, []).append(task)

    #删除待办
    def delete(self, ListTitle, task):
        self.tasks[ListTitle].remove(task)
        # 判断删除分类的最后一条任务后，不再展示空分类。
        if not self.tasks[ListTitle]:
            del self.tasks[ListTitle]

    def save(self):
        data = {title: [task.getTask() for task in tasks]
                for title, tasks in self.tasks.items()}
        return SaveTodolist(data)

    #这里使用类方法来加载数据，因为是从运行的文件中读取数据，此时TodoList类还没创建对象，因此通过类方法创建行对象cls()，并将读取的数据放入此对象
    @classmethod
    def load(cls):
        data = LoadTodolist()
        todo = cls()
        for title, records in data.items():
            if not title.strip() or not isinstance(records, list):
                raise ValueError("每个列表必须有非空标题，并包含任务数组")
            todo.tasks[title] = [Task.from_dict(record, title) for record in records]
        return todo
