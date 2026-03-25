from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Avg
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, FormView, ListView, TemplateView

from usuarios.models import Guardian

from .forms import GradeForm
from .models import (
    AcademicYear,
    Attendance,
    Course,
    Enrollment,
    Grade,
    LessonPlan,
    Schedule,
    Subject,
)


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'academico/dashboard.html'
    login_url = 'usuarios:login'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user

        is_coordinator = user.groups.filter(name='Coordinators').exists()
        is_teacher = user.groups.filter(name='Teachers').exists()
        is_student = user.groups.filter(name='Students').exists()
        is_parent = user.groups.filter(name='Parents').exists()

        ctx.update({
            'is_coordinator': is_coordinator,
            'is_teacher': is_teacher,
            'is_student': is_student,
            'is_parent': is_parent,
        })

        active_year = AcademicYear.get_active()
        ctx['active_year'] = active_year
        active_year_value = active_year.year if active_year else timezone.now().year

        # ===== COORDINATOR =====
        if is_coordinator:
            ctx['total_courses'] = Course.objects.filter(
                academic_year=active_year
            ).count()
            ctx['total_enrollments'] = Enrollment.objects.filter(
                course__academic_year=active_year
            ).count()
            ctx['total_students'] = (
                Enrollment.objects
                .filter(course__academic_year=active_year)
                .values('student')
                .distinct()
                .count()
            )
            ctx['courses'] = (
                Course.objects
                .filter(academic_year=active_year)
                .select_related('coordinator', 'academic_year')
                .order_by('name')
            )

        # ===== TEACHER =====
        elif is_teacher:
            ctx['subjects'] = (
                Subject.objects
                .filter(teacher=user)
                .select_related('course')
            )
            ctx['lesson_plans'] = (
                LessonPlan.objects
                .filter(teacher=user, lesson_date__year=active_year_value)
                .select_related('subject')
                .order_by('-lesson_date')[:10]
            )
            ctx['absent_today'] = (
                Attendance.objects
                .filter(
                    lesson_plan__teacher=user,
                    is_present=False,
                    lesson_plan__lesson_date=timezone.now().date(),
                )
                .select_related('student', 'lesson_plan')
            )

        # ===== STUDENT =====
        elif is_student:
            ctx['enrollments'] = (
                Enrollment.objects
                .filter(student=user, is_active=True)
                .select_related('course__academic_year')
            )
            ctx['grades'] = (
                Grade.objects
                .filter(student=user, academic_year=active_year)
                .select_related('subject')
                .order_by('subject__name')
            )
            student_attendance = Attendance.objects.filter(
                student=user,
                lesson_plan__lesson_date__year=active_year_value,
            )
            total_lessons = student_attendance.count()
            if total_lessons > 0:
                present_count = student_attendance.filter(is_present=True).count()
                ctx['attendance_percentage'] = round(
                    (present_count / total_lessons) * 100, 1
                )
            else:
                ctx['attendance_percentage'] = 0

        # ===== PARENT =====
        elif is_parent:
            guardianships = (
                Guardian.objects
                .filter(parent=user)
                .select_related('student')
            )
            children_data = []
            for guardianship in guardianships:
                child = guardianship.student
                child_grades = (
                    Grade.objects
                    .filter(student=child, academic_year=active_year)
                    .values('subject__name')
                    .annotate(avg_grade=Avg('value'))
                )
                child_attendance = Attendance.objects.filter(
                    student=child,
                    lesson_plan__lesson_date__year=active_year_value,
                )
                total_child_lessons = child_attendance.count()
                present_child = child_attendance.filter(is_present=True).count()
                attendance_pct = (
                    round((present_child / total_child_lessons) * 100, 1)
                    if total_child_lessons > 0 else 0
                )
                children_data.append({
                    'student': child,
                    'relationship': guardianship.get_relationship_type_display(),
                    'grades': child_grades,
                    'attendance_percentage': attendance_pct,
                })
            ctx['children_data'] = children_data

        return ctx


# ---------------------------------------------------------------------------
# Course List
# ---------------------------------------------------------------------------

