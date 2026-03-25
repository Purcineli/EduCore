from django import forms

from .models import Attendance, Grade


FIELD_CLASS = (
    'w-full rounded-md border border-slate-300 shadow-sm '
    'focus:border-indigo-500 focus:ring-indigo-500 px-3 py-2'
)


class GradeForm(forms.ModelForm):
    '''Form to create/edit a Grade record.'''

    class Meta:
        model = Grade
        fields = ['student', 'subject', 'value', 'term', 'grade_type', 'academic_year']
        widgets = {
            'student': forms.Select(attrs={'class': FIELD_CLASS}),
            'subject': forms.Select(attrs={'class': FIELD_CLASS}),
            'value': forms.NumberInput(attrs={
                'class': FIELD_CLASS,
                'step': '0.01',
                'min': '0',
                'max': '10',
            }),
            'term': forms.Select(attrs={'class': FIELD_CLASS}),
            'grade_type': forms.Select(attrs={'class': FIELD_CLASS}),
            'academic_year': forms.Select(attrs={'class': FIELD_CLASS}),
        }


class AttendanceForm(forms.ModelForm):
    '''Form to record attendance for a single lesson.'''

    class Meta:
        model = Attendance
        fields = ['student', 'is_present']
        widgets = {
            'student': forms.Select(attrs={'class': FIELD_CLASS}),
            'is_present': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 rounded border-slate-300 text-indigo-600 focus:ring-indigo-500'
            }),
        }
