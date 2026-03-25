# Agentes de Desenvolvimento - EduCore

Este diretório contém especificações de agentes de IA especializados em diferentes funções do time de desenvolvimento do **EduCore**.

Cada agente é um especialista na stack específica do projeto e deve ser utilizado para sua função designada.

---

## 📋 Índice de Agentes

### 1. [Backend Django Developer](01-backend-django-developer.md)
**Especialista em**: Django ORM, Models, Views, Signals, Migrations
**Stack**: Django 6.0.3, Python, PostgreSQL/SQLite
**Responsável por**:
- Desenvolvimento de modelos ORM
- Views e business logic
- Signals e hooks
- Migrações de banco de dados
- Consultas e otimizações

**Quando usar**: Criar/modificar modelos, implementar lógica de negócio, resolver problemas com ORM

---

### 2. [Frontend & UI Developer](02-frontend-ui-developer.md)
**Especialista em**: Django Templates, Tailwind CSS, HTML, JavaScript
**Stack**: Django Template Language, Tailwind CSS 4.x, HTML5, Vanilla JS
**Responsável por**:
- Criação de templates Django
- Layouts responsivos com Tailwind
- Componentes reutilizáveis
- UX/UI improvements
- Integração de formulários

**Quando usar**: Criar/modificar templates, melhorar UI, adicionar interatividade frontend

---

### 3. [API/DRF Developer](03-api-drf-developer.md)
**Especialista em**: Django REST Framework, Serializers, ViewSets, Permissions
**Stack**: DRF 3.17.0, Django 6.0.3, REST APIs
**Responsável por**:
- Desenvolvimento de endpoints REST
- Serializers e validações
- ViewSets e Routers
- Permissões e autenticação
- Documentação de API

**Quando usar**: Criar endpoints REST, implementar validações de API, trabalhar com JSON responses

---

### 4. [QA & Test Engineer](04-qa-test-engineer.md)
**Especialista em**: Django Tests, pytest, Coverage, Debugging
**Stack**: Django TestCase, unittest, pytest, Coverage.py
**Responsável por**:
- Escrever testes unitários
- Testes de integração
- Encontrar bugs e edge cases
- Validar funcionalidades
- Relatórios de qualidade

**Quando usar**: Implementar testes, validar funcionalidades, encontrar bugs, garantir qualidade

---

### 5. [Security & Permissions Reviewer](05-security-permissions-reviewer.md)
**Especialista em**: Autenticação, Autorização, OWASP, Segurança Django
**Stack**: Django Auth, Permissions, Token auth, HTTPS, CSRF
**Responsável por**:
- Revisar segurança de código
- Validar autenticação/autorização
- Permissões por tipo de usuário
- Proteção contra vulnerabilidades
- Conformidade com segurança

**Quando usar**: Revisar antes de deploy, implementar controle de acesso, auditar segurança

---

### 6. [Database & Performance Architect](06-database-performance-architect.md)
**Especialista em**: ORM Optimization, N+1 queries, Índices, Migrations
**Stack**: Django ORM, PostgreSQL, Query Optimization
**Responsável por**:
- Otimizar queries ORM
- Identificar e resolver N+1 queries
- Design de índices
- Performance de migrations
- Escalabilidade

**Quando usar**: Melhorar performance, otimizar queries, preparar para produção

---

## 🚀 Como Usar Este Framework

### Workflow Típico

1. **Planejamento** → Descrever o que precisa ser feito
2. **Desenvolvimento** → Chamar agente especializado apropriado
3. **Testes** → QA & Test Engineer valida a implementação
4. **Segurança** → Security Reviewer audita antes de merge
5. **Performance** → Database Architect otimiza se necessário
6. **Merge** → Code está pronto para produção

### Exemplo de Uso

```
Tarefa: "Adicionar modelo de Avaliação e criar endpoint REST"

1. Backend Developer → Cria modelo Avaliacao com validações
2. API Developer → Implementa Serializer e ViewSet
3. QA Engineer → Escreve testes para modelo e endpoint
4. Security Reviewer → Valida permissões e autenticação
5. Merge → Código pronto
```

---

## 🔄 Comunicação Entre Agentes

Os agentes devem trabalhar em **sequência lógica**:

```
Backend Developer
    ↓ (Models criados)
API Developer
    ↓ (Endpoints implementados)
Frontend Developer
    ↓ (Templates criados)
QA Engineer
    ↓ (Bugs encontrados? → volta para Dev)
Security Reviewer
    ↓ (Vulnerabilidades? → volta para Dev)
Database Architect
    ↓ (Otimizações)
MERGE ✅
```

---

## 📚 Stack do Projeto

- **Backend**: Django 6.0.3, Python 3.x
- **API**: Django REST Framework 3.17.0
- **Frontend**: Django Template Language, Tailwind CSS 4.x
- **Database**: SQLite (dev), PostgreSQL (prod)
- **Testing**: Django TestCase, unittest
- **Auth**: Django Auth customizado (Usuario model)

---

## 🛠️ Comandos Úteis (Todos Agentes)

```bash
# Ambiente
source venv/bin/activate              # Ativar venv
pip install -r requirements.txt       # Instalar deps

# Database
python manage.py makemigrations        # Gerar migrations
python manage.py migrate               # Aplicar migrations
python manage.py shell                 # Shell interativa

# Testes
python manage.py test                  # Rodar todos testes
python manage.py test app_name         # Testes de uma app

# Desenvolvimento
python manage.py runserver             # Servidor de dev
python manage.py createsuperuser       # Criar admin

# CSS
python manage.py tailwind build        # Build Tailwind
python manage.py tailwind start        # Watch mode
```

---

## 📖 Referências

- **Documentação do Projeto**: `/docs/README.md`
- **CLAUDE.md**: Guia para Claude Code neste repo
- **requirements.txt**: Dependências do projeto
- **PRD.md**: Product Requirements (vazio no momento)

---

## ⚡ Checklist Antes de Chamar um Agente

Tenha claro:
- [ ] Qual é o objetivo específico?
- [ ] Qual app/feature está envolvida?
- [ ] Qual agente é mais apropriado?
- [ ] Existem constraints ou padrões a seguir?
- [ ] Quais dependências (modelos, endpoints) já existem?

---

**Última atualização**: Março 2025

---

## 📞 Contatos Rápidos

Quando precisar de:
- **Modelo Django** → Backend Developer
- **Template/UI** → Frontend Developer
- **Endpoint REST** → API Developer
- **Testes** → QA Engineer
- **Segurança** → Security Reviewer
- **Performance** → Database Architect