class CourseListView(LoginRequiredMixin, ListView):
    '''List all courses for the active academic year. Accessible to any logged-in user.'''

    model = Course
    template_name = 'academico/course_list.html'
    context_object_name = 'courses'
    paginate_by = 20
    login_url = 'usuarios:login'

    def get_queryset(self):
        active_year = AcademicYear.get_active()
        if not active_year:
            return Course.objects.none()
        return (
            Course.objects
            .filter(academic_year=active_year)
            .select_related('coordinator', 'academic_year')
            .prefetch_related('subjects')
        )


# ---------------------------------------------------------------------------
# Grade Create
# ---------------------------------------------------------------------------

class GradeCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    '''Create a new Grade record. Restricted to Teachers.'''

    model = Grade
    form_class = GradeForm
    template_name = 'academico/grade_form.html'
    success_url = reverse_lazy('academico:grade-create')
    login_url = 'usuarios:login'

    def test_func(self):
        return self.request.user.groups.filter(name='Teachers').exists()

    def get_form(self, form_class=None):
        '''Narrow subjects/students dropdowns to the requesting teacher.'''
        form = super().get_form(form_class)

        teacher = self.request.user

        # Only subjects taught by this teacher
        form.fields['subject'].queryset = (
            Subject.objects
            .filter(teacher=teacher)
            .select_related('course')
        )

        # Only students enrolled in courses where this teacher has at least one subject
        teacher_courses = Course.objects.filter(subjects__teacher=teacher)
        Student = settings.AUTH_USER_MODEL  # string reference — use get_user_model
        from django.contrib.auth import get_user_model
        UserModel = get_user_model()
        student_pks = (
            Enrollment.objects
            .filter(course__in=teacher_courses, is_active=True)
            .values_list('student', flat=True)
        )
        form.fields['student'].queryset = (
            UserModel.objects.filter(pk__in=student_pks)
        )

        return form

    def form_valid(self, form):
        from django.contrib import messages
        messages.success(self.request, 'Nota registrada com sucesso.')
        return super().form_valid(form)


# ---------------------------------------------------------------------------
# Attendance Batch Create
# ---------------------------------------------------------------------------

class AttendanceCreateView(LoginRequiredMixin, UserPassesTestMixin, FormView):
    '''Record attendance for a lesson (batch). Restricted to Teachers.'''

    template_name = 'academico/attendance_form.html'
    success_url = reverse_lazy('academico:attendance-create')
    login_url = 'usuarios:login'

    # FormView requires a form_class; we handle the form manually via get/post,
    # so we supply a trivial form that is never rendered.
    from django import forms as _forms

    class _EmptyForm(_forms.Form):
        pass

    form_class = _EmptyForm

    def test_func(self):
        return self.request.user.groups.filter(name='Teachers').exists()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx['lesson_plans'] = (
            LessonPlan.objects
            .filter(teacher=self.request.user)
            .select_related('subject')
            .order_by('-lesson_date')[:20]
        )

        lesson_id = self.request.GET.get('lesson_id')
        if lesson_id:
            lesson_plan = get_object_or_404(
                LessonPlan, pk=lesson_id, teacher=self.request.user
            )
            ctx['selected_lesson'] = lesson_plan

            # All active students enrolled in courses that contain the lesson's subject
            ctx['enrollments'] = (
                Enrollment.objects
                .filter(
                    course__subjects=lesson_plan.subject,
                    is_active=True,
                )
                .select_related('student')
            )

        return ctx

    def post(self, request, *args, **kwargs):
        lesson_id = request.POST.get('lesson_id')

        if not lesson_id:
            return redirect(self.success_url)

        lesson_plan = get_object_or_404(
            LessonPlan, pk=lesson_id, teacher=request.user
        )

        enrollments = Enrollment.objects.filter(
            course__subjects=lesson_plan.subject,
            is_active=True,
        )

        for enrollment in enrollments:
            student_key = f'student_{enrollment.student.id}'
            is_present = student_key in request.POST

            attendance, created = Attendance.objects.get_or_create(
                student=enrollment.student,
                lesson_plan=lesson_plan,
                defaults={'is_present': is_present},
            )

            if not created and attendance.is_present != is_present:
                attendance.is_present = is_present
                attendance.save(update_fields=['is_present', 'updated_at'])

        from django.contrib import messages
        messages.success(request, 'Presença registrada com sucesso.')
        return redirect(self.success_url)


