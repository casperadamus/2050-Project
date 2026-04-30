import csv
from datetime import date

#dict with etter grade to numbers
gradeDict = {'A':4.0,'A-':3.7,'B+':3.3,'B':3.0,'B-':2.7,'C+':2.3,'C': 2.0,'C-': 1.7,'D':1.0,'F': 0.0}
DEANGPA = 3.5

class HashMap: #Mert
    def __init__(self, capacity=8):
        self._capacity = capacity
        self._size = 0
        self._buckets = [[] for i in range(self._capacity)]
    def _hash(self, key):
        return hash(key) % self._capacity
    def _load_factor(self):
        return self._size / self._capacity
    def _rehash(self):
        old_buckets = self._buckets
        self._capacity *= 2
        self._buckets = [[] for i in range(self._capacity)]
        self._size = 0
        for bucket in old_buckets:
            for key, value in bucket: self.put(key, value)
    def put(self, key, value):
        bucket = self._buckets[self._hash(key)]
        i = 0
        for k,v in bucket:
            if k == key:
                bucket[i] = (key, value)
                return
            i+=1
        bucket.append((key,value))
        self._size +=1
        if self._load_factor()>=0.8:
            self._rehash()
    def get(self, key):
        bucket = self._buckets[self._hash(key)]
        for k,v in bucket:
            if k == key: return v
        raise KeyError("Key not found.")
    def remove(self, key):
        bucket = self._buckets[self._hash(key)]
        for k,v in bucket:
            if k == key: 
                bucket.remove((k,v))
                self._size-=1
                return
        raise KeyError("Key not found.")
    def __len__(self):
        return self._size
    def __contains__(self,key):
        index = self._hash(key)
        return any(k == key for k, v in self._buckets[index])
    def __repr__(self):
        pairs = []
        for bucket in self._buckets:
            for k,v in bucket:
                pairs.append(f"{k}: {v}")
        return "{" + ", ".join(pairs) + "}"
    
def get_key(enrollment:EnrollmentRecord, by:str): #Casper
    """Return value depending on sorting filter"""
    student = enrollment.student
    if by == "name": return int(student.name[8:])
    elif by == "id": return int(student.student_id[3:])
    elif by == "date": return enrollment.enroll_date
    else: raise ValueError("Invalid sort key")

def recursive_binary_search(records, target_id, low, high) -> int: #Casper
    if low > high: return -1
    median_number = (low+high)//2
    target_key = int(target_id[3:])
    mid_key = get_key(records[median_number], "id")
    if mid_key == target_key: return median_number
    elif mid_key > target_key: return recursive_binary_search(records, target_id, low, median_number - 1)
    else: return recursive_binary_search(records, target_id, median_number + 1, high)

def _merge_sort(students:list, by:str)->list: #Mert
    if len(students)<= 1:
        return students
    mid = len(students) // 2
    left = _merge_sort(students[:mid], by)
    right = _merge_sort(students[mid:], by)
    return _merge(left, right, by)
def _merge(left:list, right:list, by:str)->list: #Mert
    result = []
    i=j=0
    while i < len(left) and j <len(right):
        if get_key(left[i], by) <= get_key(right[j], by):
            result.append(left[i])
            i+=1
        else:
            result.append(right[j])
            j+=1
    result[len(result):] = left[i:]
    result[len(result):] = right[j:]
    return result
def _quick_sort(students:list, by:str, low:int, high:int): #Mert
    if low < high:
        pivot_idx = _partition(students, by, low, high)
        _quick_sort(students, by, low, pivot_idx - 1)
        _quick_sort(students, by, pivot_idx + 1, high)
def _partition(students:list, by:str, low:int, high:int)->int: #Mert
    pivot = get_key(students[high], by)
    i = low - 1
    for j in range(low, high):
        if get_key(students[j], by) <= pivot:
            i += 1
            students[i], students[j] = students[j], students[i]
    students[i + 1], students[high] = students[high], students[i + 1]
    return i + 1
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
        self.prerequisites = self._load_prerequisites()
    def _load_prerequisites(self) -> HashMap:
        prereqs = HashMap()
        with open("cse_prerequisites.csv", "r") as f:
            next(f)
            for line in f:
                parts = line.strip().split("\t")
                course = parts[0].strip()
                prereq = parts[1].strip() if len(parts)>1 else None

                if prereq:
                    if course in prereqs: prereqs.get(course).append(prereq)
                    else: prereqs.put(course, [prereq])
                else:
                    prereqs.put(course, [])
        return prereqs
    def _already_enrolled(self, student):
        return any(r.student is student for r in self.students)
    def sort_enrolled(self, by:str, algorithm:str) -> None:
        """Sort students list depending on the algorithm and filter"""
        if by not in ("name", "id", "date"):
            raise ValueError(f"Unknown sort key {by}")
        
        match algorithm:
            case 'merge':
                self.students = _merge_sort(self.students, by)
            case 'quick':
                _quick_sort(self.students, by, 0, len(self.students) - 1)
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
        req = self.prerequisites.get(self.course_code)
        if req: 
            if [p for p in req if p not in student.courses]:
                raise ValueError("Student has not fulfilled prereqs.")
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

def populate_courses(univ:University) -> None: #Mert
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
def populate_students(univ:University) -> None: #Mert
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
def getDeansList(uni:University) -> list: #Mert
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