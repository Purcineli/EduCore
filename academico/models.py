from django.conf import settings
from django.db import models

from core.models import BaseModel


class AcademicYear(BaseModel):
    year = models.IntegerField(unique=True, help_text='Academic year (e.g., 2025)')
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=False)

    class Meta:
        ordering = ['-year']
        verbose_name = 'academic year'
        verbose_name_plural = 'academic years'

    def __str__(self):
        suffix = ' (Active)' if self.is_active else ''
        return f'{self.year}{suffix}'

    @classmethod
    def get_active(cls):
        '''Return the currently active AcademicYear, or None.'''
        return cls.objects.filter(is_active=True).first()


class Course(BaseModel):
    SHIFT_CHOICES = [
        ('morning', 'Morning'),
        ('afternoon', 'Afternoon'),
        ('evening', 'Evening'),
    ]

    name = models.CharField(max_length=100, help_text='E.g., "Grade 10A"')
    shift = models.CharField(max_length=20, choices=SHIFT_CHOICES)
    academic_year = models.ForeignKey(
        AcademicYear,
        on_delete=models.CASCADE,
        related_name='courses',
    )
    coordinator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='coordinated_courses',
        limit_choices_to={'groups__name': 'Coordinators'},
        help_text='Course coordinator',
    )

    class Meta:
        ordering = ['academic_year', 'name']
        unique_together = ('name', 'academic_year')
        verbose_name = 'course'
        verbose_name_plural = 'courses'

    def __str__(self):
        return f'{self.name} ({self.academic_year.year}) - {self.get_shift_display()}'


class Subject(BaseModel):
    name = models.CharField(max_length=100, help_text='E.g., "Mathematics"')
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='subjects',
    )
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='taught_subjects',
        limit_choices_to={'groups__name': 'Teachers'},
        help_text='Teacher responsible for this subject',
    )
    workload_hours = models.IntegerField(default=40, help_text='Total workload in hours')

    class Meta:
        ordering = ['course', 'name']
        unique_together = ('name', 'course')
        verbose_name = 'subject'
        verbose_name_plural = 'subjects'

    def __str__(self):
        return f'{self.name} - {self.course.name}'


class Schedule(BaseModel):
    WEEKDAY_CHOICES = [
        ('mon', 'Monday'),
        ('tue', 'Tuesday'),
        ('wed', 'Wednesday'),
        ('thu', 'Thursday'),
        ('fri', 'Friday'),
    ]

    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='schedules',
    )
    weekday = models.CharField(max_length=3, choices=WEEKDAY_CHOICES)
    start_time = models.TimeField(help_text='e.g., 08:00')
    end_time = models.TimeField(help_text='e.g., 09:00')

    class Meta:
        ordering = ['weekday', 'start_time']
        unique_together = ('subject', 'weekday', 'start_time')
        verbose_name = 'schedule'
        verbose_name_plural = 'schedules'

    def __str__(self):
        return (
            f'{self.subject.name} - {self.get_weekday_display()} '
            f'{self.start_time:%H:%M}-{self.end_time:%H:%M}'
        )


class Enrollment(BaseModel):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='enrollments',
        limit_choices_to={'groups__name': 'Students'},
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='enrollments',
    )
    enrolled_at = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('student', 'course')
        ordering = ['-enrolled_at']
        verbose_name = 'enrollment'
        verbose_name_plural = 'enrollments'

    def __str__(self):
        return f'{self.student.email} \u2192 {self.course.name}'


class LessonPlan(BaseModel):
    title = models.CharField(max_length=200, help_text='Lesson title')
    content = models.TextField(help_text='Lesson content/description')
    lesson_date = models.DateField()
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='lesson_plans',
        limit_choices_to={'groups__name': 'Teachers'},
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='lesson_plans',
    )

    class Meta:
        ordering = ['-lesson_date']
        verbose_name = 'lesson plan'
        verbose_name_plural = 'lesson plans'

    def __str__(self):
        return f'{self.title} ({self.lesson_date})'


class Attendance(BaseModel):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='attendances',
        limit_choices_to={'groups__name': 'Students'},
    )
    lesson_plan = models.ForeignKey(
        LessonPlan,
        on_delete=models.CASCADE,
        related_name='attendances',
    )
    is_present = models.BooleanField(default=False)

    class Meta:
        unique_together = ('student', 'lesson_plan')
        verbose_name = 'attendance'
        verbose_name_plural = 'attendances'

    def __str__(self):
        status = 'Present' if self.is_present else 'Absent'
        return f'{self.student.email} - {self.lesson_plan.title}: {status}'


class Grade(BaseModel):
    TERM_CHOICES = [
        (1, 'First Term'),
        (2, 'Second Term'),
        (3, 'Third Term'),
        (4, 'Fourth Term'),
    ]

    GRADE_TYPE_CHOICES = [
        ('exam', 'Exam'),
        ('assignment', 'Assignment'),
        ('project', 'Project'),
        ('participation', 'Participation'),
    ]

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='grades',
        limit_choices_to={'groups__name': 'Students'},
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='grades',
    )
    academic_year = models.ForeignKey(
        AcademicYear,
        on_delete=models.CASCADE,
        related_name='grades',
    )
    value = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text='Grade value (0-10)',
    )
    term = models.IntegerField(choices=TERM_CHOICES)
    grade_type = models.CharField(
        max_length=20,
        choices=GRADE_TYPE_CHOICES,
        default='exam',
    )

    class Meta:
        unique_together = ('student', 'subject', 'term', 'grade_type')
        ordering = ['-term', 'subject__name']
        verbose_name = 'grade'
        verbose_name_plural = 'grades'

    def __str__(self):
        return (
            f'{self.student.email} - {self.subject.name}: {self.value} '
            f'(Term {self.term}, {self.get_grade_type_display()})'
        )
