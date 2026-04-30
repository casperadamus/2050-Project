import unittest
from datetime import date

from main import Course, EnrollmentRecord, HashMap, Student


class CollisionKey: # casper
    """helper key class for hashmap collision tests"""

    def __init__(self, label):
        self.label = label

    def __hash__(self):
        return 7

    def __eq__(self, other):
        return isinstance(other, CollisionKey) and self.label == other.label


class TestHashMapMilestone3(unittest.TestCase): # casper
    """test cases for HashMap milestone 3 requirements"""

    def test_collision_handling(self):
        """test collision handling in hashmap buckets"""
        hmap = HashMap(capacity=8)
        k1 = CollisionKey("k1")
        k2 = CollisionKey("k2")
        k3 = CollisionKey("k3")

        hmap.put(k1, "alpha")
        hmap.put(k2, "beta")
        hmap.put(k3, "gamma")

        self.assertEqual(len(hmap), 3)
        self.assertEqual(hmap.get(k1), "alpha")
        self.assertEqual(hmap.get(k2), "beta")
        self.assertEqual(hmap.get(k3), "gamma")

        hmap.remove(k2)
        self.assertEqual(len(hmap), 2)
        self.assertNotIn(k2, hmap)
        with self.assertRaises(KeyError):
            hmap.get(k2)
        self.assertEqual(hmap.get(k1), "alpha")
        self.assertEqual(hmap.get(k3), "gamma")

    def test_rehashing_preserves_values(self):
        """test hashmap rehashing keeps inserted key-value pairs"""
        hmap = HashMap(capacity=2)
        original_capacity = hmap._capacity

        for i in range(10):
            hmap.put(f"key{i}", i)

        self.assertGreater(hmap._capacity, original_capacity)
        self.assertEqual(len(hmap), 10)
        for i in range(10):
            self.assertEqual(hmap.get(f"key{i}"), i)


class TestEnrollmentMilestone3(unittest.TestCase): # casper
    """test cases for enrollment prerequisite checks"""

    def test_request_enroll_rejects_missing_prereq(self):
        """test enrollment fails if prereqs are missing"""
        cse2050 = Course("CSE2050", 4, 5)
        student = Student("STU1001", "Student_1")

        with self.assertRaises(ValueError):
            cse2050.request_enroll(student)

    def test_request_enroll_accepts_when_prereq_met(self):
        """test enrollment succeeds when prereqs are met"""
        cse2050 = Course("CSE2050", 4, 5)
        student = Student("STU1002", "Student_2", courses={"CSE1010": "A"})

        cse2050.request_enroll(student)

        self.assertEqual(len(cse2050.students), 1)
        self.assertEqual(cse2050.students[0].student.student_id, "STU1002")


class TestSortingMilestone3(unittest.TestCase): # casper
    """test cases for merge and quick sort roster ordering"""

    def setUp(self):
        """setting up reusable enrollment records"""
        self.records = [
            EnrollmentRecord(Student("STU1003", "Student_3"), date(2026, 4, 10)),
            EnrollmentRecord(Student("STU1001", "Student_1"), date(2026, 3, 1)),
            EnrollmentRecord(Student("STU1002", "Student_2"), date(2026, 1, 20)),
        ]

    def _make_course_with_records(self):
        course = Course("CSE1010", 3, 20)
        course.students = list(self.records)
        return course

    def test_merge_sort_roster_by_id_name_date(self):
        """test merge sort by id, name, and date"""
        course = self._make_course_with_records()
        course.sort_enrolled("id", "merge")
        self.assertEqual(
            [r.student.student_id for r in course.students],
            ["STU1001", "STU1002", "STU1003"],
        )

        course = self._make_course_with_records()
        course.sort_enrolled("name", "merge")
        self.assertEqual(
            [r.student.name for r in course.students],
            ["Student_1", "Student_2", "Student_3"],
        )

        course = self._make_course_with_records()
        course.sort_enrolled("date", "merge")
        self.assertEqual(
            [r.enroll_date for r in course.students],
            [date(2026, 1, 20), date(2026, 3, 1), date(2026, 4, 10)],
        )

    def test_quick_sort_roster_by_id_name_date(self):
        """test quick sort by id, name, and date"""
        course = self._make_course_with_records()
        course.sort_enrolled("id", "quick")
        self.assertEqual(
            [r.student.student_id for r in course.students],
            ["STU1001", "STU1002", "STU1003"],
        )

        course = self._make_course_with_records()
        course.sort_enrolled("name", "quick")
        self.assertEqual(
            [r.student.name for r in course.students],
            ["Student_1", "Student_2", "Student_3"],
        )

        course = self._make_course_with_records()
        course.sort_enrolled("date", "quick")
        self.assertEqual(
            [r.enroll_date for r in course.students],
            [date(2026, 1, 20), date(2026, 3, 1), date(2026, 4, 10)],
        )


if __name__ == "__main__":
    unittest.main()
