class Course: #Mert
    """Class blueprint for a course."""
    def __init__(self, code, creds, students=[]):
        """Initializes 3 public variables for """
        self.course_code = code #string (e.g. "CSE1010")
        self.CREDITS = creds #final integer (shouldn't change)
        self.students = students #List (Student objects)

    def add_student(self, student):
        """Adds a student object to the students list of the course."""
        for i in self.students:
            if i!=student:
                self.students.append(student)

    def get_student_count(self):
        """Return total amount of students in the course."""
        return len(self.students)
"""
class Student: #Mert (In Progress)
    def __init__(self,id,name,courses):
        self.student_id = id #string
        self.name = name #string
        self.courses = courses #dict
    
    def enroll(self, course, grade):
        #— enrolls the student in a course with the given grade and updates the course roster

    def update_grade(self, course, grade):
        #modify the student grade for a particular course

    def calculate_gpa(self):
        #modify the student grade for a particular course

    def get_courses(self):
        #returns a list of course objects taken by the student.

    def get_course_info(self):
        #returns a structured summary of all enrollments, including course code, grade, and credits.
"""  