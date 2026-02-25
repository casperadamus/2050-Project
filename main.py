gradeDict = {'A':4.0,'A-':3.7,'B+':3.3,'B':3.0,'B-':2.7,'C+':2.3,'C': 2.0,'C-': 1.7,'D':1.0,'F': 0.0} #Letter grade to numbers

class Course: #Mert
    """Class blueprint for a course."""
    def __init__(self, code, creds, students=None):
        """Initializes 3 public variables for course"""
        self.course_code = code #string (e.g. "CSE1010")
        self.CREDITS = creds #final integer (shouldn't change)
        self.students = students if students is not None else [] #List (Student objects)

    def add_student(self, student):
        """Adds a student object to the students list"""
        if student not in self.students:
                self.students.append(student)

    def get_student_count(self):
        """Return total amount of students"""
        return len(self.students)

    def __str__(self):
        return f"{self.course_code} ({self.CREDITS} credits)"

class Student: #Mert
    def __init__(self,id,name,courses= None):
        self.student_id = id #string
        self.name = name #string
        self.courses = courses if courses is not None else {} #dict  def enroll(self, course, grade):
    
    def enroll(self, course, grade):
        """Student enroll w/ grade in course; Updates course.students list"""
        self.courses[course] = grade
        course.add_student(self)

    def update_grade(self, course, grade):
        """Modify grade of course obj"""
        self.enroll(course,grade)

    def calculate_gpa(self):
        """Returns GPA of student's courses"""
        pts=0
        creds=0
        for course, grade in self.courses:
            pts+=gradeDict.get(grade, 0)*course.CREDITS
            creds+=course.CREDITS
        return 0 if creds == 0 else round(pts/creds)


    def get_courses(self):
        """Return list of students courses objs"""
        return [course for course, v in self.courses]

    def get_course_info(self):
        """Return set including students courses code, grade, credits."""
        return {(k.course_code, v, k.CREDITS) for k,v in self.courses}

    def __str__(self):
        return f"{self.name} ({self.student_id}) GPA: {self.calculate_gpa()}"
    
class University: #Mert
    def __init__(self,id,name,courses=dict()):
        self.id = id
        self.name = name 
        students = {} #dict maps student_id -> Student object
        courses = {} #dict maps course_code -> Course object

    def add_course(self,course_code,credits):
        """Add new course from code"""
        if course_code not in self.courses:
            self.courses[course_code] = Course(course_code, credits)
        return self.courses[course_code]

    def add_student(self, student_id, name):
        """Add new student from id"""
        if student_id not in self.students:
            self.students[student_id] = Student(student_id, name)
        return self.students[student_id]
    
    def get_student(self, student_id):
        """Return student obj from id"""
        return self.students.get(student_id)

    def get_course(self, course_code):
        """Return course obj from code"""
        return self.courses.get(course_code)
        
    def get_course_enrollment(self, course_code):
        """return student count from code"""
        course = self.courses.get(course_code)
        if course:
            return course.get_student_count()

    def get_students_in_course(self, course_code):
        """Return student objs from code"""
        course = self.courses.get(course_code)
        if course:
            return course.students
