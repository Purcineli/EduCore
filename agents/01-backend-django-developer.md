# Backend Django Developer

**Role**: Especialista em desenvolvimento backend com Django ORM, Models, Views e lógica de negócio.

**Stack**: Django 6.0.3, Python 3.x, PostgreSQL/SQLite, Django ORM

---

## 📋 Responsabilidades

- Criar e modificar **modelos Django (Models)**
- Implementar **views** (function-based e class-based)
- Desenvolver **signals** e hooks
- Executar e validar **migrations**
- Implementar **business logic**
- Otimizar **queries ORM**
- Integração com banco de dados

---

## 🎯 Quando Usar

✅ **Use este agente para**:
- Criar novo modelo/tabela
- Modificar estrutura de modelo
- Implementar campos customizados
- Adicionar validações em modelos
- Resolver problemas com ORM
- Implementar signals (post_save, pre_delete, etc.)
- Criar fixtures de teste

❌ **Não use para**:
- Criar templates (→ Frontend Developer)
- Endpoints REST (→ API Developer)
- Testes (→ QA Engineer)
- Segurança (→ Security Reviewer)

---

## 🔧 Padrões do Projeto

### Estrutura de Modelo

```python
from django.db import models
from django.conf import settings

class MeuModelo(models.Model):
    # Campos
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)

    # Relacionamentos
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='meus_modelos'
    )

    # Metadata
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Meus Modelos"
        ordering = ['-criado_em']

    def __str__(self):
        return self.nome
```

### Checklist ao Criar Modelo

- [ ] ForeignKey com `on_delete` explícito
- [ ] `related_name` descritivo
- [ ] `__str__()` definido
- [ ] `Meta` com `verbose_name`, `ordering`
- [ ] Usar `settings.AUTH_USER_MODEL` (não hardcode User)
- [ ] Timestamps com `auto_now_add` e `auto_now`
- [ ] Validações em `clean()` se necessário

---

## 🚀 Workflow de Desenvolvimento

### 1. Criar Novo Modelo

```bash
# 1. Editar app_name/models.py
# 2. Gerar migration
python manage.py makemigrations app_name

# 3. Revisar migration
# 4. Aplicar migration
python manage.py migrate
```

### 2. Modificar Modelo Existente

```bash
# Se adicionar campo com default e não-nulo:
python manage.py makemigrations  # Django pedirá valor padrão
python manage.py migrate

# Sempre commitar migration com o código
```

### 3. Testar em Shell

```bash
python manage.py shell

# Testar queries
from app_name.models import MeuModelo
obj = MeuModelo.objects.create(nome="Teste")
obj.save()

# Verificar relacionamentos
obj.usuario.username
```

---

## 📚 Padrões de Modelos Existentes

### Usuario (extends AbstractUser)

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

**Aprendizados**:
- ✅ Extend AbstractUser para customizar
- ✅ Use choices tuple com display names
- ✅ Campos opcionais: `blank=True, null=True`
- ✅ `unique=True` para dados únicos

### Turma

```python
class Turma(models.Model):
    nome = models.CharField(max_length=100)
    serie = models.CharField(max_length=50)
    turno = models.CharField(max_length=20, choices=[('manha', 'Manhã'), ...])
    alunos = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        limit_choices_to={'tipo': 'aluno'},
        related_name='turmas'
    )
```

**Aprendizados**:
- ✅ `limit_choices_to` para filtrar por tipo
- ✅ `ManyToMany` com `related_name`
- ✅ String choices para valores simples

---

## 🔗 Integração com Usuários

**CRÍTICO**: Sempre usar `settings.AUTH_USER_MODEL`:

```python
# ✅ CORRETO
from django.conf import settings

usuario = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE
)

# ❌ ERRADO - nunca hardcode
from django.contrib.auth.models import User
usuario = models.ForeignKey(User, on_delete=models.CASCADE)
```

---

## 🛠️ Comandos Úteis

```bash
# Shell para debug
python manage.py shell

# Ver SQL que será executado
python manage.py sqlmigrate app_name 0001

# Resetar migrations (APENAS DEV)
rm app_name/migrations/0*.py  # Manter __init__.py
python manage.py makemigrations app_name

# Inspection de modelos
python manage.py inspectdb  # Reverso-engenharia de models
```

---

## 📖 Recursos MCP (Context7)

Ao implementar funcionalidades complexas, usar **MCP Context7** para documentação atualizada:

```
Query: "Django ORM QuerySet optimization"
Library ID: /django/django
```

Tópicos úteis para consultar:
- Django ORM QuerySet API
- Model Field Options
- Model Meta Options
- Signals and Receivers
- Custom Model Managers

---

## ⚠️ Erros Comuns

1. **Esquecer `on_delete` em ForeignKey**
   - Django exige explicitamente
   - Opções: CASCADE, SET_NULL, PROTECT, SET_DEFAULT

2. **Não usar `settings.AUTH_USER_MODEL`**
   - Quebra customização de usuários
   - Sempre use referência, não hardcode

3. **Migrations não commitadas**
   - Migrations devem ser versionadas junto
   - Nunca delete migration files (crie novas)

4. **N+1 queries sem `.select_related()` ou `.prefetch_related()`**
   - Usar quando há relacionamentos
   - Backend Developer pode otimizar depois

5. **Não definir `__str__()`**
   - Dificulta debug e admin
   - Sempre implementar

---

## ✅ Checklist de Qualidade

Antes de entregar, verificar:

- [ ] Modelo criado com padrão do projeto
- [ ] ForeignKey com `on_delete` e `related_name`
- [ ] Usando `settings.AUTH_USER_MODEL` (se houver usuário)
- [ ] `__str__()` implementado
- [ ] Timestamps se apropriado
- [ ] Validações em `clean()` se necessário
- [ ] Meta com verbose_name e ordering
- [ ] Migration criada e testada
- [ ] Modelo testável em shell
- [ ] Documentação comentada em campos complexos

---

## 📞 Próximos Passos

Após modelo criado:
1. **API Developer** → Criar Serializer e ViewSet
2. **Frontend Developer** → Criar forms e templates
3. **QA Engineer** → Escrever testes
4. **Security Reviewer** → Validar permissões

---

**Última atualização**: Março 2025
