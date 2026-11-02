# 第四周作业：FastAPI CRUD 与 Git

本周在第三周查询接口基础上加入任务的新增、查询、修改、删除，练习 JSON 请求体、Pydantic 校验、HTTP 状态码、APIRouter 路由组织和 Git 提交。API 使用进程内字典，重启服务会清空数据；数据库持久化留到后续周次。

## 接口清单

| 方法 | 地址 | 请求/用途 | 成功响应 |
| --- | --- | --- | --- |
| GET | /health | 检查服务是否启动 | 200 |
| POST | /tasks | title 必填，completed 默认为 false | 201 + 新任务 |
| GET | /tasks?completed=false | 查询全部或按完成状态筛选 | 200 + 数组 |
| GET | /tasks/{task_id} | 按 ID 查询 | 200；不存在为 404 |
| PATCH | /tasks/{task_id} | 只提交要改变的字段 | 200；不存在为 404 |
| DELETE | /tasks/{task_id} | 删除任务 | 204 空响应；不存在为 404 |

输入模型拒绝缺少标题、空标题、错误类型、额外字段和显式 null，FastAPI 会返回 422。PATCH 使用 exclude_unset=True，所以省略字段会保留原值，显式 completed=false 也能正确生效。ID 使用递增计数器，删除后不会复用旧 ID。

## 代码阅读方向

1. api/schemas.py：分清新增、部分更新和响应模型；StrictBool 避免字符串悄悄转换成布尔值。
2. api/store.py：只处理内存数据，不处理 HTTP；观察 completed is None 与 exclude_unset=True 的作用。
3. api/routes.py：路由负责参数接收、状态码和 404；Depends 让每个接口使用同一存储实例。
4. api/main.py：创建应用、注册路由和健康检查；create_app() 让测试得到相互隔离的应用。
5. test_api.py：覆盖正常 CRUD、筛选、422 校验、部分更新、404、204 和删除后的 ID 稳定性。

## 启动与验证

    python -m venv .venv
    .venv\\Scripts\\Activate.ps1
    python -m pip install -r requirements.txt
    python -m uvicorn api.main:app --reload

浏览器打开 http://127.0.0.1:8000/docs 可使用 Swagger UI；/health 应返回 {"status":"ok"}。测试命令：python -m unittest -v。

## Git 任务方向

    git status
    git add api requirements.txt test_api.py WEEK4.md README.md .gitignore
    git diff --cached
    git commit -m "feat: add FastAPI task CRUD"
    git push -u origin <your-branch>

练习分支创建、分阶段提交、diff 检查、推送和从 GitHub 克隆后按 README 启动。不要提交 .venv/、__pycache__/ 或个人数据文件；提交前用 git status 确认暂存内容。
