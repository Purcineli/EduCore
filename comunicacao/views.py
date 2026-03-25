from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView

from .forms import MessageForm
from .models import Message, NoticeBoard


class NoticeBoardListView(LoginRequiredMixin, ListView):
    '''List published notices filtered by the current user's groups.'''

    model = NoticeBoard
    template_name = 'comunicacao/noticeboard_list.html'
    context_object_name = 'notices'
    paginate_by = 20

    def get_queryset(self):
        user = self.request.user
        user_groups = user.groups.all()
        return (
            NoticeBoard.objects.filter(is_published=True)
            .filter(
                Q(target_groups__isnull=True) | Q(target_groups__in=user_groups)
            )
            .distinct()
            .select_related('author')
            .prefetch_related('target_groups')
        )


class MessageInboxView(LoginRequiredMixin, ListView):
    '''List messages received by the current user.'''

    model = Message
    template_name = 'comunicacao/message_inbox.html'
    context_object_name = 'inbox_messages'
    paginate_by = 20

    def get_queryset(self):
        return (
            Message.objects.filter(receiver=self.request.user)
            .select_related('sender')
        )


class MessageDetailView(LoginRequiredMixin, DetailView):
    '''Display a single received message and mark it as read.'''

    model = Message
    template_name = 'comunicacao/message_detail.html'
    context_object_name = 'message'

    def get_queryset(self):
        '''Restrict access so users can only read their own received messages.'''
        return Message.objects.filter(receiver=self.request.user)

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        self.object.mark_as_read()
        return response


class MessageCreateView(LoginRequiredMixin, CreateView):
    '''Compose and send a new direct message.'''

    model = Message
    form_class = MessageForm
    template_name = 'comunicacao/message_form.html'
    success_url = reverse_lazy('comunicacao:inbox')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Exclude the current user from the receiver list; only active users.
        form.fields['receiver'].queryset = (
            form.fields['receiver'].queryset
            .exclude(pk=self.request.user.pk)
            .filter(is_active=True)
        )
        # Pre-select receiver when replying (query param ?receiver_id=<pk>).
        receiver_id = self.request.GET.get('receiver_id')
        if receiver_id:
            try:
                form.fields['receiver'].initial = int(receiver_id)
            except (ValueError, TypeError):
                pass
        return form

    def form_valid(self, form):
        form.instance.sender = self.request.user
        return super().form_valid(form)
