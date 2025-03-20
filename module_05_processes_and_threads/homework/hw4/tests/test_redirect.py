import unittest
import sys
import io
from redirect import Redirect


class TestRedirect(unittest.TestCase):
    def test_redirect_stdout(self):
        """
        Тест: перенаправление stdout в файл.
        """
        stdout_file = io.StringIO()
        with Redirect(stdout=stdout_file):
            print('stdout')
        self.assertEqual(stdout_file.getvalue().strip(), 'stdout')

    def test_redirect_stderr(self):
        """
        Тест: перенаправление stderr в файл.
        """
        stderr_file = io.StringIO()
        with Redirect(stderr=stderr_file):
            print('stderr', file=sys.stderr)
        self.assertEqual(stderr_file.getvalue().strip(), 'stderr')

    def test_redirect_both(self):
        """
        Тест: перенаправление stdout и stderr в разные файлы.
        """
        stdout_file = io.StringIO()
        stderr_file = io.StringIO()
        with Redirect(stdout=stdout_file, stderr=stderr_file):
            print('stdout')
            try:
                raise ValueError('stderr exception')
            except ValueError:
                print('stderr', file=sys.stderr)
        self.assertEqual(stdout_file.getvalue().strip(), 'stdout')
        self.assertIn('stderr', stderr_file.getvalue().strip())

    def test_no_redirect(self):
        """
        Тест: отсутствие перенаправления (потоки остаются без изменений).
        """
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        with Redirect():
            self.assertEqual(sys.stdout, old_stdout)
            self.assertEqual(sys.stderr, old_stderr)

    def test_redirect_stdout_only(self):
        """
        Тест: перенаправление только stdout.
        """
        stdout_file = io.StringIO()
        old_stderr = sys.stderr
        with Redirect(stdout=stdout_file):
            print('stdout')
            self.assertEqual(sys.stderr, old_stderr)
        self.assertEqual(stdout_file.getvalue().strip(), 'stdout')

    def test_redirect_stderr_only(self):
        """
        Тест: перенаправление только stderr.
        """
        stderr_file = io.StringIO()
        old_stdout = sys.stdout
        with Redirect(stderr=stderr_file):
            print('stderr', file=sys.stderr)
            self.assertEqual(sys.stdout, old_stdout)
        self.assertEqual(stderr_file.getvalue().strip(), 'stderr')


if __name__ == '__main__':
    with open('test_results.txt', 'a') as test_file_stream:
        runner = unittest.TextTestRunner(stream=test_file_stream)
        unittest.main(testRunner=runner)