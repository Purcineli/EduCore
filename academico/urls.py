from django.urls import path

from .views import (
    AttendanceCreateView,
    CourseListView,
    DashboardView,
    GradeCreateView,
    ReportCardView,
    ScheduleView,
)

app_name = 'academico'

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('courses/', CourseListView.as_view(), name='course-list'),
    path('grades/create/', GradeCreateView.as_view(), name='grade-create'),
    path('attendance/', AttendanceCreateView.as_view(), name='attendance-create'),
    path('report-card/', ReportCardView.as_view(), name='report-card'),
    path('schedule/', ScheduleView.as_view(), name='schedule'),
]
