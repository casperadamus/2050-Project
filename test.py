import unittest
import main

class TestCourse(unittest.TestCase):
    def setUp(self):
        self.courseEx=main.Course("CSE1010", 4)
        self.studentEx = None
    
    def test_objectCreation(self):
        self.assertIsInstance(self.courseExample, main.Course)
        #self.assertEqual(a.get_student_count(), 0)
    #def test_studentAdding(self):
        

if __name__ == '__main__':
    unittest.main()