# usuarios/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    TIPO_CHOICES = (
        ('aluno', 'Aluno'),
        ('professor', 'Professor'),
        ('pais', 'Pais/Responsáveis'),
        ('coordenador', 'Coordenador'),
    )
    tipo = models.CharField(max_length=15, choices=TIPO_CHOICES, default='aluno')
    cpf = models.CharField(max_length=14, unique=True, blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.get_full_name()} ({self.get_tipo_display()})"