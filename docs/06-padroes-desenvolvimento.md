# Padrões de Desenvolvimento

## 📏 Convenções de Código

### Nomeação

#### Modelos
- **PascalCase** (class CamelCase)
- Singular (não plural)
- Exemplos: `Usuario`, `Turma`, `Disciplina`, `Mensagem`

```python
class Usuario(AbstractUser):
    pass

class PlanoDeAula(models.Model):  # Composto: múltiplas palavras
    pass
```

#### Campos de Modelo
- **snake_case**
- Nomes descritivos em português
- Exemplos: `data_envio`, `hora_inicio`, `publico_alvo`

```python
class Mensagem(models.Model):
    data_envio = models.DateTimeField(auto_now_add=True)
    lida = models.BooleanField(default=False)
```

#### Aplicações (Apps)
- **snake_case**
- Singular ou plural conforme domínio
- Exemplos: `academico`, `comunicacao`, `usuarios`

#### Variáveis/Funções
- **snake_case**
- Nomes auto-explicativos
- Evitar abreviações

```python
def calcular_media_aluno(aluno_id):
    pass

def filtar_turmas_by_turno(turno):
    pass
```

---

## 🗂️ Organização de Arquivos

### Estrutura Padrão de Uma App

```
app_name/
├── migrations/          # Histórico de mudanças BD
│   └── __init__.py
├── __init__.py
├── admin.py             # Registro de modelos no admin
├── apps.py              # Configuração da app
├── models.py            # Definição de modelos ORM
├── tests.py             # Testes unitários
└── views.py             # Lógica de views
```

### Hierarquia Sugerida para Projetos Maiores

Se uma app crescer muito, pode-se organizar assim:

```
app_name/
├── migrations/
├── views/
│   ├── __init__.py
│   ├── operacao1.py
│   └── operacao2.py
├── models/
│   ├── __init__.py
│   ├── modelo1.py
│   └── modelo2.py
├── __init__.py
├── admin.py
├── apps.py
├── tests.py
└── urls.py
```

---

## 🗄️ Padrões de Modelos

### ForeignKey - Always Explicit `on_delete`

```python
# ✅ Correto
professor = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    limit_choices_to={'tipo': 'professor'}
)

# ❌ Evitar
professor = models.ForeignKey(settings.AUTH_USER_MODEL)
```

### Related Name Consistente

Use nomes descritivos e padronizados:

```python
# ✅ Bom
alunos = models.ManyToManyField(
    settings.AUTH_USER_MODEL,
    related_name='turmas'  # Usuario terá acesso a usuario.turmas.all()
)

# ❌ Evitar
alunos = models.ManyToManyField(settings.AUTH_USER_MODEL)
```

### Timestamps em Modelos

Use `auto_now_add` para data de criação:

```python
class Mensagem(models.Model):
    data_envio = models.DateTimeField(auto_now_add=True)  # ✅
```

Para atualização automática, use `auto_now` com cuidado:

```python
data_atualizacao = models.DateTimeField(auto_now=True)
```

### `__str__` Sempre Definido

Facilita debug e representação em admin:

```python
class Turma(models.Model):
    nome = models.CharField(max_length=100)
    turno = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.nome} - {self.turno}"
```

### Campos Opcionais

Use `blank=True` e `null=True` quando apropriado:

```python
class Usuario(AbstractUser):
    cpf = models.CharField(max_length=14, unique=True, blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
```

### Choices em Modelos

Use tuplas com choices:

```python
class Usuario(AbstractUser):
    TIPO_CHOICES = (
        ('aluno', 'Aluno'),
        ('professor', 'Professor'),
        ('pais', 'Pais/Responsáveis'),
    )
    tipo = models.CharField(max_length=15, choices=TIPO_CHOICES)
```

Acesso ao display:
```python
usuario.get_tipo_display()  # Retorna "Aluno" ao invés de "aluno"
```

---

## 🔒 Filtragem por Tipo de Usuário

Quando um campo ForeignKey deve ser restrito a um tipo específico, use `limit_choices_to`:

