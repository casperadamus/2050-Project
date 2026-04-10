import csv
from datetime import date

#dict with etter grade to numbers
gradeDict = {'A':4.0,'A-':3.7,'B+':3.3,'B':3.0,'B-':2.7,'C+':2.3,'C': 2.0,'C-': 1.7,'D':1.0,'F': 0.0}
DEANGPA = 3.5

def get_key(enrollment:EnrollmentRecord, by:str):
        """Return value depending on sorting filter"""
        student = enrollment.student
        if by == "name": return int(student.name[8:])
        elif by == "id": return int(student.student_id[3:])
        elif by == "date": return enrollment.enroll_date
        else: raise ValueError("Invalid sort key")

def recursive_binary_search(records, target_id, low, high) -> int:
        if low > high: return -1
        median_number = (low+high)//2
        target_key = int(target_id[3:])
        mid_key = get_key(records[median_number], "id")
        if mid_key == target_key: return median_number
        elif mid_key > target_key: return recursive_binary_search(records, target_id, low, median_number - 1)
        else: return recursive_binary_search(records, target_id, median_number + 1, high)

class EnrollmentRecord: #Mert
    """represents an Enrollment Record

    Attributes
    ----------
    student : Student
        Student obj
    enroll_date : datetime.date
        Stores a "YYYY-MM-DD" of when object is created
    """
    def __init__(self, student, enroll_date=date.today()):
        """Initializes an enrollment record"""
        self.student = student
        self.enroll_date = enroll_date
class Node: #Mert
    """represents a Node for LinkedList
    
    Attributes
    ----------
    data : Any
        Any type of data type
    next : Node
        Stores the next node in LinkedList (can be None)
    """
    def __init__(self, data):
        """Initializes a Node"""
        self.data = data
        self.next = None
class LinkedQueue: #Mert
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
        self._head = self._tail = None
        self._len = 0
    def __len__(self): return self._len
    def is_empty(self): return len(self) == 0
    def enqueue(self, item):
        self._len += 1
        newNode = Node(item)
        if self._head is None: self._head = newNode
        if self._tail is not None: self._tail.next = newNode
        self._tail = newNode
    def dequeue(self):
        if self.is_empty(): raise ValueError("Queue is empty")
        self._len -= 1
        headNode = self._head
        self._head = headNode.next
        if self._head is None: self._tail = None
        return headNode.data
class Course: #Mert
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
    enrolled_sorted_by_attribute : str or None
        The algorithm used to sort students
    """
    def __init__(self, code:str, creds:int, capacity:int, students=None) -> None:
        """Initialize a Course"""
        self.course_code = code
        self.CREDITS = creds
        self.capacity = capacity
        self.students = students if students is not None else list()
        self.waitlist = LinkedQueue()
        self.enrolled_sorted_by_attribute = None
        self.studentCount = 0
    def _already_enrolled(self, student):
        return any(r.student is student for r in self.students)
    def sort_enrolled(self, by:str, algorithm:str) -> None:
        """Sort students list depending on the algorithm and filter"""
        if by not in ("name", "id", "date"):
            raise ValueError(f"Unknown sort key {by}")
        students = self.students
        n = len(students)
        match algorithm:
            case 'selection':
                for i in range(n):
                    min_index = i
                    for j in range(i+1, n):
                        if get_key(students[j], by) < get_key(students[min_index],by): min_index = j
                    students[i], students[min_index] = students[min_index], students[i]
            case 'insertion':
                for i in range(1, n):
                    j = i-1
                    value = students[i]
                    while j>=0 and (get_key(students[j], by) > get_key(value, by)):
                        students[j+1] = students[j]
                        j-=1
                    students[j+1] = value
            case _: raise ValueError(f"Not an integrated sorting algorithm :{str(algorithm)}")
        self.enrolled_sorted_by_attribute = by
    def add_student(self, student: Student) -> None:
        """Add a student to the course if not already enrolled"""
        if not self._already_enrolled(student): self.students.append(EnrollmentRecord(student, date.today()))
        self.studentCount+=1
        self.enrolled_sorted_by_attribute = None
    def get_student_count(self) -> int:
        """Returns the number of enrolled students"""
        return self.studentCount
    def __str__(self) -> str:
        """Return a human-readable course information"""
        return f"{self.course_code}: ({self.CREDITS} credits)"
    def request_enroll(self, student:Student, enroll_date=date.today()) -> None:
        """Add a student to the course if capacity not full"""
        if self._already_enrolled(student): return
        if len(self.students) >= self.capacity:
            self.waitlist.enqueue(EnrollmentRecord(student, enroll_date))
        else:
            self.students.append(EnrollmentRecord(student, enroll_date))
            self.studentCount+=1
            self.enrolled_sorted_by_attribute = None 
    def drop(self, student_id:str, enroll_date_for_replacement=date.today()) -> None:
        if not self.students: raise ValueError("No students enrolled")
        if self.enrolled_sorted_by_attribute !=  "id": raise ValueError("Students not sorted by id.")
        self.studentCount-=1
        idx = recursive_binary_search(self.students, student_id, 0, len(self.students)-1 )
        if idx == -1: raise ValueError("Student not found")
        self.students.pop(idx)
        if not self.waitlist.is_empty(): self.request_enroll(self.waitlist.dequeue().student, enroll_date_for_replacement); self.enrolled_sorted_by_attribute = None
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

if __name__ == "__main__":
    ex_uni = University()
    print("Populating course catalog...", end=" ")
    populate_courses(ex_uni)
    print("OK.")
    print("Populating students and enrollments...", end=" ")
    populate_students(ex_uni)
    print("OK.")