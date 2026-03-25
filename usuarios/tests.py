from django.db import IntegrityError
from django.test import TestCase
from django.contrib.auth.models import Group

from usuarios.models import Guardian, User


class UserModelTests(TestCase):
    '''Testa o modelo User e autenticacao por e-mail.'''

    def setUp(self):
        self.user = User.objects.create_user(
            email='teste@exemplo.com',
            password='senha123',
            first_name='Joao',
            last_name='Silva',
        )

    def test_criar_usuario_com_email(self):
        '''Criacao de usuario com email funciona corretamente.'''
        self.assertEqual(self.user.email, 'teste@exemplo.com')
        self.assertTrue(self.user.check_password('senha123'))
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)

    def test_representacao_str(self):
        '''__str__ retorna o e-mail do usuario.'''
        self.assertEqual(str(self.user), 'teste@exemplo.com')

    def test_get_full_name(self):
        '''get_full_name retorna nome completo.'''
        self.assertEqual(self.user.get_full_name(), 'Joao Silva')

    def test_criar_superusuario(self):
        '''create_superuser define is_staff e is_superuser como True.'''
        admin = User.objects.create_superuser(
            email='admin@exemplo.com',
            password='admin123',
            first_name='Admin',
            last_name='Sistema',
        )
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)
        self.assertTrue(admin.is_active)

    def test_email_obrigatorio(self):
        '''Criar usuario sem e-mail levanta ValueError.'''
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password='senha123')


class GuardianModelTests(TestCase):
    '''Testa o modelo Guardian (vinculo responsavel-aluno).'''

    def setUp(self):
        self.parents_group = Group.objects.create(name='Parents')
        self.students_group = Group.objects.create(name='Students')

        self.parent = User.objects.create_user(
            email='responsavel@exemplo.com',
            password='senha123',
            first_name='Maria',
            last_name='Santos',
        )
        self.parent.groups.add(self.parents_group)

        self.student = User.objects.create_user(
            email='aluno@exemplo.com',
            password='senha123',
            first_name='Pedro',
            last_name='Santos',
        )
        self.student.groups.add(self.students_group)

    def test_criar_vinculo_guardian(self):
        '''Vinculo responsavel-aluno e criado corretamente.'''
        guardian = Guardian.objects.create(
            parent=self.parent,
            student=self.student,
            relationship_type='mother',
        )
        self.assertEqual(guardian.parent, self.parent)
        self.assertEqual(guardian.student, self.student)
        self.assertEqual(guardian.relationship_type, 'mother')

    def test_unique_together_parent_student(self):
        '''O par (parent, student) deve ser unico.'''
        Guardian.objects.create(
            parent=self.parent,
            student=self.student,
            relationship_type='mother',
        )
        with self.assertRaises(IntegrityError):
            Guardian.objects.create(
                parent=self.parent,
                student=self.student,
                relationship_type='father',
            )

    def test_representacao_str(self):
        '''__str__ retorna a representacao legivel do vinculo.'''
        guardian = Guardian.objects.create(
            parent=self.parent,
            student=self.student,
            relationship_type='guardian',
        )
        self.assertIn(self.parent.email, str(guardian))
        self.assertIn(self.student.email, str(guardian))
