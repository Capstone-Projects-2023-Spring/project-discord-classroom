import unittest
from fastapi.testclient import TestClient
from api import app


class TestEndpoints(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_get_classrooms(self):
        response = self.client.get('/classrooms')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0], {'id': 1,
                                              'serverId': '1068288565806637119',
                                              'serverName': 'Test Discord Classroom'})

    def test_get_classroom_id(self):
        response = self.client.get('/classroomId', params={'server_id': 1078525927010598983})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'id': 2})


if __name__ == '__main__':
    unittest.main()
