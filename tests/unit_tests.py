import unittest
from database_test import Database_test

class TestDatabase(unittest.TestCase):

    def setUp(self):
        self.db = Database_test()

    def tearDown(self):
        self.db.close()

    def test_add_project(self):
        project_id = self.db.add_project('Test Project')
        self.assertIsNotNone(project_id)

    def test_add_note(self):
        project_id = self.db.add_project('Test Project')
        note_id = self.db.add_note(project_id, 'Test Note')
        self.assertIsNotNone(note_id)

    def test_delete_project(self):
        project_id = self.db.add_project('Test Project')
        self.db.delete_project(project_id)

    def test_get_note(self):
        project_id = self.db.add_project('Test Project')
        note_id = self.db.add_note(project_id, 'Test Note')
        note_content = self.db.get_note(project_id)
        self.assertEqual(note_content, 'Test Note')

if __name__ == '__main__':
    unittest.main()