```python
professor = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.SET_NULL,
    null=True,
    limit_choices_to={'tipo': 'professor'}  # ✅ Restringe choices
)
```

Para múltiplos tipos:

```python
autor = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    limit_choices_to={'tipo__in': ['coordenador', 'professor']}  # ✅
)
```

---

## 🎨 Frontend com Tailwind CSS

### Localização de Templates

Siga convenção Django:

```
app_name/
├── templates/
│   └── app_name/
│       ├── lista.html
│       ├── detalhe.html
│       └── form.html
```

### Uso de Tailwind

Classes utility-first:

```html
<!-- ✅ Tailwind -->
<div class="flex items-center justify-between p-4 bg-blue-500 rounded-lg">
    <h1 class="text-2xl font-bold text-white">Título</h1>
</div>

<!-- ❌ Evitar CSS customizado desnecessário -->
<div style="display: flex; ...">
```

---

## 🧪 Testes

### Estrutura Básica

```python
# tests.py
from django.test import TestCase
from .models import Turma

class TurmaTestCase(TestCase):
    def setUp(self):
        """Executado antes de cada teste"""
        self.turma = Turma.objects.create(nome="1º Ano A", serie="1")

    def test_turma_str(self):
        """Testa representação em string"""
        self.assertEqual(str(self.turma), "1º Ano A - None")
```

### Executar Testes

```bash
python manage.py test                    # Todos
python manage.py test academico          # App específica
python manage.py test academico.tests    # Módulo específico
```

---

## 📝 Documentação de Código

### Docstrings

Use para modelos e funções complexas:

```python
class PlanoDeAula(models.Model):
    """
    Plano de aula criado por um professor.

    Armazena os objetivos, conteúdo e data de cada aula.
    Relacionado a uma turma, professor e disciplina específicos.
    """
    professor = models.ForeignKey(...)
    turma = models.ForeignKey(...)
```

### Comentários

Use com moderação, apenas para lógica não óbvia:

```python
# ✅ Bom: explica por quê
if usuario.tipo == 'aluno' and turma.alunos.filter(id=usuario.id).exists():
    # Apenas alunos inscritos podem acessar o conteúdo
    return True

# ❌ Ruim: óbvio demais
nome = models.CharField(max_length=100)  # Campo de nome com max 100 chars
```

---

## 🚀 Boas Práticas

### Importações

Use importações relativas dentro da mesma app:

```python
# ✅
from .models import Turma
from .views import turma_detail

# ❌
from academico.models import Turma
from academico.views import turma_detail
```

Para imports entre apps, use absolutas:

```python
from academico.models import Turma
from usuarios.models import Usuario
```

### QuerySets

Sempre use `.all()` ou `.filter()` para clareza:

```python
# ✅ Claro
turmas = Turma.objects.all()
alunos_presentes = usuario.presencas.filter(presente=True)

# Menos claro
turmas = Turma.objects
```

### Migrations

- Sempre execute `makemigrations` após mudar modelos
- Commit migrations junto com o código
- Nunca delete migration files (apenas crie novas)

```bash
python manage.py makemigrations
git add academico/migrations/
git commit -m "Add new fields to Turma model"
```

---

## 🔐 Segurança Básica

### Settings.py

```python
# ✅ Correto para produção
SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = False
ALLOWED_HOSTS = ['seu-dominio.com']

# ❌ Nunca fazer em produção
SECRET_KEY = 'hardcoded-secret'
DEBUG = True
ALLOWED_HOSTS = ['*']
```

### Autenticação

Use modelo `Usuario` customizado com `settings.AUTH_USER_MODEL`:

```python
# ✅ Correto
from django.conf import settings
usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

# ❌ Não fazer
from django.contrib.auth.models import User
usuario = models.ForeignKey(User, on_delete=models.CASCADE)
```

---

## 📚 Recursos Úteis

- [Django Documentação](https://docs.djangoproject.com/en/6.0/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Tailwind CSS Docs](https://tailwindcss.com/docs)

---

**Última atualização**: Março 2025
