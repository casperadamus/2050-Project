import csv

class Course:
    def __init__(self, course_code, credits):
        self.course_code = course_code
        self.credits = credits
        self.students = []  
    
    def add_student(self, student):
        """Add a student to this course"""
        if student not in self.students:
            self.students.append(student)
    
    def get_student_count(self):
        """Return the number of students enrolled in this course"""
        return len(self.students)
    
    def __str__(self):
        return f"{self.course_code} ({self.credits} credits)"
    


class Student:
    GRADE_POINTS = {'A': 4.0, 'A-': 3.7, 'B+': 3.3, 'B': 3.0, 'B-': 2.7, 
                    'C+': 2.3, 'C': 2.0, 'C-': 1.7, 'D': 1.0, 'F': 0.0}
    
    def __init__(self, student_id, name):
        self.student_id = student_id
        self.name = name
        self.courses = {}  # dictionary key, value => course, grade, grade starts with None 
    
    def enroll(self, course, grade): 
        """Enroll student in a course with a grade"""
        self.courses[course]=grade
        course.add_student(self)

    def grade_course(self,course,grade):
        self.enroll(course,grade)
    
    def calculate_gpa(self):
        """Calculate GPA based on all enrolled courses and grades"""
        total_points = 0
        total_credits = 0
        
        for course, grade in self.courses.items():
            grade_point = self.GRADE_POINTS.get(grade, 0.0)
            total_points += grade_point * course.credits
            total_credits += course.credits
        
        if total_credits == 0:
            return 0.0
        
        return round(total_points / total_credits, 2)
    
    def get_courses(self):
        """Return list of courses the student is enrolled in"""
        return [course for course, _ in self.courses.items()]
    
    def get_course_info(self):
        """Return formatted course information"""
        return [(course.course_code, grade, course.credits) 
                for course, grade in self.courses.items()]
    
    def __str__(self):
        return f"{self.student_id}: {self.name} (GPA: {self.calculate_gpa()})"
    


class University:
    def __init__(self):
        self.students = {}  # Dictionary: student_id -> Student object
        self.courses = {}   # Dictionary: course_code -> Course object
    
    def add_course(self, course_code, credits):
        """Add a course to the university"""
        if course_code not in self.courses:
            self.courses[course_code] = Course(course_code, credits)
        return self.courses[course_code]
    
    def add_student(self, student_id, name):
        """Add a student to the university"""
        if student_id not in self.students:
            self.students[student_id] = Student(student_id, name)
        return self.students[student_id]
    
    def get_student(self, student_id):
        """Get a student by ID"""
        return self.students.get(student_id)
    
    def get_course(self, course_code):
        """Get a course by code"""
        return self.courses.get(course_code)
    
    def get_course_enrollment(self, course_code):
        """Get the number of students enrolled in a course"""
        course = self.courses.get(course_code)
        if course:
            return course.get_student_count()
        return 0
    
    def get_all_course_enrollments(self):
        """Return enrollment count for all courses"""
        return {code: course.get_student_count() 
                for code, course in self.courses.items()}
    
    def get_students_in_course(self, course_code):
        """Get list of students enrolled in a specific course"""
        course = self.courses.get(course_code)
        if course:
            return course.students
        return []
    
    def display_statistics(self):
        """Display university statistics"""
        print(f"Total Students: {len(self.students)}")
        print(f"Total Courses: {len(self.courses)}")
        print(f"\nCourse Enrollment Statistics:")
        print(f"{'-'*60}")
        
        enrollments = self.get_all_course_enrollments()
        for course_code in sorted(enrollments.keys()):
            count = enrollments[course_code]
            credits = self.courses[course_code].credits
            print(f"{course_code:12} - {count:3} students ({credits} credits)")
        
        print(f"{'='*60}\n")


def load_data_from_csv():
    """Load data from CSV files and create University object"""
    university = University()
    
    # Load courses from course_catalog.csv
    print("Loading course catalog...")
    with open('course_catalog.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            university.add_course(row['course_code'], int(row['credits']))
    
    # Load students and their enrollments from university_data.csv
    print("Loading student data...")
    with open('university_data.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Create student
            student = university.add_student(row['student_id'], row['name'])
            
            # Parse courses string: "CSE1010:A:3;MATH1010:B+:4"
            courses_str = row['courses']
            course_entries = courses_str.split(';')
            
            for entry in course_entries:
                course_code, grade,_  = entry.split(':')
                # Get the course object from university
                course = university.get_course(course_code)
                if course:
                    # Enroll student in course with grade
                    student.enroll(course, grade)
    
    return university


def main():
    # Load data
    university = load_data_from_csv()
    
    # Display university statistics
    university.display_statistics()
    
    # Example: Display information for first 5 students
    print("\nSample Student Information:")
    student_ids = list(university.students.keys())[:5]
    for student_id in student_ids:
        student = university.get_student(student_id)
        print(f"\n{student}")
        print(f"  Enrolled Courses:")
        if student is not None:
            for course_code, grade, credits in student.get_course_info():
                print(f"    {course_code}: {grade} ({credits} credits)")
    
    # Example: Show students in a specific course
    print(f"\n{'-'*60}")
    example_course = 'CSE1010'
    students_in_course = university.get_students_in_course(example_course)
    print(f"\nStudents enrolled in {example_course}: {len(students_in_course)}")
    print(f"First 5 students:")
    for student in students_in_course[:5]:
        print(f"  {student.student_id}: {student.name}")
    
    # Example: Calculate average GPA across all students
    gpas = [student.calculate_gpa() for student in university.students.values()]
    avg_gpa = sum(gpas) / len(gpas) if gpas else 0
    print(f"\n{'-'*60}")
    print(f"Average GPA across all students: {avg_gpa:.2f}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
