import csv

#dict with etter grade to numbers
gradeDict = {'A':4.0,'A-':3.7,'B+':3.3,'B':3.0,'B-':2.7,'C+':2.3,'C': 2.0,'C-': 1.7,'D':1.0,'F': 0.0}
DEANGPA = 3.5
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
        return f"{self.course_code}: ({self.CREDITS} credits)"

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
    students : dict
        Maps id to student obj
    courses : dict
        Maps code to course obj
    deanslist : list
        students with high GPA's
    """
    def __init__(self) -> None:
        """Initializes an University"""
        self.students, self.courses = dict(), dict()
        self.deansList = []

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
    
    def get_common_students(self, course1:Course, course2:Course) -> set:
        return set(self.get_students_in_course(course1)) & set(self.get_students_in_course(course2))

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
            std_id = row['student_id']
            student = univ.get_student(std_id)
            if not student and len(std_id) >= 8 and std_id[:3] == "STU":
                student = univ.add_student(std_id, row['name'])
                for item in row['courses'].split(";"):
                    split = item.split(":")
                    course = univ.get_course(split[0])
                    if course and split[1] in gradeDict: student.enroll(course, split[1])
                if univ.students[std_id].calculate_gpa() >= DEANGPA:
                    univ.deansList.append(std_id)
            # else:
            #     print("Duplicate or invalid student ID found:", row['student_id'])

def getDeansList(uni:University) -> list:
    objList = []
    for stdId in uni.deansList:
        objList.append(uni.get_student(stdId))
    return objList

ex_uni = University()
print("Populating course catalog...", end=" ")
populate_courses(ex_uni)
print("OK.")
print("Populating students and enrollments...", end=" ")
populate_students(ex_uni)
print("OK.")
"""
Demonstrations
--------------
Get the list of students enrolled in a course X
Print GPA of a student X
Print all the courses and course info (grades and credits) for a student 
Calculate mean and median for the GPA of all students in the university
Print common students in two different courses (Intersection)
"""

if __name__=="__main__":
    #1
    listStudents = ex_uni.get_students_in_course("CSE1010")
    if len(ex_uni.students) > 0: firstStudentObj = list(ex_uni.students.values())[0]
    else: firstStudentObj = None
    #2
    if firstStudentObj is not None:
        print(firstStudentObj.name + "'s GPA: " + str(firstStudentObj.calculate_gpa()))
        print(f"Course: (credit) | grade for {firstStudentObj.name}")
        for course, grade in firstStudentObj.courses.items():
            print(str(course) + " | Grade: " + grade) 
    else: print("No students found to demonstrate GPA")
    #mean:
    totalGPA = 0
    gpaList = list()
    for student in ex_uni.students.values(): 
        studentGPA = student.calculate_gpa()
        totalGPA+=studentGPA
        gpaList.append(studentGPA)
    length_gpaList = len(gpaList)
    meanGPA = 0
    if length_gpaList != 0: meanGPA = round(totalGPA/length_gpaList,3)
    else: raise KeyError("Cannot divide by 0, no classes found.")
    #median:
    gpaList.sort()
    medianGPA = 0
    if(length_gpaList%2==1): #odd
        medianGPA = gpaList[int(((length_gpaList+1)/2)-1)]
    elif(length_gpaList%2==0): #even
        medianGPA = round((gpaList[int((length_gpaList/2)-1)] + gpaList[int(length_gpaList/2)])/2,3)

    print("Mean GPA of all students: " + str(meanGPA))
    print("Median GPA of all students: " + str(medianGPA))

    print("Students in CSE1010 and CSE2050")
    for i in ex_uni.get_common_students("CSE1010", "CSE2050"):
        print(i)

    print(f"Dean's List: (>={DEANGPA} gpa)")
    for student in getDeansList(ex_uni): print(str(student))