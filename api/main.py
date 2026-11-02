"""启动入口：python -m uvicorn api.main:app --reload。"""

from fastapi import FastAPI

from api.routes import router
from api.store import TaskStore


def create_app() -> FastAPI:
    #每个应用单独建立存储，测试不会污染运行中的应用或 CLI 文件。
    application = FastAPI(title="StudyTodo API", version="1.0.0")
    application.state.task_store = TaskStore()
    #将router注册为fastapi的接口
    application.include_router(router)

    @application.get("/health", tags=["health"])
    def health():
        return {"status": "ok"}

    return application


app = create_app()
