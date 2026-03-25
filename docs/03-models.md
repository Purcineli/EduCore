# Modelos do Projeto

## 📋 Visão Geral

O projeto está organizado em modelos por domínio funcional. Todos os modelos utilizam padrões Django com `on_delete` explícito e `related_name` para relacionamentos.

---

## 👥 Modelo de Usuários (`usuarios/models.py`)

### Usuario (extends AbstractUser)

Modelo customizado que estende o AbstractUser do Django com campos adicionais específicos da escola.

```python
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
```

**Campos**:
- `tipo`: Classificação do usuário na escola
- `cpf`: CPF único (opcional)
- `telefone`: Contato (opcional)
- Herda: `username`, `email`, `first_name`, `last_name`, etc. (AbstractUser)

---

## 🎓 Modelos Acadêmicos (`academico/models.py`)

### Turma

Representa uma turma/classe escolar.

```python
class Turma(models.Model):
    nome = models.CharField(max_length=100)           # Ex: "1º Ano A"
    serie = models.CharField(max_length=50)
    turno = models.CharField(
        max_length=20,
        choices=[('manha', 'Manhã'), ('tarde', 'Tarde'), ('noite', 'Noite')]
    )
    alunos = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        limit_choices_to={'tipo': 'aluno'},
        related_name='turmas'
    )
```

### Disciplina

Matéria/disciplina lecionada.

```python
class Disciplina(models.Model):
    nome = models.CharField(max_length=100)
```

### Horario

Horário de uma disciplina em uma turma.

```python
class Horario(models.Model):
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name='horarios')
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    professor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={'tipo': 'professor'}
    )
    dia_semana = models.IntegerField(
        choices=[(0, 'Segunda'), (1, 'Terça'), (2, 'Quarta'), (3, 'Quinta'), (4, 'Sexta')]
    )
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()
```

### PlanoDeAula

Plano de aula criado por um professor.

```python
class PlanoDeAula(models.Model):
    professor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'tipo': 'professor'}
    )
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    data = models.DateField()
    objetivos = models.TextField()
    conteudo = models.TextField()
```

### Presenca

Registro de presença em uma aula.

```python
class Presenca(models.Model):
    plano_aula = models.ForeignKey(
        PlanoDeAula,
        on_delete=models.CASCADE,
        related_name='presencas'
    )
    aluno = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'tipo': 'aluno'}
    )
    presente = models.BooleanField(default=True)
```

### Avaliacao

Avaliação/prova de uma disciplina.

```python
class Avaliacao(models.Model):
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    bimestre = models.IntegerField(
        choices=[(1, '1º Bimestre'), (2, '2º Bimestre'), (3, '3º Bimestre'), (4, '4º Bimestre')]
    )
    titulo = models.CharField(max_length=100)  # Ex: "Prova Mensal"
    data = models.DateField()
```

### Nota

Nota de um aluno em uma avaliação.

```python
class Nota(models.Model):
    avaliacao = models.ForeignKey(Avaliacao, on_delete=models.CASCADE, related_name='notas')
    aluno = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'tipo': 'aluno'}
    )
    # (campo valor não finalizado no código atual)
```

---

## 💬 Modelos de Comunicação (`comunicacao/models.py`)

### Mensagem

Mensagem privada entre usuários.

```python
class Mensagem(models.Model):
    remetente = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='mensagens_enviadas'
    )
    destinatario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='mensagens_recebidas'
    )
    assunto = models.CharField(max_length=200)
    corpo = models.TextField()
    data_envio = models.DateTimeField(auto_now_add=True)
    lida = models.BooleanField(default=False)
```

### AvisoMural

Aviso público com público-alvo específico.

```python
class AvisoMural(models.Model):
    PUBLICO_CHOICES = [
        ('todos', 'Todos'),
        ('alunos', 'Apenas Alunos'),
        ('professores', 'Apenas Professores'),
        ('pais', 'Apenas Pais/Responsáveis'),
    ]
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'tipo__in': ['coordenador', 'professor']}
    )
    titulo = models.CharField(max_length=200)
    conteudo = models.TextField()
    data_publicacao = models.DateTimeField(auto_now_add=True)
    publico_alvo = models.CharField(max_length=20, choices=PUBLICO_CHOICES, default='todos')
```

---

## 🔗 Padrões Observados

1. **Sempre `on_delete` explícito**: Todos os ForeignKey têm comportamento definido (CASCADE, SET_NULL, etc.)
2. **`related_name` consistente**: Facilita acesso reverso aos relacionamentos
3. **`limit_choices_to` em usuários**: Restringe seleção por tipo de usuário quando apropriado
4. **Timestamps**: `auto_now_add` para datas de criação (ex: PlanoDeAula, Mensagem)
5. **`__str__` definido**: Para melhor representação em admin e debug
6. **Campos opcional com `blank` e `null`**: Quando aplicável (ex: CPF, telefone)
