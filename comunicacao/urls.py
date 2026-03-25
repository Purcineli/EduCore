from django.urls import path

from .views import (
    MessageCreateView,
    MessageDetailView,
    MessageInboxView,
    NoticeBoardListView,
)

app_name = 'comunicacao'

urlpatterns = [
    path('notices/', NoticeBoardListView.as_view(), name='noticeboard-list'),
    path('messages/', MessageInboxView.as_view(), name='inbox'),
    path('messages/send/', MessageCreateView.as_view(), name='message-create'),
    path('messages/<int:pk>/', MessageDetailView.as_view(), name='message-detail'),
]
