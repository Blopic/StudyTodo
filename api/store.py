"""内存存储层：同一应用的路由共享同一实例，重启应用后数据清空。"""

from itertools import count

from api.schemas import TaskCreate, TaskResponse, TaskUpdate


class TaskStore:
    def __init__(self):
        self.tasks: dict[int, TaskResponse] = {}
        # 不使用 len(tasks)+1：删除中间或末尾任务后也不能复用 ID。
        self.next_id = count(1)

    def create(self, request: TaskCreate) -> TaskResponse:
        task = TaskResponse(id=next(self.next_id), **request.model_dump())
        self.tasks[task.id] = task
        return task

    def list(self, completed: bool | None = None) -> list[TaskResponse]:
        # 必须判断 is None，否则 completed=False 会被误认为没有筛选条件。
        return [task for task in self.tasks.values()
                if completed is None or task.completed == completed]

    def get(self, task_id: int) -> TaskResponse | None:
        return self.tasks.get(task_id)

    def update(self, task_id: int, request: TaskUpdate) -> TaskResponse:
        # 调用方先确认任务存在。只取实际提交字段，避免默认值覆盖原数据。
        changes = request.model_dump(exclude_unset=True)
        updated = self.tasks[task_id].model_copy(update=changes)
        self.tasks[task_id] = updated
        return updated

    def delete(self, task_id: int) -> None:
        del self.tasks[task_id]
