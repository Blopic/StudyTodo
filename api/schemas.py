"""请求模型校验客户端输入，响应模型限定接口输出。"""

from pydantic import BaseModel, ConfigDict, Field, StrictBool, field_validator


class TaskCreate(BaseModel):
    """新增时必须给标题；完成状态默认 false，ID 由服务端生成。"""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    title: str = Field(min_length=1)
    completed: StrictBool = False


class TaskUpdate(BaseModel):
    """字段可以省略，但显式传 null 无效；省略与置空是不同含义。"""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    title: str = Field(default=None, min_length=1)
    completed: StrictBool = None

#调用field_validator方法，对于title或者complete参数校验时先自动调用下面的reject_null方法进行初校验，mode="before"表示在正式校验前执行
    @field_validator("title", "completed", mode="before")
    @classmethod
    def reject_null(cls, value):
        # 默认值不触发此校验：{} 合法，{"title": null} 不合法。
        if value is None:
            raise ValueError("字段不能为 null；不修改时请省略该字段")
        return value


class TaskResponse(BaseModel):
    """所有任务接口使用统一输出结构。"""

    id: int
    title: str
    completed: bool
