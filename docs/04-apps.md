# Aplicações (Apps) do Projeto

## 📦 Visão Geral das Aplicações

O projeto está organizado em múltiplas aplicações Django, cada uma com responsabilidades bem definidas.

---

## 🎓 academico

**Responsabilidade**: Gerenciar todas as funcionalidades acadêmicas da escola.

### Estrutura
```
academico/
├── migrations/         # Histórico de mudanças no banco
├── admin.py           # Registro de modelos no admin (vazio no momento)
├── apps.py            # Configuração da aplicação
├── models.py          # Modelos acadêmicos
├── tests.py           # Testes unitários
└── views.py           # Views (vazio no momento)
```

### Modelos Contidos
- `Turma`: Salas/turmas de alunos
- `Disciplina`: Disciplinas/matérias
- `Horario`: Horários de disciplinas
- `PlanoDeAula`: Planos de aula dos professores
- `Presenca`: Registro de presença em aulas
- `Avaliacao`: Avaliações/provas
- `Nota`: Notas de alunos

### Responsabilidades
- Gestão de turmas e suas composições
- Planos de aula e acompanhamento
- Controle de frequência
- Avaliações e notas

---

## 💬 comunicacao

**Responsabilidade**: Gerenciar sistema de comunicação entre usuários da plataforma.

### Estrutura
```
comunicacao/
├── migrations/
├── admin.py           # Registro de modelos no admin (vazio)
├── apps.py            # Configuração da aplicação
├── models.py          # Modelos de comunicação
├── tests.py           # Testes
└── views.py           # Views (vazio)
```

### Modelos Contidos
- `Mensagem`: Mensagens privadas entre usuários
- `AvisoMural`: Avisos públicos com público-alvo definido

### Responsabilidades
- Mensageria direta entre usuários
- Publicação de avisos institucionais
- Controle de acesso baseado no tipo de usuário

---

## 👥 usuarios

**Responsabilidade**: Gerenciar autenticação, autorização e perfis de usuários.

### Estrutura
```
usuarios/
├── migrations/
├── admin.py           # Registro de modelos no admin
├── apps.py            # Configuração da aplicação
├── models.py          # Modelo customizado de Usuario
├── tests.py           # Testes
└── views.py           # Views (vazio)
```

### Modelos Contidos
- `Usuario` (extends AbstractUser): Usuário customizado com tipos (aluno, professor, pais, coordenador)

### Responsabilidades
- Autenticação de usuários
- Classificação de usuários por tipo/papel
- Armazenamento de dados adicionais (CPF, telefone)
- Integração com sistema de permissões do Django

### Configuração no settings.py
```python
AUTH_USER_MODEL = 'usuarios.Usuario'
```

---

## 🏛️ institucional

**Responsabilidade**: Funcionalidades relacionadas à instituição como um todo.

### Estrutura
```
institucional/
├── migrations/
├── admin.py
├── apps.py
├── models.py           # (vazio no momento)
├── tests.py
└── views.py            # (vazio)
```

### Status
Aplicação criada mas ainda em desenvolvimento. Sem modelos definidos.

### Possíveis Responsabilidades (futuro)
- Dados institucionais (nome, logo, calendário)
- Configurações gerais da escola
- Relatórios institucionais

---

## 🎨 EduCore

**Responsabilidade**: Aplicação principal com integração do Tailwind CSS e configurações de frontend.

### Estrutura
```
EduCore/
├── migrations/
├── admin.py
├── apps.py
├── models.py           # (vazio no momento)
└── tests.py
```

### Responsabilidades
- Integração com Tailwind CSS (`TAILWIND_APP_NAME = 'EduCore'` em settings.py)
- Templates e componentes frontend
- Assets (CSS compilado, JavaScript)

### Configuração
Em `core/settings.py`:
```python
INSTALLED_APPS = [
    # ...
    'tailwind',
    'EduCore',
]

TAILWIND_APP_NAME = 'EduCore'
```

---

## ⚙️ core

**Responsabilidade**: Configurações principais e roteamento do projeto Django.

### Estrutura
```
core/
├── asgi.py            # Configuração ASGI para deploy
├── settings.py        # Configurações Django
├── urls.py            # Roteamento principal
└── wsgi.py            # Configuração WSGI para deploy
```

### Responsabilidades
- Configurações globais do Django
- Roteamento de URLs raiz
- Integração de middleware
- Configuração de banco de dados

### URLs Implementadas
```python
urlpatterns = [
    path('admin/', admin.site.urls),
]
```

---

## 🔌 Padrão de Estrutura de App

Cada aplicação segue o padrão Django padrão:

```python
# apps.py
class <AppName>Config(AppConfig):
    name = '<app_name>'
```

### Arquivo models.py
Contém todos os modelos ORM da aplicação.

### Arquivo views.py
Vazio no momento. Futuras views devem ser implementadas aqui.

### Arquivo admin.py
Registra modelos no Django Admin. Atualmente vazio em alguns apps.

---

## 📝 Padrões Observados

1. **Nomeação**: Apps seguem convenção snake_case
2. **Organização**: Cada domínio funcional em sua própria app
3. **Separação de Responsabilidades**: Modelos, views e admin bem delimitados
4. **Extensibilidade**: Apps podem crescer independentemente
5. **Integração com Usuario**: Referências ao modelo customizado via `settings.AUTH_USER_MODEL`
