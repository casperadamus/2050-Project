import unittest
from datetime import date
from main import Course, EnrollmentRecord, LinkedQueue, Node, Student, recursive_binary_search


class TestLinkedQueue(unittest.TestCase): # casper
    """test cases for linked queue class"""

    def setUp(self):
        """setting up test"""
        self.queue = LinkedQueue()

    def test_fifo_order(self):
        """test fifo order of enqueue and dequeue"""
        self.queue.enqueue("a")
        self.queue.enqueue("b")
        self.queue.enqueue("c")
        self.assertEqual(self.queue.dequeue(), "a")
        self.assertEqual(self.queue.dequeue(), "b")
        self.assertEqual(self.queue.dequeue(), "c")
        self.assertTrue(self.queue.is_empty())

    def test_dequeue_empty_raises(self):
        """test dequeue on empty queue raises"""
        with self.assertRaises(ValueError):
            self.queue.dequeue()

    def test_len_after_enqueue_and_dequeue(self):
        """test length tracking on queue"""
        self.assertEqual(len(self.queue), 0)
        self.queue.enqueue(1)
        self.assertEqual(len(self.queue), 1)
        self.queue.enqueue(2)
        self.assertEqual(len(self.queue), 2)
        self.queue.dequeue()
        self.assertEqual(len(self.queue), 1)
        self.queue.dequeue()
        self.assertEqual(len(self.queue), 0)

    def test_single_item_dequeue_empties_queue(self):
        """test one item dequeue leaves empty queue"""
        only = object()
        self.queue.enqueue(only)
        self.assertIs(self.queue.dequeue(), only)
        self.assertTrue(self.queue.is_empty())
        with self.assertRaises(ValueError):
            self.queue.dequeue()


class TestNode(unittest.TestCase): # casper
    """test cases for node class"""

    def test_node_creation(self):
        """test node data and next"""
        node = Node(42)
        self.assertEqual(node.data, 42)
        self.assertIsNone(node.next)


class TestEnrollmentRecord(unittest.TestCase): # casper
    """test cases for enrollment record"""

    def test_enrollment_record_string_date(self):
        """test enrollment record with string date"""
        student = Student("STU00001", "1_Student")
        record = EnrollmentRecord(student, "2026-03-01")
        self.assertIs(record.student, student)
        self.assertEqual(record.enroll_date, "2026-03-01")

    def test_enrollment_record_date_object(self):
        """test enrollment record with date object"""
        student = Student("STU00002", "2_Student")
        enroll_date = date(2026, 3, 15)
        record = EnrollmentRecord(student, enroll_date)
        self.assertIs(record.student, student)
        self.assertEqual(record.enroll_date, enroll_date)


