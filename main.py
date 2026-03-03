import csv

#dict with etter grade to numbers
gradeDict = {'A':4.0,'A-':3.7,'B+':3.3,'B':3.0,'B-':2.7,'C+':2.3,'C': 2.0,'C-': 1.7,'D':1.0,'F': 0.0}

class Course: #Mert
    """Represents a course

    Attributes
    ----------
    course_code : str
        The course code
    CREDITS : int
        number of credits
    students : list
        Students enrolled in the course
    """
    def __init__(self, code:str, creds:int, students=None) -> None:
        """Initialize a Course"""
        self.course_code = code
        self.CREDITS = creds
        self.students = students if students is not None else list()

    def add_student(self, student: Student) -> None:
        """Add a student to the course if not already enrolled"""
        if student not in self.students: self.students.append(student)

    def get_student_count(self) -> int:
        """Returns the number of enrolled students"""
        return len(self.students)

    def __str__(self) -> str:
        """Return a human-readable course information"""
        return f"{self.course_code} ({self.CREDITS} credits)"

class Student: #Mert
    """Represents a student

    Attributes
    ----------
    student_id : str
        id of student
    name : str
        name of student
    courses : dict
        enrolled courses
    """
    def __init__(self,id:str,name:str,courses=None) -> None:
        """Initializes a student"""
        self.student_id = id
        self.name = name
        self.courses = courses if courses is not None else dict()
    
    def enroll(self, course: Course, grade:str) -> None:
        """Enrolls student to course with a grade"""
        self.courses.setdefault(course,grade)
        course.add_student(self)

    def update_grade(self, course: Course, grade:str) -> None:
        """Changes the grade of the student for select course"""
        if course in self.courses: self.courses[course] = grade

    def calculate_gpa(self) -> int:
        """Returns GPA"""
        pts = creds = 0 
        for course, grade in self.courses.items():
            pts+=gradeDict.get(grade, 0)*course.CREDITS
            creds+=course.CREDITS
        return 0 if creds == 0 else round(pts/creds, 2)

    def get_courses(self) -> list:
        """returns enrolled courses"""
        return list(self.courses)

    def get_course_info(self) -> set:
        """returns course information for student"""
        return {(course.course_code, grade, course.CREDITS) for course, grade in self.courses.items()}

    def __str__(self) -> str:
        """Return a human-readable student information"""
        return f"{self.name} ({self.student_id}) GPA: {self.calculate_gpa()}"
    
class University: #Mert
    """represents a University
    
    Attributes
    ----------
    student : dict
        Maps id to student obj
    courses : dict
        Maps code to course obj

    """
    def __init__(self) -> None:
        """Initializes an University"""
        self.students, self.courses = dict(), dict()

    def add_course(self,course_code:str,credits:int) -> Course:
        """Adds a non-existing course to mapping"""
        if course_code not in self.courses:
            self.courses.setdefault(course_code, Course(course_code, credits))
        return self.courses.get(course_code)

    def add_student(self, student_id:str, name:str) -> Student:
        """Adda a non-existing student to mapping"""
        if student_id not in self.students:
            self.students.setdefault(student_id, Student(student_id, name))
        return self.students.get(student_id)
    
    def get_course(self, course_code:str) -> Course:
        """Return course obj from code"""
        return self.courses.get(course_code)
        
    def get_student(self, student_id:str) -> Student:
        """Return student obj from id"""
        return self.students.get(student_id)

    def get_course_enrollment(self, course_code:str) -> int:
        """returns student count"""
        course = self.courses.get(course_code)
        if course is None: raise KeyError(f"course '{course_code}' not found.")
        return course.get_student_count()

    def get_students_in_course(self, course_code:str) -> list:
        """Return list of students in course"""
        course = self.courses.get(course_code)
        if course is None: raise KeyError(f"course '{course_code}' not found.")
        return course.students

def populate_courses(univ:University) -> None: #Ismam
    """Populates the University with course information in course_catalog.csv

    Parameters
    ----------
    univ : University
        University object
    """
    with open('course_catalog.csv', 'r') as file:
        for line in file.readlines()[1:]:
            course_code, credits = line.strip().split(',')
            if not univ.get_course(course_code): univ.add_course(course_code, int(credits))
    
def populate_students(univ:University) -> None: #Ismam
    """Populates the University with information from university_data.csv

    Parameters
    ----------
    univ : University
        University object
    """
    with open('university_data.csv', 'r') as file:
        for row in csv.DictReader(file):
            student = univ.get_student(row['student_id'])
            if not student and len(row['student_id']) >= 8 and row['student_id'][:3] == "STU":
                student = univ.add_student(row['student_id'], row['name'])
                for item in row['courses'].split(";"):
                    split = item.split(":")
                    course = univ.get_course(split[0])
                    if course and split[1] in gradeDict: student.enroll(course, split[1])
            # else:
            #     print("Duplicate or invalid student ID found:", row['student_id'])

if __name__=="__main__":
    ex_uni = University()
    print("Populating course catalog...", end=" ")
    populate_courses(ex_uni)
    print("OK.")
    print("Populating students and enrollments...", end=" ")
    populate_students(ex_uni)
    print("OK.")