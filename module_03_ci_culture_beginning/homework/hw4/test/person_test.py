import unittest
import datetime
from person import Person


class TestPerson(unittest.TestCase):
    def setUp(self):
        self.person = Person(name='John Doe', year_of_birth=1990, address='123 Main St')

    def test_get_age(self):
        current_year = datetime.datetime.now().year
        expected_age = current_year - self.person.yob
        self.assertEqual(self.person.get_age(), expected_age)

    def test_get_name(self):
        self.assertEqual(self.person.get_name(), 'John Doe')

    def test_set_name(self):
        self.person.set_name('Jane Doe')
        self.assertEqual(self.person.get_name(), 'Jane Doe')

    def test_set_address(self):
        self.person.set_address('456 Elm St')
        self.assertEqual(self.person.get_address(), '456 Elm St')

    def test_get_address(self):
        self.assertEqual(self.person.get_address(), '123 Main St')

    def test_is_homeless_with_address(self):
        self.assertFalse(self.person.is_homeless())

    def test_is_homeless_without_address(self):
        homeless_person = Person(name='Jane Doe', year_of_birth=1985)
        self.assertTrue(homeless_person.is_homeless())


if __name__ == '__main__':
    unittest.main()
