from django.db import IntegrityError
from django.test import TestCase
from django.contrib.auth.models import Group

from usuarios.models import User
from academico.models import (
    AcademicYear,
    Attendance,
    Course,
    Enrollment,
    Grade,
    LessonPlan,
    Subject,
)


class AcademicYearModelTests(TestCase):
    '''Testa o modelo AcademicYear.'''

    def test_criar_ano_letivo(self):
        '''AcademicYear e criado com os campos corretos.'''
        year = AcademicYear.objects.create(
            year=2025,
            start_date='2025-01-01',
            end_date='2025-12-31',
            is_active=True,
        )
        self.assertEqual(year.year, 2025)
        self.assertTrue(year.is_active)

    def test_get_active_retorna_ano_ativo(self):
        '''get_active() retorna o ano letivo ativo.'''
        year = AcademicYear.objects.create(
            year=2025,
            start_date='2025-01-01',
            end_date='2025-12-31',
            is_active=True,
        )
        active = AcademicYear.get_active()
        self.assertEqual(active, year)

    def test_get_active_retorna_none_sem_ano_ativo(self):
        '''get_active() retorna None quando nenhum ano esta ativo.'''
        AcademicYear.objects.create(
            year=2024,
            start_date='2024-01-01',
            end_date='2024-12-31',
            is_active=False,
        )
        self.assertIsNone(AcademicYear.get_active())

    def test_str_inclui_active(self):
        '''__str__ indica quando o ano esta ativo.'''
        year = AcademicYear.objects.create(
            year=2025,
            start_date='2025-01-01',
            end_date='2025-12-31',
            is_active=True,
        )
        self.assertIn('Active', str(year))


class EnrollmentModelTests(TestCase):
    '''Testa o modelo Enrollment.'''

    def setUp(self):
        students_group = Group.objects.create(name='Students')

        self.student = User.objects.create_user(
            email='aluno@exemplo.com',
            password='senha123',
        )
        self.student.groups.add(students_group)

        self.year = AcademicYear.objects.create(
            year=2025,
            start_date='2025-01-01',
            end_date='2025-12-31',
            is_active=True,
        )
        self.course = Course.objects.create(
            name='Turma 10A',
            shift='morning',
            academic_year=self.year,
        )

    def test_criar_matricula(self):
        '''Enrollment e criada corretamente.'''
        enrollment = Enrollment.objects.create(
            student=self.student,
            course=self.course,
            is_active=True,
        )
        self.assertEqual(enrollment.student, self.student)
        self.assertEqual(enrollment.course, self.course)
        self.assertTrue(enrollment.is_active)

    def test_unique_together_aluno_turma(self):
        '''O par (student, course) deve ser unico.'''
        Enrollment.objects.create(student=self.student, course=self.course)
        with self.assertRaises(IntegrityError):
            Enrollment.objects.create(student=self.student, course=self.course)


class GradeModelTests(TestCase):
    '''Testa o modelo Grade.'''

    def setUp(self):
        teachers_group = Group.objects.create(name='Teachers')
        students_group = Group.objects.create(name='Students')

        self.teacher = User.objects.create_user(
            email='professor@exemplo.com',
            password='senha123',
        )
        self.teacher.groups.add(teachers_group)

        self.student = User.objects.create_user(
            email='aluno@exemplo.com',
            password='senha123',
        )
        self.student.groups.add(students_group)

        self.year = AcademicYear.objects.create(
            year=2025,
            start_date='2025-01-01',
            end_date='2025-12-31',
            is_active=True,
        )
        self.course = Course.objects.create(
            name='Turma 10A',
            shift='morning',
            academic_year=self.year,
        )
        self.subject = Subject.objects.create(
            name='Matematica',
            course=self.course,
            teacher=self.teacher,
        )

    def test_criar_nota(self):
        '''Grade e criada com os valores corretos.'''
        grade = Grade.objects.create(
            student=self.student,
            subject=self.subject,
            academic_year=self.year,
            value='8.50',
            term=1,
            grade_type='exam',
        )
        self.assertEqual(float(grade.value), 8.50)
        self.assertEqual(grade.term, 1)
        self.assertEqual(grade.grade_type, 'exam')

    def test_unique_together_nota(self):
        '''Combinacao (student, subject, term, grade_type) deve ser unica.'''
        Grade.objects.create(
            student=self.student,
            subject=self.subject,
            academic_year=self.year,
            value='7.00',
            term=1,
            grade_type='exam',
        )
        with self.assertRaises(IntegrityError):
            Grade.objects.create(
                student=self.student,
                subject=self.subject,
                academic_year=self.year,
                value='6.00',
                term=1,
                grade_type='exam',
            )

    def test_str_nota(self):
        '''__str__ da Grade contem email do aluno e nome da disciplina.'''
        grade = Grade.objects.create(
            student=self.student,
            subject=self.subject,
            academic_year=self.year,
            value='9.00',
            term=2,
            grade_type='assignment',
        )
        self.assertIn(self.student.email, str(grade))
        self.assertIn('Matematica', str(grade))
