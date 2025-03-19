import unittest
from remote_execution import app

class RemoteExecutionTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_valid_code(self):
        response = self.app.post('/run_code', data={
            'code': 'print("Hello, World!")',
            'timeout': 5
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("Hello, World!", response.json['output'])

    def test_timeout(self):
        response = self.app.post('/run_code', data={
            'code': 'import time; time.sleep(10)',
            'timeout': 1
        })
        self.assertEqual(response.status_code, 500)
        self.assertIn("Execution timed out", response.json['error'])

    def test_invalid_timeout(self):
        response = self.app.post('/run_code', data={
            'code': 'print("Hello")',
            'timeout': 40  # Превышает максимальное значение
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid input", response.json['error'])

    def test_invalid_code(self):
        response = self.app.post('/run_code', data={
            'code': 'invalid python code',
            'timeout': 5
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json)

    def test_partial_output_on_timeout(self):
        response = self.app.post('/run_code', data={
            'code': 'import time; print("Start"); time.sleep(10); print("End")',
            'timeout': 1
        })
        self.assertEqual(response.status_code, 500)
        self.assertIn("Execution timed out", response.json['error'])

if __name__ == '__main__':
    unittest.main()