class TestCourseCapacityWaitlist(unittest.TestCase): # casper
    """test cases for course capacity and waitlist"""

    def setUp(self):
        """setting up test"""
        self.cap = 2
        self.course = Course("CSE9999", 3, self.cap)

    def test_enroll_to_capacity(self):
        """test enroll until roster hits capacity"""
        student1 = Student("STU00001", "1_Student")
        student2 = Student("STU00002", "2_Student")
        self.course.request_enroll(student1, "2026-01-10")
        self.course.request_enroll(student2, "2026-01-11")
        self.assertEqual(len(self.course.students), self.cap)

    def test_extra_student_goes_to_waitlist(self):
        """test student goes to waitlist when course is full"""
        student1 = Student("STU00001", "1_Student")
        student2 = Student("STU00002", "2_Student")
        student3 = Student("STU00003", "3_Student")
        self.course.request_enroll(student1, "2026-01-10")
        self.course.request_enroll(student2, "2026-01-11")
        self.course.request_enroll(student3, "2026-01-12")
        self.assertEqual(len(self.course.students), self.cap)
        self.assertEqual(len(self.course.waitlist), 1)

    def test_waitlist_fifo_on_drop(self):
        """test waitlist fifo when student drops"""
        student1 = Student("STU00001", "1_Student")
        student2 = Student("STU00002", "2_Student")
        student3 = Student("STU00003", "3_Student")
        student4 = Student("STU00004", "4_Student")
        self.course.request_enroll(student1, "2026-01-01")
        self.course.request_enroll(student2, "2026-01-02")
        self.course.request_enroll(student3, "2026-01-03")
        self.course.request_enroll(student4, "2026-01-04")
        self.assertEqual(len(self.course.students), 2)
        self.assertEqual(len(self.course.waitlist), 2)

        self.course.sort_enrolled("id", "insertion")
        replacement = date(2026, 4, 8)
        self.course.drop("STU00001", replacement)

        ids = [r.student.student_id for r in self.course.students]
        self.assertEqual(sorted(ids), ["STU00002", "STU00003"])
        self.assertEqual(len(self.course.waitlist), 1)

        self.course.sort_enrolled("id", "insertion")
        self.course.drop("STU00002", replacement)
        ids = [r.student.student_id for r in self.course.students]
        self.assertEqual(sorted(ids), ["STU00003", "STU00004"])
        self.assertTrue(self.course.waitlist.is_empty())

    def test_duplicate_enroll_ignored(self):
        """test duplicate enroll on roster is ignored"""
        student = Student("STU00001", "1_Student")
        self.course.request_enroll(student, "2026-01-01")
        self.course.request_enroll(student, "2026-02-01")
        self.assertEqual(len(self.course.students), 1)
        self.assertEqual(self.course.students[0].enroll_date, "2026-01-01")

    def test_promoted_student_replacement_date(self):
        """test waitlist student gets replacement enroll date"""
        student1 = Student("STU00010", "1_Student")
        student2 = Student("STU00011", "2_Student")
        student3 = Student("STU00012", "3_Student")
        self.course.request_enroll(student1, "2026-01-01")
        self.course.request_enroll(student2, "2026-01-02")
        self.course.request_enroll(student3, "2026-01-03")
        self.course.sort_enrolled("id", "selection")
        rep = date(2026, 5, 1)
        self.course.drop("STU00010", rep)
        promoted = None
        for r in self.course.students:
            if r.student is student3:
                promoted = r
                break
        self.assertIsNotNone(promoted)
        self.assertEqual(promoted.enroll_date, rep)


class TestCourseSorting(unittest.TestCase): # casper
    """test cases for sorting enrolled roster"""

    def setUp(self):
        """setting up test"""
        self.course = Course("CSE8888", 3, 10)
        self.student_a = Student("STU00003", "3_Student")
        self.student_b = Student("STU00001", "1_Student")
        self.student_c = Student("STU00002", "2_Student")
        self.course.request_enroll(self.student_a, "2026-03-03")
        self.course.request_enroll(self.student_b, "2026-03-01")
        self.course.request_enroll(self.student_c, "2026-03-02")

    def test_sort_by_name_insertion(self):
        """test sort roster by name insertion sort"""
        self.course.sort_enrolled("name", "insertion")
        names = [r.student.name for r in self.course.students]
        self.assertEqual(names, ["1_Student", "2_Student", "3_Student"])
        self.assertEqual(self.course.enrolled_sorted_by, "name")

    def test_sort_by_name_selection(self):
        """test sort roster by name selection sort"""
        self.course.sort_enrolled("name", "selection")
        names = [r.student.name for r in self.course.students]
        self.assertEqual(names, ["1_Student", "2_Student", "3_Student"])
        self.assertEqual(self.course.enrolled_sorted_by, "name")

    def test_sort_by_id_insertion(self):
        """test sort roster by id insertion sort"""
        self.course.sort_enrolled("id", "insertion")
        ids = [r.student.student_id for r in self.course.students]
        self.assertEqual(ids, ["STU00001", "STU00002", "STU00003"])
        self.assertEqual(self.course.enrolled_sorted_by, "id")

    def test_sort_by_id_selection(self):
        """test sort roster by id selection sort"""
        self.course.sort_enrolled("id", "selection")
        ids = [r.student.student_id for r in self.course.students]
        self.assertEqual(ids, ["STU00001", "STU00002", "STU00003"])
        self.assertEqual(self.course.enrolled_sorted_by, "id")

    def test_sort_by_date_insertion(self):
        """test sort roster by date insertion sort"""
        self.course.sort_enrolled("date", "insertion")
        dates = [r.enroll_date for r in self.course.students]
        self.assertEqual(dates, ["2026-03-01", "2026-03-02", "2026-03-03"])
        self.assertEqual(self.course.enrolled_sorted_by, "date")

    def test_sort_by_date_selection(self):
        """test sort roster by date selection sort"""
        self.course.sort_enrolled("date", "selection")
        dates = [r.enroll_date for r in self.course.students]
        self.assertEqual(dates, ["2026-03-01", "2026-03-02", "2026-03-03"])
        self.assertEqual(self.course.enrolled_sorted_by, "date")

    def test_sort_one_student_sets_sorted_key(self):
        """test sort with one student sets enrolled_sorted_by"""
        course = Course("CSE7777", 1, 5)
        course.request_enroll(Student("STU00001", "1_Student"), "2026-01-01")
        course.sort_enrolled("id", "selection")
        self.assertEqual(course.enrolled_sorted_by, "id")


