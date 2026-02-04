import unittest

from project import Course, Student, University 


class TestCourse(unittest.TestCase):
    """Test cases for Course class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.course = Course('CSE1010', 3)
    
    def test_course_creation(self):
        """Test course object creation"""
        self.assertEqual(self.course.course_code, 'CSE1010')
        self.assertEqual(self.course.credits, 3)
        self.assertEqual(len(self.course.students), 0)
    
    def test_add_student(self):
        """Test adding students to a course"""
        student1 = Student('STU00001','Student_1')
        student2 = Student('STU00002','Student_2')
        
        self.course.add_student(student1)
        self.assertEqual(len(self.course.students), 1)
        
        self.course.add_student(student2)
        self.assertEqual(len(self.course.students), 2)
    
    def test_add_duplicate_student(self):
        """Test that duplicate students are not added"""
        student = Student('STU00001','Student_1')
        
        self.course.add_student(student)
        self.course.add_student(student)
        
        self.assertEqual(len(self.course.students), 1)
    
    def test_get_student_count(self):
        """Test student count method"""
        self.assertEqual(self.course.get_student_count(), 0)
        
        student1 = Student('STU00001','Student_1')
        student2 = Student('STU00002','Student_2')
        
        self.course.add_student(student1)
        self.assertEqual(self.course.get_student_count(), 1)
        
        self.course.add_student(student2)
        self.assertEqual(self.course.get_student_count(), 2)
    

class TestStudent(unittest.TestCase):
    """Test cases for Student class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.student = Student('STU00001','Student_1')
        self.course1 = Course('CSE1010', 3)
        self.course2 = Course('MATH1010', 3)
    
    def test_student_creation(self):
        """Test student object creation"""
        self.assertEqual(self.student.student_id, 'STU00001')
        self.assertEqual(self.student.name, 'Student_1')
        self.assertEqual(len(self.student.courses), 0)
    
    def test_enroll_single_course(self):
        """Test enrolling in a single course"""
        self.student.enroll(self.course1, 'A')
        
        self.assertEqual(len(self.student.courses), 1)
        self.assertEqual(self.course1.get_student_count(), 1)
    
    def test_enroll_multiple_courses(self):
        """Test enrolling in multiple courses"""
        self.student.enroll(self.course1, 'A')
        self.student.enroll(self.course2, 'B+')
        
        self.assertEqual(len(self.student.courses), 2)
    
    def test_calculate_gpa_single_course(self):
        """Test GPA calculation with one course"""
        self.student.enroll(self.course1, 'A')  
        
        expected_gpa = 4.0
        self.assertEqual(self.student.calculate_gpa(), expected_gpa)
    
    def test_calculate_gpa_multiple_courses(self):
        """Test GPA calculation with multiple courses"""
        self.student.enroll(self.course1, 'A')   
        self.student.enroll(self.course2, 'B')   
        
        expected_gpa = 3.5
        self.assertEqual(self.student.calculate_gpa(), expected_gpa)
    
    def test_calculate_gpa_with_different_credits(self):
        """Test GPA calculation with courses of different credits"""
        course3 = Course('PHYS1010', 2)
        
        self.student.enroll(self.course1, 'A')   
        self.student.enroll(course3, 'B')        
        
        expected_gpa = 3.6
        self.assertEqual(self.student.calculate_gpa(), expected_gpa)
    
    def test_calculate_gpa_no_courses(self):
        """Test GPA when student has no courses"""
        self.assertEqual(self.student.calculate_gpa(), 0.0)
    
    def test_calculate_gpa_with_failing_grade(self):
        """Test GPA calculation with F grade"""
        self.student.enroll(self.course1, 'F')   
        
        expected_gpa = 0.0
        self.assertEqual(self.student.calculate_gpa(), expected_gpa)
    
    def test_get_courses(self):
        """Test getting list of enrolled courses"""
        self.student.enroll(self.course1, 'A')
        self.student.enroll(self.course2, 'B')
        
        courses = self.student.get_courses()
        self.assertEqual(len(courses), 2)
        self.assertIn(self.course1, courses)
        self.assertIn(self.course2, courses)
    

class TestUniversity(unittest.TestCase):
    """Test cases for University class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.university = University()
    
    def test_university_creation(self):
        """Test university object creation"""
        self.assertEqual(len(self.university.students), 0)
        self.assertEqual(len(self.university.courses), 0)
    
    def test_add_course(self):
        """Test adding courses to university"""
        course = self.university.add_course('CSE1010', 3)
        
        self.assertIsNotNone(course)
        self.assertEqual(len(self.university.courses), 1)
        self.assertIn('CSE1010', self.university.courses)
    
    def test_add_duplicate_course(self):
        """Test adding duplicate course doesn't create duplicates"""
        course1 = self.university.add_course('CSE1010', 3)
        course2 = self.university.add_course('CSE1010', 3)
        
        self.assertEqual(len(self.university.courses), 1)
        self.assertIs(course1, course2)
    
    def test_add_student(self):
        """Test adding students to university"""
        student = self.university.add_student('STU001', 'Alice')
        
        self.assertIsNotNone(student)
        self.assertEqual(len(self.university.students), 1)
        self.assertIn('STU001', self.university.students)
    
    def test_add_duplicate_student(self):
        """Test adding duplicate student doesn't create duplicates"""
        student1 = self.university.add_student('STU001', 'Alice')
        student2 = self.university.add_student('STU001', 'Alice')
        
        self.assertEqual(len(self.university.students), 1)
        self.assertIs(student1, student2)
    
   
    def test_get_nonexistent_student(self):
        """Test retrieving non-existent student returns None"""
        student = self.university.get_student('STU999')
        self.assertIsNone(student)
    
    def test_get_course(self):
        """Test retrieving course by code"""
        self.university.add_course('CSE1010', 3)
        
        course = self.university.get_course('CSE1010')
        if course is not None:
            self.assertIsNotNone(course)
            self.assertEqual(course.course_code, 'CSE1010')
    
    def test_get_nonexistent_course(self):
        """Test retrieving non-existent course returns None"""
        course = self.university.get_course('XXX9999')
        self.assertIsNone(course)
    
   


def run_tests():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestCourse))
    suite.addTests(loader.loadTestsFromTestCase(TestStudent))
    suite.addTests(loader.loadTestsFromTestCase(TestUniversity))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("TEST SUMMARY")
    print("="*70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("="*70)
    
    return result


if __name__ == '__main__':
    run_tests()
    # unittest.main()