# ---------------------------------------------------------------------------
# Report Card (Boletim)
# ---------------------------------------------------------------------------

class ReportCardView(LoginRequiredMixin, TemplateView):
    '''Exibe o boletim consolidado de um aluno ou filho (se responsavel).'''

    template_name = 'academico/report_card.html'
    login_url = 'usuarios:login'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user

        student_id = self.request.GET.get('student_id')

        if student_id:
            if user.groups.filter(name='Parents').exists():
                guardianship = Guardian.objects.filter(
                    parent=user,
                    student_id=student_id,
                ).first()
                if not guardianship:
                    ctx['error'] = 'Acesso nao autorizado.'
                    return ctx
                student = guardianship.student
            else:
                ctx['error'] = 'Apenas responsaveis podem visualizar o boletim de outros alunos.'
                return ctx
        else:
            if user.groups.filter(name='Students').exists():
                student = user
            else:
                ctx['error'] = 'Apenas alunos podem visualizar boletins.'
                return ctx

        active_year = AcademicYear.get_active()
        if not active_year:
            ctx['error'] = 'Nenhum ano letivo ativo encontrado.'
            return ctx

        grades = (
            Grade.objects
            .filter(student=student, academic_year=active_year)
            .select_related('subject')
            .order_by('subject__name', 'term')
        )

        # {subject_name: {term_int: [grade, ...]}}
        report_data = {}
        for grade in grades:
            subj = grade.subject.name
            if subj not in report_data:
                report_data[subj] = {}
            if grade.term not in report_data[subj]:
                report_data[subj][grade.term] = []
            report_data[subj][grade.term].append(grade)

        subject_summary = {}
        for subj, terms_data in report_data.items():
            all_grades = [g for term_grades in terms_data.values() for g in term_grades]
            avg = sum(float(g.value) for g in all_grades) / len(all_grades) if all_grades else 0
            avg = round(avg, 2)
            if avg >= 7:
                status = 'Aprovado'
            elif avg >= 5:
                status = 'Recuperacao'
            else:
                status = 'Reprovado'
            subject_summary[subj] = {'average': avg, 'status': status}

        all_attendances = Attendance.objects.filter(
            student=student,
            lesson_plan__subject__course__academic_year=active_year,
        )
        total_lessons = all_attendances.count()
        if total_lessons > 0:
            present_count = all_attendances.filter(is_present=True).count()
            attendance_percentage = round((present_count / total_lessons) * 100, 1)
        else:
            attendance_percentage = 0

        ctx.update({
            'student': student,
            'active_year': active_year,
            'report_data': report_data,
            'subject_summary': subject_summary,
            'attendance_percentage': attendance_percentage,
            'total_lessons': total_lessons,
        })
        return ctx


# ---------------------------------------------------------------------------
# Weekly Schedule (Grade Horaria)
# ---------------------------------------------------------------------------

class ScheduleView(LoginRequiredMixin, TemplateView):
    '''Exibe a grade horaria semanal do aluno ou professor.'''

    template_name = 'academico/schedule.html'
    login_url = 'usuarios:login'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user

        weekday_keys = ['mon', 'tue', 'wed', 'thu', 'fri']
        weekday_labels = ['Segunda', 'Terca', 'Quarta', 'Quinta', 'Sexta']

        if user.groups.filter(name='Students').exists():
            courses = Course.objects.filter(
                enrollments__student=user,
                enrollments__is_active=True,
            )
            schedules = (
                Schedule.objects
                .filter(subject__course__in=courses)
                .select_related('subject', 'subject__teacher', 'subject__course')
                .order_by('weekday', 'start_time')
            )
        elif user.groups.filter(name='Teachers').exists():
            schedules = (
                Schedule.objects
                .filter(subject__teacher=user)
                .select_related('subject', 'subject__course')
                .order_by('weekday', 'start_time')
            )
        else:
            schedules = Schedule.objects.none()

        schedule_data = {day: [] for day in weekday_keys}
        for schedule in schedules:
            schedule_data[schedule.weekday].append(schedule)

        ctx.update({
            'weekdays': list(zip(weekday_labels, weekday_keys)),
            'schedule_data': schedule_data,
        })
        return ctx
