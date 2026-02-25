import unittest
from main import Course, Student, University

class TestCourse(unittest.TestCase):
    """test cases for the course class"""

    def setUp(self):
        """setting up test"""
        self.course= Course("CSE2050", 4)
            
    def  test_course_creation(self):
        """test course creation"""
        self.assertIsInstance(self.course.course_code, str)
        self.assertEqual(self.course.course_code, "CSE2050")
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
        self.course1 = Course("CSE2050", 4)
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

    def test_enroll_multiple_courses(self):
        """test enrollment in multiple courses"""
        self.student.enroll(self.course1, "A")
        self.student.enroll(self.course2, "B")
        self.assertEqual(len(self.student.courses), 2)

    def test_calculate_gpa(self):
        """ test gpa calculation"""
        self.student.enroll(self.course1, "A")

        expectedgpa = 4.0
        self.assertEqual(self.student.calculate_gpa(), expectedgpa)

    def test_calculate_gpa_multiple_courses(self):
        """test gpa calculation with multiple courses"""
        self.student.enroll(self.course1, "A")
        self.student.enroll(self.course2, "B")

        expectedgpa = 3.57
        self.assertEqual(self.student.calculate_gpa(), expectedgpa)

    def test_calculate_gpa_with_different_credits(self):
        """test gpa with different credits"""
        course3 = Course("BIO101", 2)
        
        self.student.enroll(self.course1, "A")
        self.student.enroll(self.course2, "B")

        expectedgpa = 3.57
        self.assertEqual(self.student.calculate_gpa(), expectedgpa)

    def test_calculate_gpa_no_courses(self):
        """test gpa calculation with no courses"""
        expectedgpa = 0.0
        self.assertEqual(self.student.calculate_gpa(), expectedgpa)

    def test_calculate_gpa_with_failing_grade(self):
        """test gpa calculation with failing grade"""
        self.student.enroll(self.course1, "F")

        expectedgpa = 0.0
        self.assertEqual(self.student.calculate_gpa(), expectedgpa)

    def test_get_courses(self):
        """test getting list of courses"""
        self.student.enroll(self.course1, "A")
        self.student.enroll(self.course2, "B")

        courses = self.student.get_courses()
        self.assertEqual(len(courses), 2)
        self.assertIn(self.course1, courses)
        self.assertIn(self.course2, courses)

class TestUniversity(unittest.TestCase):
    """test cases for university class"""

    def setUp(self):
        self.university = University()
    
    def test_university_creation(self):
        """test university obj creation"""
        self.assertEqual(len(self.university.students), 0)
        self.assertEqual(len(self.university.courses), 0)

    def test_add_course(self):
        """test adding courses to university"""
        course = self.university.add_course("CSE2050", 4)
        
        self.assertIsNotNone(course)
        self.assertEqual(course.course_code, "CSE2050")
        self.assertIn("CSE2050", self.university.courses)
    
    def test_add_duplicate_course(self):
        """test duplicate courses are not added"""
        course1 = self.university.add_course("CSE2050", 4)
        course2 = self.university.add_course("CSE2050", 4)

        self.assertEqual(course1, course2)
        self.assertEqual(len(self.university.courses), 1)

    def test_add_student(self):
        """test adding students to university"""
        student = self.university.add_student("ABC1234", "1_Student")

        self.assertIsNotNone(student)
        self.assertEqual(student.student_id, "ABC1234")
        self.assertIn("ABC1234", self.university.students)

    def test_add_duplicate_student(self):
        """test adding duplicate students does not create duplicates"""
        student1 = self.university.add_student("ABC1234", "1_Student")
        student2 = self.university.add_student("ABC1234", "1_Student")

        self.assertEqual(len(self.university.students), 1)
        self.assertIs(student1, student2)

    



if __name__ == '__main__':
    unittest.main()
