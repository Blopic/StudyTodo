#定义单条任务卡片，能获取自身状态与信息
from datetime import datetime

class Task:
    # 初始化任务卡片，设置标题、描述、状态、添加时间、退出时间和列表标题（若为传入标题，则采用Todotask加当前时间的组合避免出现重复写入报错）
    def __init__(self, Title, description, status="pending",addtime=None,exittime=None,ListTitle=None):
        # 在对象入口检查数据，菜单输入和 JSON 恢复都使用同一套规则，规范代码
        if not isinstance(Title, str) or not Title.strip():
            raise ValueError("任务标题不能为空")
        if not isinstance(description, str) or not description.strip():
            raise ValueError("任务内容不能为空")
        if status not in ("pending", "completed"):
            raise ValueError("任务状态必须是 pending 或 completed")
        if ListTitle is not None and not isinstance(ListTitle, str):
            raise ValueError("列表标题必须是字符串")
        for value in (addtime, exittime):
            if value is not None and not isinstance(value, str):
                raise ValueError("任务时间必须是字符串或空值")
        self.title = Title
        self.description = description
        self.status = status
        self.ListTitle = ListTitle
        if addtime is None:
            self.addtime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            self.addtime = addtime

        self.exittime = exittime

    #修改待办状态
    def mark_completed(self):
        #状态和完成时间一起更新；重复标记不覆盖原完成时间。
        if self.status != "completed":
            self.exittime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.status = "completed"

    def mark_pending(self):
        self.status = "pending"
        self.exittime = None

    def rename(self, title):
        # 【新增】方法只修改当前对象，其他任务不会跟着变化。
        if not isinstance(title, str) or not title.strip():
            raise ValueError("任务标题不能为空")
        self.title = title.strip()

    @classmethod
    def from_dict(cls, data, ListTitle):
        # 【新增】JSON 读出来的是字典，需要显式恢复成 Task 实例。
        required = {"Title", "Description", "Status", "StartTime", "exittime"}
        if not isinstance(data, dict) or not required.issubset(data):
            raise ValueError("任务数据缺少必要字段")
        return cls(data["Title"], data["Description"],
                   status=data["Status"], addtime=data["StartTime"],
                   exittime=data["exittime"], ListTitle=ListTitle)


    #获取任务信息
    def getTask(self):
        return {
            "Title": self.title,
            "Description": self.description,
            "Status": self.status,
            "StartTime": self.addtime,
            "exittime": self.exittime
        }
    
