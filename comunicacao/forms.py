from django import forms

from .models import Message


class MessageForm(forms.ModelForm):
    '''Form to compose and send a direct message.'''

    class Meta:
        model = Message
        fields = ['receiver', 'subject', 'body']
        widgets = {
            'receiver': forms.Select(attrs={
                'class': (
                    'w-full rounded-md border border-slate-300 shadow-sm '
                    'focus:border-indigo-500 focus:ring-indigo-500 px-3 py-2'
                ),
            }),
            'subject': forms.TextInput(attrs={
                'class': (
                    'w-full rounded-md border border-slate-300 shadow-sm '
                    'focus:border-indigo-500 focus:ring-indigo-500 px-3 py-2'
                ),
                'placeholder': 'Message subject',
            }),
            'body': forms.Textarea(attrs={
                'class': (
                    'w-full rounded-md border border-slate-300 shadow-sm '
                    'focus:border-indigo-500 focus:ring-indigo-500 px-3 py-2'
                ),
                'rows': 8,
                'placeholder': 'Write your message here…',
            }),
        }
