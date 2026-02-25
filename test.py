import unittest
from main import Course, Student, University

class TestCourse(unittest.TestCase):
    """test cases for the course class"""

    def setUp(self):
        """setting up test"""
        self.course= Course("CSE1010", 4)
            
    def  test_course_creation(self):
        """test course creation"""
        self.assertIsInstance(self.course.course_code, str)
        self.assertEqual(self.course.course_code, "CSE1010")
        self.assertEqual(self.course.CREDITS, 4)
        self.assertEqual(len(self.course.students), 0)

    def test_add_student(self):
        """test addition of students"""
        student1 = Student("ABC1234", "1_Student")
        student2 = Student("DEF5678", "2_Student")

        self.course.add_student(student1)
        self.assertEqual(len(self.course.students), 1)

        self.course.add_student(student2)
        self.assertEqual(len(self.course.students), 2)

    def test_add_duplicate_student(self):
        """test duplicate students are not added"""
        student = Student("ABC1234", "1_Student")
        self.course.add_student(student)
        self.course.add_student(student)

        self.assertEqual(len(self.course.students), 1)

    def test_get_student_count(self):
        """test student count method"""
        self.assertEqual(self.course.get_student_count(), 0)

        student1 = Student("ABC1234", "1_Student")
        student2 = Student("DEF5678", "2_Student")

        self.course.add_student(student1)
        self.assertEqual(self.course.get_student_count(), 1)

        self.course.add_student(student2)
        self.assertEqual(self.course.get_student_count(), 2)


class TestStudent(unittest.TestCase):
    """Test cases for student class"""

    def setUp(self):
        self.student = Student("ABC1234", "1_Student")
        self.course1 = Course("CSE1010", 4)
        self.course2 = Course("MATH2110", 3)

    def test_student_creation(self):
        """test student creation"""
        self.assertEqual(self.student.student_id, "ABC1234")
        self.assertEqual(self.student.name, "1_Student")
        self.assertEqual(len(self.student.courses), 0)

    def test_enroll_single_course(self):
        """test one course enrollment"""
        self.student.enroll(self.course1, "A")

        self.assertEqual(len(self.student.courses), 1)
        self.assertEqual(self.course1.get_student_count(), 1)



if __name__ == '__main__':
    unittest.main()
