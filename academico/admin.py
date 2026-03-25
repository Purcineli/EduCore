from django.contrib import admin

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


@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ('year', 'start_date', 'end_date', 'is_active')
    list_filter = ('is_active',)
    readonly_fields = ('created_at', 'updated_at', 'historical')


class SubjectInline(admin.TabularInline):
    model = Subject
    extra = 1
    fields = ('name', 'teacher', 'workload_hours')
    show_change_link = True


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'academic_year', 'shift', 'coordinator')
    list_filter = ('shift', 'academic_year')
    search_fields = ('name',)
    readonly_fields = ('created_at', 'updated_at', 'historical')
    inlines = [SubjectInline]


class ScheduleInline(admin.TabularInline):
    model = Schedule
    extra = 1
    fields = ('weekday', 'start_time', 'end_time')


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'course', 'teacher', 'workload_hours')
    list_filter = ('course__academic_year',)
    search_fields = ('name', 'teacher__email')
    readonly_fields = ('created_at', 'updated_at', 'historical')
    inlines = [ScheduleInline]


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('subject', 'weekday', 'start_time', 'end_time')
    list_filter = ('weekday',)
    readonly_fields = ('created_at', 'updated_at', 'historical')


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'enrolled_at', 'is_active')
    list_filter = ('is_active', 'course__academic_year')
    search_fields = ('student__email',)
    readonly_fields = ('created_at', 'updated_at', 'enrolled_at', 'historical')


@admin.register(LessonPlan)
class LessonPlanAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'teacher', 'lesson_date')
    list_filter = ('lesson_date', 'subject', 'teacher')
    search_fields = ('title', 'content')
    readonly_fields = ('created_at', 'updated_at', 'historical')


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'lesson_plan', 'is_present')
    list_filter = ('is_present', 'lesson_plan__lesson_date')
    search_fields = ('student__email',)
    readonly_fields = ('created_at', 'updated_at', 'historical')


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'value', 'term', 'grade_type')
    list_filter = ('term', 'subject', 'grade_type', 'academic_year')
    search_fields = ('student__email', 'subject__name')
    readonly_fields = ('created_at', 'updated_at', 'historical')
