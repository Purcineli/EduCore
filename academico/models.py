# academico/models.py
from django.db import models
from django.conf import settings

class Turma(models.Model):
    nome = models.CharField(max_length=100) # Ex: 1º Ano A
    serie = models.CharField(max_length=50)
    turno = models.CharField(max_length=20, choices=[('manha', 'Manhã'), ('tarde', 'Tarde'), ('noite', 'Noite')])
    alunos = models.ManyToManyField(settings.AUTH_USER_MODEL, limit_choices_to={'tipo': 'aluno'}, related_name='turmas')

    def __str__(self):
        return f"{self.nome} - {self.turno}"

class Disciplina(models.Model):
    nome = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nome

class Horario(models.Model):
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name='horarios')
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    professor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, limit_choices_to={'tipo': 'professor'})
    dia_semana = models.IntegerField(choices=[(0, 'Segunda'), (1, 'Terça'), (2, 'Quarta'), (3, 'Quinta'), (4, 'Sexta')])
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()

class PlanoDeAula(models.Model):
    professor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'tipo': 'professor'})
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    data = models.DateField()
    objetivos = models.TextField()
    conteudo = models.TextField()

class Presenca(models.Model):
    plano_aula = models.ForeignKey(PlanoDeAula, on_delete=models.CASCADE, related_name='presencas')
    aluno = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'tipo': 'aluno'})
    presente = models.BooleanField(default=True)

class Avaliacao(models.Model):
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    bimestre = models.IntegerField(choices=[(1, '1º Bimestre'), (2, '2º Bimestre'), (3, '3º Bimestre'), (4, '4º Bimestre')])
    titulo = models.CharField(max_length=100) # Ex: Prova Mensal
    data = models.DateField()

class Nota(models.Model):
    avaliacao = models.ForeignKey(Avaliacao, on_delete=models.CASCADE, related_name='notas')
    aluno = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'tipo': 'aluno'})
    valor = models.DecimalField(max_digits=5, decimal_places=2)