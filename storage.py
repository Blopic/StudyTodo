from pathlib import Path
import json

# 获取当前 Python 文件所在目录，并构造数据文件路径，避免终
DATA_FILE = Path(__file__).parent / "data" / "todos.json"

def LoadTodolist():
    # 创建父级目录
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

    # 文件不存在时，创建一个空字典
    if not DATA_FILE.is_file():
        DATA_FILE.write_text("{}", encoding="utf-8")
        return {}

    # 读取文件内容
    text = DATA_FILE.read_text(encoding="utf-8")

    # 文件存在，但内容为空或只有空白，换行符
    if not text.strip():
        DATA_FILE.write_text("{}", encoding="utf-8")
        return {}

    # 解析 JSON
    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        raise ValueError(f"todos.json 的 JSON 格式有误：{e}") from e

    # 确保读取出来的是字典
    if not isinstance(data, dict):
        raise ValueError("todos.json 的最外层数据必须是一个 JSON 对象")

    return data


def SaveTodolist(Todolist):
    #字典属性校验
    if not isinstance(Todolist, dict):
        raise ValueError("待办数据必须是一个字典")
    
    temp_file = DATA_FILE.with_name(DATA_FILE.name + ".tmp")

    try:
        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

        # 先将数据写入临时文件，避免写入过程中出现异常导致正式文件损坏
        with open(temp_file, "w", encoding="utf-8") as f:
            json.dump(Todolist,f,ensure_ascii=False,indent=4)

        # 临时文件写入成功后，再替换正式文件
        temp_file.replace(DATA_FILE)
        return True

    except PermissionError as e:
        print(f"没有文件写入权限：{e}")

    except OSError as e:
        print(f"文件写入或替换失败：{e}")

    except (TypeError, ValueError) as e:
        print(f"待办数据无法转换为 JSON：{e}")
    finally:
        # 如果临时文件存在，尝试删除，避免多余占用
        if temp_file.exists():
            try:
                temp_file.unlink()
            except OSError as e:
                print(f"无法删除临时文件 {temp_file}：{e}")

    return False