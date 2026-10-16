# Created by Chatgpt 异常模拟与测试
import contextlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import main
import storage
from Task import Task
from TodoList import TodoList


class TodoTests(unittest.TestCase):
    def setUp(self):
        # 测试只读写临时目录，保护真实待办数据。
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "data" / "todos.json"
        patcher = patch.object(storage, "DATA_FILE", self.path)
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_object_state_and_independence(self):
        first = Task("A", "内容")
        second = Task("B", "内容")
        first.mark_completed()
        completed_at = first.exittime
        first.mark_completed()
        self.assertEqual(first.status, "completed")
        self.assertTrue(completed_at)
        self.assertEqual(first.exittime, completed_at)
        first.rename("新标题")
        self.assertEqual(second.title, "B")
        self.assertEqual(second.status, "pending")
        with self.assertRaises(ValueError):
            first.rename("  ")
        first.mark_pending()
        self.assertIsNone(first.exittime)
        self.assertEqual(first.status, "pending")

    def test_real_json_roundtrip_and_delete(self):
        todo = TodoList.load()
        self.assertEqual(todo.tasks, {})
        first = Task("A", "内容", ListTitle="学习")
        first.mark_completed()
        todo.add(first)
        todo.add(Task("B", "内容", ListTitle="学习"))
        self.assertTrue(todo.save())
        loaded = TodoList.load()
        task = loaded.tasks["学习"][0]
        self.assertIsInstance(task, Task)
        self.assertEqual(task.getTask(), first.getTask())
        for task in list(loaded.tasks["学习"]):
            loaded.delete("学习", task)
        self.assertEqual(loaded.tasks, {})
        self.assertTrue(loaded.save())
        self.assertEqual(TodoList.load().tasks, {})

    def test_invalid_data_does_not_get_overwritten(self):
        self.path.parent.mkdir()
        for content in ('{broken', '{"学习": [{}]}', '[]', '{"学习": {}}'):
            with self.subTest(content=content):
                self.path.write_text(content, encoding="utf-8")
                with patch("builtins.input", side_effect=AssertionError("不应进入菜单")):
                    with contextlib.redirect_stdout(io.StringIO()) as output:
                        main.main()
                self.assertIn("读取待办失败", output.getvalue())
                self.assertEqual(self.path.read_text(encoding="utf-8"), content)

    def test_cli_and_failed_save(self):
        inputs = ["x", "1", "，内容", "A，内容，学习", "exit",
                  "2", "abc", "2", "99", "2", "1", "x",
                  "2", "1", "2", "5", "1", "新标题", "4"]
        with patch("builtins.input", side_effect=inputs):
            with contextlib.redirect_stdout(io.StringIO()) as output:
                main.main()
        self.assertEqual(output.getvalue().count("状态修改成功"), 1)
        task = TodoList.load().tasks["学习"][0]
        self.assertEqual(task.title, "新标题")
        self.assertEqual(task.status, "completed")
        before = self.path.read_bytes()
        with patch.object(Path, "replace", side_effect=PermissionError("测试权限错误")):
            with contextlib.redirect_stdout(io.StringIO()) as output:
                self.assertFalse(main.ReportSave(TodoList.load(), "状态修改成功"))
        self.assertNotIn("状态修改成功", output.getvalue())
        self.assertEqual(self.path.read_bytes(), before)
        self.assertFalse(self.path.with_name("todos.json.tmp").exists())
        with patch("builtins.input", side_effect=["3", "1", "4"]):
            with contextlib.redirect_stdout(io.StringIO()):
                main.main()
        self.assertEqual(TodoList.load().tasks, {})


if __name__ == "__main__":
    unittest.main()
