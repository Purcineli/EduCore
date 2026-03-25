from comunicacao.models import Message


def unread_messages_count(request):
    '''Adiciona a contagem de mensagens nao lidas ao contexto de todos os templates.'''
    if request.user.is_authenticated:
        count = Message.objects.filter(
            receiver=request.user,
            is_read=False,
        ).count()
        return {'unread_messages_count': count}
    return {'unread_messages_count': 0}
