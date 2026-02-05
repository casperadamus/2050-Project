import csv
from pprint import pprint

gradeDict = {'A':4.0,'A-':3.7,'B+':3.3,'B':3.0,'B-':2.7,'C+':2.3,'C': 2.0,'C-': 1.7,'D':1.0,'F': 0.0} #Letter grade to numbers

class Course: #Mert
    """Class blueprint for a course."""
    def __init__(self, code, creds, students=[]):
        """Initializes 3 public variables for course"""
        self.course_code = code #string (e.g. "CSE1010")
        self.CREDITS = creds #final integer (shouldn't change)
        self.students = students #List (Student objects)

    def add_student(self, student):
        """Adds a student object to the students list"""
        if student not in self.students:
                self.students.append(student)

    def get_student_count(self):
        """Return total amount of students"""
        return len(self.students)

class Student: #Mert
    def __init__(self,id,name,courses={}):
        self.student_id = id #string
        self.name = name #string
        self.courses = courses #dict
    
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
        return 0 if creds == 0 else round(pts/creds, 2)


    def get_courses(self):
        """Return list of students courses objs"""
        return [course for course, v in self.courses]

    def get_course_info(self):
        """Return set including students courses code, grade, credits."""
        return {(k.course_code, v, k.CREDITS) for k,v in self.courses}
    
class University: #Mert
    def __init__(self):
        self.students = dict() #dict maps student_id -> Student object
        self.courses = dict() #dict maps course_code -> Course object

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



#CSV reading/writing functions
def populate_courses(univ):
    with open('course_catalog.csv', 'r') as file:
        for line in file.readlines()[1:]:
            course_code, credits = line.strip().split(',')
            univ.add_course(course_code, int(credits))
    
def populate_students(univ):
    with open('university_data.csv', 'r') as file:
        for row in csv.DictReader(file):
            student = univ.get_student(row['student_id'])
            if not student and len(row['student_id']) >= 8:
                student = univ.add_student(row['student_id'], row['name'])
                for item in row['courses'].split(";"):
                    split = item.split(":")
                    course = univ.get_course(split[0])
                    if course:
                        student.enroll(course, split[1])
            # else:
            #     print("Duplicate or invalid student ID found:", row['student_id'])



def main():
    ex_uni = University()
    print("Populating course catalog...", end=" ")
    populate_courses(ex_uni)
    # pprint(ex_uni.courses)
    print("OK.")
    print("Populating students and enrollments...", end=" ")
    populate_students(ex_uni)
    # pprint(ex_uni.students)
    print("OK.")
    

main()