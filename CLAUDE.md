# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 🏗️ Arquitetura de Alto Nível

**EduCore** é um sistema de gestão escolar em Django 6.0.3 organizado por domínio funcional em aplicações independentes:

```
Django Project (core/)
├── academico/       → Turmas, disciplinas, horários, planos de aula, frequência, avaliações
├── comunicacao/     → Mensagens privadas, avisos murais
├── usuarios/        → Modelo customizado de Usuário com tipos (aluno, professor, pais, coordenador)
├── institucional/   → Funcionalidades institucionais (em desenvolvimento)
└── EduCore/         → App principal com Tailwind CSS
```

### Modelo de Usuários Customizado

O projeto **não usa** `django.contrib.auth.User`. Em vez disso, usa `usuarios.Usuario` (extends `AbstractUser`) com campo `tipo` para classificação:

```python
# settings.py já configura isso:
AUTH_USER_MODEL = 'usuarios.Usuario'

# Tipos: 'aluno', 'professor', 'pais', 'coordenador'
```

**Isso é crítico**: Qualquer referência a usuários deve usar `settings.AUTH_USER_MODEL` ao invés de hardcoding `User`.

### Padrões de Modelos

Todos os modelos seguem convenções explícitas:

- **ForeignKey sempre com `on_delete` explícito**: `on_delete=models.CASCADE`, `SET_NULL`, etc.
- **`related_name` descritivo**: facilita acesso reverso (ex: `usuario.mensagens_enviadas.all()`)
- **`limit_choices_to` para filtrar usuários**: ex: `limit_choices_to={'tipo': 'professor'}`
- **`__str__` sempre definido**: para debug e admin
- **Timestamps automáticos**: usar `auto_now_add=True` para datas de criação

Exemplo correto:
```python
professor = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.SET_NULL,
    null=True,
    limit_choices_to={'tipo': 'professor'},
    related_name='disciplinas'
)
```

---

## 🛠️ Comandos Essenciais

### Desenvolvimento

```bash
# Ativar ambiente virtual
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows

# Instalar dependências
pip install -r requirements.txt

# Executar migrations
python manage.py makemigrations  # Gerar migrations após alterar models.py
python manage.py migrate         # Aplicar migrations

# Iniciar servidor de desenvolvimento
python manage.py runserver

# Criar superusuário (admin)
python manage.py createsuperuser

# Shell interativa para testar queries
python manage.py shell
```

### Testes

```bash
# Executar todos os testes
python manage.py test

# Testes de uma app específica
python manage.py test academico

# Testes de uma classe específica
python manage.py test academico.tests.TurmaTestCase

# Testes verbosos
python manage.py test --verbosity=2
```

### Tailwind CSS

```bash
# Build Tailwind CSS
python manage.py tailwind build

# Watch mode (recompila ao salvar)
python manage.py tailwind start
```

### Linting e Formatação

O projeto **não tem** linter ou formatter configurado atualmente. Sugestão futura:
- **black** para formatação automática
- **flake8** para linting
- **isort** para organização de imports

---

## 📁 Estrutura de Pasta de App

Quando adicionar uma nova app, siga este padrão:

```
nova_app/
├── migrations/
│   └── __init__.py
├── __init__.py
├── admin.py           # Registrar modelos: admin.site.register(MeuModelo)
├── apps.py            # Classe Config (não alterar nome)
├── models.py          # Definir todos os modelos aqui
├── tests.py           # Testes unitários
└── views.py           # Views (CBV ou FBV)
```

Depois:
1. Adicionar app ao `INSTALLED_APPS` em `core/settings.py`
2. Rodar `python manage.py makemigrations nova_app`
3. Rodar `python manage.py migrate`

---

## 🗄️ Banco de Dados

### Desenvolvimento
- **SQLite3** (`db.sqlite3`)
- Adequado para desenvolvimento local

### Produção
- Usar **PostgreSQL** (driver `psycopg2-binary` já está em requirements.txt)
- Configurar em `core/settings.py` antes de fazer deploy

### Resetar Banco (Desenvolvimento)

```bash
# Deletar banco e reaplicar todas as migrations
rm db.sqlite3
python manage.py migrate

# Se quiser rescriar superusuário também
python manage.py createsuperuser
```

---

## ⚙️ Configurações Importantes (settings.py)

### Variáveis de Ambiente (TODO)

**⚠️ Recomendação importante**: As seguintes variáveis estão hardcoded e devem ser movidas para variáveis de ambiente em produção:

```python
SECRET_KEY = 'django-insecure-...'  # Usar os.getenv('SECRET_KEY')
DEBUG = True                        # Usar os.getenv('DEBUG') == 'True'
ALLOWED_HOSTS = ['*']              # Restringir em produção
```

Package `python-dotenv` já está em requirements.txt. Criar `.env` na raiz:
```
SECRET_KEY=seu-secret-aqui
DEBUG=False
ALLOWED_HOSTS=seu-dominio.com,www.seu-dominio.com
```

