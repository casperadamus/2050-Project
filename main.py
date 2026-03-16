import csv
from datetime import date

#dict with etter grade to numbers
gradeDict = {'A':4.0,'A-':3.7,'B+':3.3,'B':3.0,'B-':2.7,'C+':2.3,'C': 2.0,'C-': 1.7,'D':1.0,'F': 0.0}
DEANGPA = 3.5

class EnrollmentRecord:
    """represents a Enrollment Record

    Attributes
    ----------
    student : Student
        Student obj
    enroll_date : string
        Stores a "YYYY-MM-DD" of when object is created
    """
    def __init__(self, student, enroll_date):
        """Initializes an enrollment record"""
        self.student = student
        self.enroll_date = enroll_date

class Node:
    """represents a Node for LinkedList
    
    Attributes
    ----------
    data : Any
        Any type of data type
    next : Node
        Stores the next node in LinkedList
    """
    def __init__(self, data):
        """Initializes a Node"""
        self.data = data
        self.next = None
    
class LinkedQueue: #FIFO
    """Classic Singly LinkedQueue ADT

    Attributes
    ----------
    _head : Node
        Pointer to the first Node
    _tail : Node
        Pointer to the last Node
    _len : int
        Length of the Queue
    """
    def __init__(self):
        self._head = None
        self._tail = None
        self._len = 0
    def __len__(self): return(self._len)
    def is_empty(self): return self._len == 0
    def enqueue(self, item):
        self._len += 1
        newNode = Node(item)
        if self._head is None: self._head = newNode
        if self._tail is not None: self._tail.next = newNode
        self._tail = newNode
    def dequeue(self):
        self._len -= 1
        if self.is_empty(): raise ValueError
        headNode = self._head
        self._head = headNode.next
        return headNode.item

class Course: #Mert
    def sort_enrolled(self, by, algorithm):
        match algorithm:
            case 'selection':
                for i in self.students:
                    minObj = self.students[i]
                    for j in self.students:
                        numObj = self.students[j]
                        if by=='name' and (numObj.student.name[8:] > minObj.student.name[8:]): minObj = numObj
                        if by=="id" and (numObj.student.student_id[3:] > minObj.student.name[3:]): minObj = numObj
                        if by=="date" and (numObj.enroll_date > minObj.enroll_date): minObj = numObj
                    self.students[i], minObj = minObj, self.students[i]
            case 'insertion':
                ...
        ...

    """Represents a course

    Attributes
    ----------
    course_code : str
        The course code
    CREDITS : int
        number of credits
    capacity : int
        # of students limit
    students : list
        Students enrolled in the course
    waitlist : LinkedQueue
        LinkedQueue ADT for students waiting to enroll
    """
    def __init__(self, code:str, creds:int, capacity:int, students=None) -> None:
        """Initialize a Course"""
        self.course_code = code
        self.CREDITS = creds
        self.capacity = capacity
        self.students = students if students is not None else list()
        self.waitlist = LinkedQueue()

    def add_student(self, student: Student) -> None:
        """Add a student to the course if not already enrolled"""
        if student not in self.students:
            self.students.append(EnrollmentRecord(student))

    def get_student_count(self) -> int:
        """Returns the number of enrolled students"""
        return len(self.students)

    def __str__(self) -> str:
        """Return a human-readable course information"""
        return f"{self.course_code}: ({self.CREDITS} credits)"
    
    def request_enroll(self, student:Student, enroll_date=date.today()) -> None:
        """Add a student to the course if capacity not full"""
        if len(self.students) == self.capacity:
            self.waitlist.enqueue(EnrollmentRecord(student, enroll_date))
        else:
            for enrollmentRecord in self.students:
                if enrollmentRecord.student is not student: ValueError("Student is already enrolled.")
            self.students.append(EnrollmentRecord(student))
    
    def drop(self, student_id:str, enroll_date_for_replacement=date.today()) -> None:
        ... #remove the student from roster
        if not self.waitlist.is_empty(): self.request_enroll(self.waitlist.dequeue(), enroll_date_for_replacement)

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

    def add_course(self,course_code:str,credits:int,capacity:int) -> Course:
        """Adds a non-existing course to mapping"""
        if course_code not in self.courses:
            self.courses.setdefault(course_code, Course(course_code, credits, capacity))
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
    # with open('course_catalog.csv', 'r') as file:
    #     for line in file.readlines()[1:]:
    #         course_code, credits = line.strip().split(',')
    #         if not univ.get_course(course_code): univ.add_course(course_code, int(credits))

    with open('course_catalog_CSE10_with_capacity.csv', 'r') as file:
        for row in csv.DictReader(file):
            course_id = row['course_id']
            credits = int(row['credits'])
            capacity = int(row['capacity'])
            if not univ.get_course(course_id): univ.add_course(course_id, credits, capacity)
    
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
    """Converts the student id storing list from the University class to object list

    Paramaters
    ----------
    univ : University
        University Object
    """
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

listStudents = ex_uni.get_students_in_course("CSE1010")

