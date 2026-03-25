# Estrutura do Projeto

## 📂 Hierarquia de Diretórios

```
escola/
├── academico/              # App para funcionalidades acadêmicas
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py          # Modelos acadêmicos
│   ├── tests.py
│   └── views.py
│
├── comunicacao/            # App para comunicações
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py          # Modelos de mensagens e avisos
│   ├── tests.py
│   └── views.py
│
├── institucional/          # App para funcionalidades institucionais
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
│
├── usuarios/              # App para gerenciamento de usuários
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py          # Modelo customizado de Usuário
│   ├── tests.py
│   └── views.py
│
├── EduCore/               # App principal com configurações Tailwind
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   └── tests.py
│
├── core/                  # Configurações principais do Django
│   ├── __init__.py
│   ├── asgi.py           # Configuração ASGI
│   ├── settings.py       # Configurações do Django
│   ├── urls.py           # URL patterns raiz
│   └── wsgi.py           # Configuração WSGI
│
├── venv/                  # Ambiente virtual Python
├── db.sqlite3            # Banco de dados (desenvolvimento)
├── manage.py             # Script de gerenciamento Django
├── requirements.txt      # Dependências do projeto
├── PRD.md               # Product Requirements Document
├── tasks.md             # Tarefas do projeto
└── docs/                # Esta documentação
```

## 📦 Aplicações Principais

### `core/`
Módulo de configuração principal do Django. Contém:
- **settings.py**: Configurações globais da aplicação
- **urls.py**: Roteamento principal de URLs
- **wsgi.py** e **asgi.py**: Configurações para deployment

### `academico/`
Gerenciamento de funcionalidades acadêmicas:
- Turmas, disciplinas, horários
- Planos de aula, presenças
- Avaliações e notas

### `comunicacao/`
Sistema de comunicação entre usuários:
- Mensagens diretas
- Avisos murais com público-alvo

### `usuarios/`
Gerenciamento de usuários:
- Modelo customizado baseado em AbstractUser
- Tipos de usuário: aluno, professor, pais, coordenador

### `institucional/`
Funcionalidades institucionais (em desenvolvimento)

### `EduCore/`
Aplicação principal com:
- Integração com Tailwind CSS
- Configurações de frontend

## 🔧 Dependências Principais

Ver `requirements.txt` para lista completa. Principais:
- **Django 6.0.3**: Framework web
- **djangorestframework 3.17.0**: APIs REST
- **django-tailwind 4.4.2**: Framework CSS
- **psycopg2-binary 2.9.11**: Adaptador PostgreSQL (para produção)
