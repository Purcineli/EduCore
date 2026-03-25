# Configuração de Desenvolvimento

## 🔧 Ambiente de Desenvolvimento

### Requisitos

- **Python**: 3.x (compatível com Django 6.0.3)
- **pip**: Gerenciador de pacotes Python
- **venv**: Ambiente virtual (incluído no Python)

### Dependências Principais

Ver arquivo `requirements.txt` para lista completa. Principais:

```
Django==6.0.3
djangorestframework==3.17.0
django-tailwind==4.4.2
psycopg2-binary==2.9.11
```

## 🚀 Instalação Inicial

### 1. Criar Ambiente Virtual

```bash
# Windows
python -m venv venv

# Linux/Mac
python3 -m venv venv
```

### 2. Ativar Ambiente Virtual

```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instalar Dependências

```bash
pip install -r requirements.txt
```

## 🗄️ Configuração do Banco de Dados

### Desenvolvimento

O projeto usa **SQLite3** por padrão:

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

#### Criar e aplicar migrações

```bash
# Criar migrações pendentes
python manage.py makemigrations

# Aplicar migrações ao banco
python manage.py migrate
```

#### Resetar banco de dados (desenvolvimento)

```bash
# Deletar db.sqlite3 e rodar migrate novamente
rm db.sqlite3  # Linux/Mac
del db.sqlite3  # Windows
python manage.py migrate
```

## 👤 Criação de Superusuário

Para acessar o Django Admin:

```bash
python manage.py createsuperuser
```

Siga as instruções interativas. Após criação:
- Acesse: `http://localhost:8000/admin/`
- Use credenciais de superusuário

## 🏃 Rodando o Servidor de Desenvolvimento

```bash
python manage.py runserver
```

Acesse em: `http://localhost:8000`

## ⚙️ Configurações Principais (settings.py)

### Variáveis de Ambiente

Atualmente hardcoded (não recomendado para produção):

```python
SECRET_KEY = 'django-insecure-...'  # ⚠️ Usar variáveis de ambiente
DEBUG = True                        # ⚠️ Deve ser False em produção
ALLOWED_HOSTS = ['*']              # ⚠️ Restringir em produção
```

**Melhorias Recomendadas**:
- Usar `python-dotenv` (já no requirements.txt) para gerenciar secrets
- Criar `.env` na raiz do projeto

### Apps Instalados

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tailwind',
    'EduCore',
]
```

### Middleware

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

### Templates

Usa template engine padrão do Django:

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # Diretórios customizados de templates (vazio no momento)
        'APP_DIRS': True,  # Procura em app_name/templates/
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

## 🎨 Tailwind CSS

### Configuração

```python
TAILWIND_APP_NAME = 'EduCore'  # App onde Tailwind está configurado
```

### Compilação de CSS

```bash
# Build Tailwind CSS
python manage.py tailwind build

# Watch mode (desenvolvimento)
python manage.py tailwind start
```

## 🧪 Testes

### Executar Testes

```bash
# Todos os testes
python manage.py test

# App específica
python manage.py test academico

# Teste específico
python manage.py test academico.tests.NomeDoTeste
```

## 📊 Django Admin

O Django Admin é acessível em `/admin/` após criar um superusuário.

**Apps sem modelos registrados**:
- Algumas apps têm `admin.py` vazio
- Modelos não aparecem no admin automaticamente
- Registrar: adicionar em `app/admin.py`:

```python
from django.contrib import admin
from .models import SeuModelo

admin.site.register(SeuModelo)
```

## 🐛 Debugging

### Shell Interativa Django

```bash
python manage.py shell
```

Útil para testar queries ORM:

```python
>>> from usuarios.models import Usuario
>>> Usuario.objects.all()
<QuerySet [...]>
```

## 📝 Estrutura de Arquivos Importantes

| Arquivo | Propósito |
|---------|-----------|
| `manage.py` | Script de gerenciamento Django |
| `requirements.txt` | Dependências do projeto |
| `core/settings.py` | Configurações globais |
| `core/urls.py` | Roteamento principal |
| `db.sqlite3` | Banco de dados (desenvolvimento) |
| `venv/` | Ambiente virtual |

## ⚠️ Considerações para Produção

1. **Secret Key**: Usar variável de ambiente
2. **DEBUG**: Definir como `False`
3. **ALLOWED_HOSTS**: Restringir aos domínios reais
4. **Database**: Migrar para PostgreSQL com `psycopg2`
5. **Static Files**: Configurar servindo correto (WhiteNoise, AWS S3, etc.)
6. **Variáveis de Ambiente**: Usar arquivo `.env` com `python-dotenv`
