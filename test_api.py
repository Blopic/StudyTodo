import unittest

from fastapi.testclient import TestClient

from api.main import create_app


class ApiTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(create_app())

    def test_create_list_filter_and_get(self):
        created = self.client.post("/tasks", json={"title": "学习 FastAPI"})
        self.assertEqual(created.status_code, 201)
        self.assertEqual(created.json(), {"id": 1, "title": "学习 FastAPI", "completed": False})
        self.client.post("/tasks", json={"title": "复习 Git", "completed": True})
        self.assertEqual([item["id"] for item in self.client.get("/tasks?completed=true").json()], [2])
        self.assertEqual(self.client.get("/tasks/1").status_code, 200)

    def test_validation_and_extra_fields(self):
        for body in ({}, {"title": ""}, {"title": "有效", "completed": "yes"}, {"title": "有效", "other": 1}):
            with self.subTest(body=body):
                self.assertEqual(self.client.post("/tasks", json=body).status_code, 422)

    def test_patch_preserves_omitted_fields_and_accepts_false(self):
        self.client.post("/tasks", json={"title": "原标题", "completed": True})
        response = self.client.patch("/tasks/1", json={"completed": False})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"id": 1, "title": "原标题", "completed": False})
        self.assertEqual(self.client.patch("/tasks/1", json={"title": None}).status_code, 422)
        self.assertEqual(self.client.patch("/tasks/99", json={"completed": False}).status_code, 404)

    def test_delete_204_and_stable_ids(self):
        self.client.post("/tasks", json={"title": "待删除"})
        self.assertEqual(self.client.delete("/tasks/1").status_code, 204)
        self.assertEqual(self.client.get("/tasks/1").status_code, 404)
        self.assertEqual(self.client.delete("/tasks/1").status_code, 404)
        self.assertEqual(self.client.post("/tasks", json={"title": "新任务"}).json()["id"], 2)


if __name__ == "__main__":
    unittest.main()
