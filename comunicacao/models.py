# comunicacao/models.py
from django.db import models
from django.conf import settings

class Mensagem(models.Model):
    remetente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mensagens_enviadas')
    destinatario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mensagens_recebidas')
    assunto = models.CharField(max_length=200)
    corpo = models.TextField()
    data_envio = models.DateTimeField(auto_now_add=True)
    lida = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.assunto} - De {self.remetente} para {self.destinatario}"

class AvisoMural(models.Model):
    PUBLICO_CHOICES = [
        ('todos', 'Todos'),
        ('alunos', 'Apenas Alunos'),
        ('professores', 'Apenas Professores'),
        ('pais', 'Apenas Pais/Responsáveis'),
    ]
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'tipo__in': ['coordenador', 'professor']})
    titulo = models.CharField(max_length=200)
    conteudo = models.TextField()
    data_publicacao = models.DateTimeField(auto_now_add=True)
    publico_alvo = models.CharField(max_length=20, choices=PUBLICO_CHOICES, default='todos')

    def __str__(self):
        return self.titulo