### Modelo de Usuário

```python
AUTH_USER_MODEL = 'usuarios.Usuario'  # Já configurado
```

Qualquer novo model com FK para usuário DEVE usar:
```python
from django.conf import settings
usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
```

### Apps Instaladas

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tailwind',           # django-tailwind
    'EduCore',            # App principal
    # Adicionar novas apps aqui
]

TAILWIND_APP_NAME = 'EduCore'  # Templates e CSS em EduCore/
```

---

## 📚 Workflow de Desenvolvimento

### Adicionar um Novo Modelo

1. Criar classe em `app_name/models.py`
2. Sempre incluir:
   - `on_delete` explícito em ForeignKey
   - `related_name` em relacionamentos
   - `__str__()` para representação
3. Rodar: `python manage.py makemigrations app_name`
4. Rodar: `python manage.py migrate`
5. Registrar em `app_name/admin.py` se quiser no Django Admin:
   ```python
   from django.contrib import admin
   from .models import MeuModelo
   admin.site.register(MeuModelo)
   ```

### Modificar um Modelo Existente

1. Alterar classe em `models.py`
2. Se remover campo sem `null=True` em dados existentes, Django pedirá valor padrão
3. Rodar: `python manage.py makemigrations`
4. Rodar: `python manage.py migrate`
5. **Sempre commitar migrations junto com mudanças de código**

### Testar Mudanças

```bash
# Abrir shell e testar queries
python manage.py shell
>>> from academico.models import Turma
>>> Turma.objects.all()

# Ou rodar testes
python manage.py test academico
```

---

## 🔗 Padrões Observados no Código

### Imports de Modelos

```python
# ✅ Correto - referência via settings
from django.conf import settings
professor = models.ForeignKey(settings.AUTH_USER_MODEL, ...)

# ❌ Errado - hardcoding
from usuarios.models import Usuario
professor = models.ForeignKey(Usuario, ...)
```

### Choices em Modelos

```python
class Turma(models.Model):
    TURNO_CHOICES = [
        ('manha', 'Manhã'),
        ('tarde', 'Tarde'),
        ('noite', 'Noite'),
    ]
    turno = models.CharField(max_length=20, choices=TURNO_CHOICES)

# Acessar o display:
turma.get_turno_display()  # Retorna "Manhã"
```

### Restrição de Usuários por Tipo

```python
# Apenas professores podem ser selecionados
professor = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    limit_choices_to={'tipo': 'professor'}
)

# Múltiplos tipos
autor = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    limit_choices_to={'tipo__in': ['coordenador', 'professor']}
)
```

---

## 📖 Documentação do Projeto

Toda a documentação está em `/docs/`:

- **docs/README.md** - Índice geral
- **docs/01-estrutura-projeto.md** - Hierarquia de pastas
- **docs/02-arquitetura.md** - Stack, banco de dados
- **docs/03-models.md** - Detalhamento completo de modelos
- **docs/04-apps.md** - Responsabilidades de cada app
- **docs/05-configuracao-desenvolvimento.md** - Setup e configuração
- **docs/06-padroes-desenvolvimento.md** - Convenções e boas práticas

Consulte quando precisar entender estrutura ou padrões do projeto.

---

## 🚨 Pontos de Atenção

1. **Usar `settings.AUTH_USER_MODEL`**: Nunca hardcode o modelo de usuário
2. **Migrations**: Sempre commitar junto com mudanças de models.py
3. **on_delete explícito**: Sem exceções em ForeignKey
4. **related_name descritivo**: Facilita queries reversas
5. **DEBUG e SECRET_KEY**: Nunca fazer commit com DEBUG=True ou SECRET_KEY em produção
6. **Banco SQLite**: Adequado para dev, usar PostgreSQL em produção

---

## 🔄 Django Admin

Django Admin é acessível em `/admin/` após criar superusuário:

```bash
python manage.py createsuperuser
```

Para registrar um modelo no admin:

```python
# app_name/admin.py
from django.contrib import admin
from .models import Turma, Disciplina

admin.site.register(Turma)
admin.site.register(Disciplina)
```

---

## 📦 Dependências Principais

Ver `requirements.txt`. Principais:
- **Django 6.0.3**: Framework web
- **djangorestframework 3.17.0**: APIs REST (instalado, não implementado ainda)
- **django-tailwind 4.4.2**: Integração Tailwind CSS
- **psycopg2-binary**: Driver PostgreSQL para produção
- **python-dotenv**: Variáveis de ambiente

---

## 🚀 Próximos Passos Sugeridos

1. Mover secrets para variáveis de ambiente (.env)
2. Configurar CORS se houver frontend separado
3. Implementar views e URLs (atualmente vazias)
4. Registrar modelos no Django Admin
5. Implementar testes para modelos existentes
6. Configurar DRF para APIs REST
7. Estruturar templates com Tailwind CSS

---

**Última atualização**: Março 2025
