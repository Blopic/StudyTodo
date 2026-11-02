#路由层把 HTTP 输入交给存储层，并将不存在的资源映射为 404。

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status

from api.schemas import TaskCreate, TaskResponse, TaskUpdate
from api.store import TaskStore

#这里的tags是将APIRouter下的所有接口进行分类，使得在http://127.0.0.1:8000/docs查看时方便阅览
router = APIRouter(prefix="/tasks", tags=["tasks"])


def get_store(request: Request) -> TaskStore:
    # 所有接口都从同一应用读取存储，避免各个路由各自维护一份数据。
    return request.app.state.task_store


def require_task(store: TaskStore, task_id: int) -> TaskResponse:
    task = store.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="任务不存在")
    return task 


@router.get("", response_model=list[TaskResponse])
def list_tasks(completed: bool | None = None, store: TaskStore = Depends(get_store)):
    #completed 是查询参数；省略时返回全部任务。
    return store.list(completed)

#依赖注入
@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, store: TaskStore = Depends(get_store)):
    """task_id 是路径参数，无法转换为整数时框架自动返回 422。"""
    return require_task(store, task_id)


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(request: TaskCreate, store: TaskStore = Depends(get_store)):
    #request 来自 JSON 请求体，通过模型校验后才会创建任务。
    return store.create(request)


@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, request: TaskUpdate, store: TaskStore = Depends(get_store)):
    require_task(store, task_id)
    return store.update(task_id, request)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, store: TaskStore = Depends(get_store)):
    require_task(store, task_id)
    store.delete(task_id)
    # 204 不能带 JSON；显式返回空 Response，避免生成 null 响应体。
    return Response(status_code=status.HTTP_204_NO_CONTENT)