class TestRecursiveBinarySearch(unittest.TestCase): # casper
    """test cases for recursive binary search"""

    def setUp(self):
        """setting up test"""
        self.records = [
            EnrollmentRecord(Student("STU00001", "1_Student"), "2026-01-01"),
            EnrollmentRecord(Student("STU00002", "2_Student"), "2026-01-02"),
            EnrollmentRecord(Student("STU00003", "3_Student"), "2026-01-03"),
            EnrollmentRecord(Student("STU00004", "4_Student"), "2026-01-04"),
        ]
        self.high = len(self.records) - 1

    def test_binary_search_first(self):
        """test binary search finds first id"""
        idx = recursive_binary_search(self.records, "STU00001", 0, self.high)
        self.assertEqual(idx, 0)

    def test_binary_search_middle(self):
        """test binary search finds middle id"""
        idx = recursive_binary_search(self.records, "STU00003", 0, self.high)
        self.assertEqual(idx, 2)

    def test_binary_search_last(self):
        """test binary search finds last id"""
        idx = recursive_binary_search(self.records, "STU00004", 0, self.high)
        self.assertEqual(idx, 3)

    def test_binary_search_not_found(self):
        """test binary search returns negative one if missing"""
        idx = recursive_binary_search(self.records, "STU00999", 0, self.high)
        self.assertEqual(idx, -1)

    def test_binary_search_empty_range(self):
        """test binary search with invalid range"""
        idx = recursive_binary_search(self.records, "STU00001", 1, 0)
        self.assertEqual(idx, -1)


class TestCourseDropSortedById(unittest.TestCase): # casper
    """test cases for drop when roster sorted by id"""

    def test_drop_without_sort_by_id_raises(self):
        """test drop raises if roster not sorted by id"""
        course = Course("CSE6666", 3, 5)
        course.request_enroll(Student("STU00002", "2_Student"), "2026-01-01")
        course.request_enroll(Student("STU00001", "1_Student"), "2026-01-02")
        course.sort_enrolled("name", "insertion")
        with self.assertRaises(ValueError):
            course.drop("STU00001")

    def test_drop_after_sort_by_id(self):
        """test drop works after sort by id"""
        course = Course("CSE6666", 3, 5)
        course.request_enroll(Student("STU00002", "2_Student"), "2026-01-01")
        course.request_enroll(Student("STU00001", "1_Student"), "2026-01-02")
        course.sort_enrolled("id", "insertion")
        course.drop("STU00002")
        ids = [r.student.student_id for r in course.students]
        self.assertEqual(ids, ["STU00001"])
        self.assertEqual(course.enrolled_sorted_by, "id")

    def test_drop_missing_student_raises(self):
        """test drop raises for id not on roster"""
        course = Course("CSE5555", 3, 5)
        course.request_enroll(Student("STU00001", "1_Student"), "2026-01-01")
        course.sort_enrolled("id", "selection")
        with self.assertRaises(ValueError):
            course.drop("STU99999")


if __name__ == '__main__': # casper
    unittest.main()
