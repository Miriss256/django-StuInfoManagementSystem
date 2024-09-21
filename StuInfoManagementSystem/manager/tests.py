from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import manager, teacher, student
from datetime import date

class ManagerModelTest(TestCase):

    def test_create_manager(self):
        manager_obj = manager.objects.create(name='admin', password='password123')
        self.assertEqual(manager_obj.name, 'admin')
        self.assertEqual(manager_obj.password, 'password123')


class TeacherModelTest(TestCase):

    def setUp(self):
        self.teacher_data = {
            'name': 'Mr. Smith',
            'age': 45,
            'gender': 1,
            'create_time': date(2023, 1, 1),
            'salary': 5000.00,
            'password': 'teacherpass',
            'department': 2,
            'faculty': 'Science',
            'level': 2,
            'phone_number': '13800138000',
        }

    def test_create_teacher(self):
        teacher_obj = teacher(**self.teacher_data)
        teacher_obj.save()
        self.assertEqual(teacher_obj.name, 'Mr. Smith')
        self.assertEqual(teacher_obj.department, 2)

    def test_teacher_gender_validation(self):
        invalid_data = self.teacher_data.copy()
        invalid_data['gender'] = 3  # Invalid choice
        with self.assertRaises(ValidationError):
            teacher(**invalid_data).full_clean()

    def test_teacher_phone_number_validation(self):
        invalid_data = self.teacher_data.copy()
        invalid_data['phone_number'] = '12345678901'  # Invalid mobile number format
        with self.assertRaises(ValidationError):
            teacher(**invalid_data).full_clean()


class StudentModelTest(TestCase):

    def setUp(self):
        self.student_data = {
            'name': 'John Doe',
            'age': 20,
            'gender': 1,
            'password': 'studentpass',
            'grade': 2,
            'classes': '2A',
            'major': 'Computer Science',
            'studentid': 10001,
            'faculty': 'Engineering',
            'address': '123 Main St',
            'phone_number': '13800138001',
        }

    def test_create_student(self):
        student_obj = student(**self.student_data)
        student_obj.save()
        self.assertEqual(student_obj.name, 'John Doe')
        self.assertEqual(student_obj.major, 'Computer Science')

    def test_student_phone_number_validation(self):
        invalid_data = self.student_data.copy()
        invalid_data['phone_number'] = '12345678901'  # Invalid mobile number format
        with self.assertRaises(ValidationError):
            student(**invalid_data).full_clean()

