# Arquitetura do Projeto

## 🏗️ Stack Tecnológico

| Componente | Tecnologia | Versão |
|-----------|-----------|--------|
| Framework Web | Django | 6.0.3 |
| API REST | Django REST Framework | 3.17.0 |
| Frontend Styling | Tailwind CSS | (via django-tailwind) |
| Banco de Dados | SQLite (dev) / PostgreSQL (prod) | - |
| Autenticação | Django Auth customizado | 6.0.3 |
| Python | - | 3.x |

## 💾 Banco de Dados

### Desenvolvimento
- **Engine**: SQLite3
- **Local**: `db.sqlite3` na raiz do projeto
- **Apropriado para**: Desenvolvimento local e testes

### Configuração
```python
# core/settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

### Migrações
O projeto usa o sistema de migrações do Django:
- Arquivos de migração em `app/migrations/`
- Executar: `python manage.py migrate`

## 🔐 Autenticação e Autorização

### Modelo de Usuário Customizado
Baseado em `AbstractUser` com campo adicional `tipo`:

```python
class Usuario(AbstractUser):
    TIPO_CHOICES = (
        ('aluno', 'Aluno'),
        ('professor', 'Professor'),
        ('pais', 'Pais/Responsáveis'),
        ('coordenador', 'Coordenador'),
    )
    tipo = models.CharField(max_length=15, choices=TIPO_CHOICES)
    cpf = models.CharField(max_length=14, unique=True, blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
```

### Referência no settings.py
```python
AUTH_USER_MODEL = 'usuarios.Usuario'
```

## 📱 Frontend

### Tailwind CSS
- Framework CSS utility-first
- Configuração: `django-tailwind`
- App principal: `EduCore`

## 🔄 Padrão MVT (Model-View-Template)

O projeto segue o padrão MVT do Django:
- **Models**: Definidos em `models.py` de cada app
- **Views**: Lógica de negócio em `views.py`
- **Templates**: (Em EduCore) com Tailwind CSS

## 🗄️ Estrutura de Dados

Principais entidades:
- **Usuários**: Alunos, Professores, Pais/Responsáveis, Coordenadores
- **Acadêmicas**: Turmas, Disciplinas, Horários, Planos de Aula, Avaliações
- **Comunicação**: Mensagens, Avisos

## ⚙️ Middleware Ativo

Padrão do Django 6.0:
```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```
