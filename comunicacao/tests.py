from django.test import TestCase
from django.contrib.auth.models import Group

from usuarios.models import User
from comunicacao.models import Message, NoticeBoard


class NoticeBoardModelTests(TestCase):
    '''Testa o modelo NoticeBoard.'''

    def setUp(self):
        coord_group = Group.objects.create(name='Coordinators')
        self.coordinator = User.objects.create_user(
            email='coordenador@exemplo.com',
            password='senha123',
            first_name='Ana',
            last_name='Lima',
        )
        self.coordinator.groups.add(coord_group)

    def test_criar_aviso(self):
        '''NoticeBoard e criado com os campos corretos.'''
        notice = NoticeBoard.objects.create(
            title='Reuniao de Pais',
            content='Reuniao marcada para sexta-feira.',
            author=self.coordinator,
            is_published=True,
        )
        self.assertEqual(notice.title, 'Reuniao de Pais')
        self.assertTrue(notice.is_published)

    def test_aviso_draft_nao_publicado(self):
        '''Aviso criado sem publicacao e um draft.'''
        notice = NoticeBoard.objects.create(
            title='Rascunho',
            content='Conteudo provisorio.',
            author=self.coordinator,
        )
        self.assertFalse(notice.is_published)

    def test_publish_method(self):
        '''O metodo publish() marca o aviso como publicado.'''
        notice = NoticeBoard.objects.create(
            title='Aviso Teste',
            content='Conteudo.',
            author=self.coordinator,
            is_published=False,
        )
        notice.publish()
        notice.refresh_from_db()
        self.assertTrue(notice.is_published)
        self.assertIsNotNone(notice.published_at)

    def test_is_visible_to_todos(self):
        '''Aviso sem grupo alvo e visivel a qualquer usuario autenticado.'''
        notice = NoticeBoard.objects.create(
            title='Aviso Geral',
            content='Para todos.',
            author=self.coordinator,
            is_published=True,
        )
        outro_usuario = User.objects.create_user(
            email='outro@exemplo.com',
            password='senha123',
        )
        self.assertTrue(notice.is_visible_to(outro_usuario))

    def test_str_notice(self):
        '''__str__ inclui o titulo e o status do aviso.'''
        notice = NoticeBoard.objects.create(
            title='Aviso Str',
            content='Teste.',
            author=self.coordinator,
            is_published=True,
        )
        self.assertIn('Aviso Str', str(notice))
        self.assertIn('Published', str(notice))


class MessageModelTests(TestCase):
    '''Testa o modelo Message.'''

    def setUp(self):
        self.sender = User.objects.create_user(
            email='remetente@exemplo.com',
            password='senha123',
        )
        self.receiver = User.objects.create_user(
            email='destinatario@exemplo.com',
            password='senha123',
        )

    def test_criar_mensagem(self):
        '''Message e criada com is_read=False por padrao.'''
        msg = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            subject='Ola',
            body='Esta e uma mensagem de teste.',
        )
        self.assertEqual(msg.sender, self.sender)
        self.assertEqual(msg.receiver, self.receiver)
        self.assertFalse(msg.is_read)
        self.assertIsNone(msg.read_at)

    def test_mark_as_read(self):
        '''mark_as_read() marca a mensagem como lida e registra o timestamp.'''
        msg = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            subject='Teste',
            body='Corpo.',
        )
        msg.mark_as_read()
        msg.refresh_from_db()
        self.assertTrue(msg.is_read)
        self.assertIsNotNone(msg.read_at)

    def test_mark_as_read_idempotente(self):
        '''Chamar mark_as_read() duas vezes nao levanta erro.'''
        msg = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            subject='Idempotente',
            body='Corpo.',
        )
        msg.mark_as_read()
        first_read_at = msg.read_at
        msg.mark_as_read()
        # read_at nao deve mudar na segunda chamada
        self.assertEqual(msg.read_at, first_read_at)

    def test_str_mensagem(self):
        '''__str__ inclui os emails do remetente e destinatario.'''
        msg = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            subject='Assunto Teste',
            body='Corpo.',
        )
        self.assertIn(self.sender.email, str(msg))
        self.assertIn(self.receiver.email, str(msg))
