# Database & Performance Architect

**Role**: Especialista em otimização de queries ORM, índices e performance de banco de dados.

**Stack**: Django ORM, PostgreSQL, Query Optimization, Indexes

---

## 📋 Responsabilidades

- Otimizar **queries ORM**
- Identificar e resolver **N+1 queries**
- Projetar **índices** de banco de dados
- Analisar **planos de execução**
- Melhorar **performance** de migration
- Validar **escalabilidade**
- Relatórios de **performance**

---

## 🎯 Quando Usar

✅ **Use este agente para**:
- Endpoint está lento (> 1 segundo)
- Encontrar N+1 queries
- Criar índices em campos
- Otimizar migrations
- Analizar plano de query
- Melhorar escalabilidade

❌ **Não use para**:
- Criar features (→ Backend Developer)
- Escrever testes (→ QA Engineer)
- Segurança (→ Security Reviewer)

---

## 🔍 Identificar N+1 Queries

### Problema Clássico

```python
# ❌ N+1 QUERY - LENTO
def listar_turmas(request):
    turmas = Turma.objects.all()  # 1 query

    for turma in turmas:  # N queries (uma por turma)
        print(turma.alunos.count())

    # Total: 1 + N queries
```

### Solução com select_related()

```python
# ✅ select_related() - RÁPIDO
def listar_turmas(request):
    # Para ForeignKey e OneToOne
    turmas = Turma.objects.select_related('criado_por')

    for turma in turmas:
        print(turma.criado_por.username)

    # Total: 1 query com JOIN
```

### Solução com prefetch_related()

```python
# ✅ prefetch_related() - RÁPIDO
def listar_turmas(request):
    # Para ManyToMany e reverse relations
    turmas = Turma.objects.prefetch_related('alunos')

    for turma in turmas:
        print(turma.alunos.all())  # Não dispara mais queries

    # Total: 2 queries (1 turmas + 1 alunos)
```

### Exemplo Real

```python
# ❌ LENTO - 1 + N + M queries
class TurmaListView(viewsets.ReadOnlyModelViewSet):
    queryset = Turma.objects.all()
    serializer_class = TurmaSerializer

    # Ao serializar, acessa:
    # - turma.alunos (N queries)
    # - aluno.usuario (N*M queries)

# ✅ RÁPIDO - 2 queries
class TurmaListView(viewsets.ReadOnlyModelViewSet):
    def get_queryset(self):
        return Turma.objects.prefetch_related(
            'alunos__usuario'  # Prefetch nested
        )

    serializer_class = TurmaSerializer
```

---

## 📊 Analisar Query Performance

### Método 1: Django Debug Toolbar

```bash
pip install django-debug-toolbar
```

```python
# settings.py
INSTALLED_APPS = [
    'debug_toolbar',
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

INTERNAL_IPS = ['127.0.0.1']
```

**Visualizar em localhost**: barra lateral com queries, SQL, etc.

### Método 2: Print SQL

```python
from django.db import connection
from django.test.utils import CaptureQueriesContext

def minha_view(request):
    with CaptureQueriesContext(connection) as ctx:
        turmas = Turma.objects.all()
        for turma in turmas:
            print(turma.alunos.count())  # N+1 aqui

    print(f"Total queries: {len(ctx.captured_queries)}")
    for q in ctx.captured_queries:
        print(q['sql'])
```

### Método 3: Django Shell

```bash
python manage.py shell

>>> from django.db import connection
>>> from django.test.utils import CaptureQueriesContext

>>> connection.queries_log.clear()
>>> turmas = Turma.objects.all()
>>> for turma in turmas:
...     print(turma.alunos.count())

>>> from django.db import connection
>>> print(f"Queries: {len(connection.queries)}")
>>> for q in connection.queries:
...     print(q['sql'])
```

---

## 🚀 Otimizações Comuns

### 1. select_related() para ForeignKey

```python
# ❌ 2 queries
turmas = Turma.objects.all()
for turma in turmas:
    print(turma.professor.username)  # Query por turma

# ✅ 1 query com JOIN
turmas = Turma.objects.select_related('professor')
```

### 2. prefetch_related() para ManyToMany

```python
# ❌ N queries
turmas = Turma.objects.all()
for turma in turmas:
    alunos = turma.alunos.all()  # Query por turma

# ✅ 2 queries (prefetch)
turmas = Turma.objects.prefetch_related('alunos')
```

### 3. only() e defer() para campos

```python
# ✅ Carregar apenas alguns campos
turmas = Turma.objects.only('id', 'nome', 'serie')

# ✅ Excluir campos grandes
turmas = Turma.objects.defer('descricao_grande')
```

### 4. Annotations para agregações

```python
# ❌ Loop com count()
for turma in turmas:
    total = turma.alunos.count()  # Query por turma

# ✅ 1 query com agregação
from django.db.models import Count

turmas = Turma.objects.annotate(
    total_alunos=Count('alunos')
)
for turma in turmas:
    print(turma.total_alunos)  # Não dispara query
```

### 5. Filtering no banco (não em Python)

```python
# ❌ Carregar tudo, filtrar em Python
alunos = Usuario.objects.all()
alunos_ativos = [a for a in alunos if a.ativo]

# ✅ Filtrar no banco
alunos = Usuario.objects.filter(ativo=True)
```

---

## 📈 Índices de Banco de Dados

### Quando Criar Índice

- Campo frequentemente usado em WHERE
- Campo usado em ORDER BY
- Campo usado em JOIN (ForeignKey)
- Campo com muitos valores únicos

### Criar Índice via Migration

```bash
python manage.py makemigrations
```

```python
# migrations/0002_add_index.py
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('academico', '0001_initial'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='turma',
            index=models.Index(
                fields=['serie', 'turno'],
                name='turma_serie_turno_idx'
            ),
        ),
    ]
```

### db_index em Modelo

```python
class Turma(models.Model):
    nome = models.CharField(max_length=100, db_index=True)
    serie = models.CharField(max_length=50, db_index=True)
    turno = models.CharField(
        max_length=20,
        choices=[...],
        db_index=True  # Frequentemente filtrado
    )

    class Meta:
        indexes = [
            models.Index(fields=['serie', 'turno']),  # Índice composto
        ]
```

### Analizar Índices

```sql
-- PostgreSQL
SELECT schemaname, tablename, indexname FROM pg_indexes
WHERE tablename = 'academico_turma';

-- Ver índices não usados
SELECT * FROM pg_stat_user_indexes WHERE idx_scan = 0;
```

---

## 🧪 Testes de Performance

```python
from django.test import TestCase
from django.test.utils import CaptureQueriesContext
from django.db import connection

class PerformanceTestCase(TestCase):
    def test_turma_list_sem_n_plus_one(self):
        """Teste: listar turmas sem N+1 query"""
        # Criar dados
        for i in range(10):
            turma = Turma.objects.create(nome=f"Turma {i}", ...)
            for j in range(5):
                Usuario.objects.create(..., turmas=[turma])

        # Capturar queries
        with CaptureQueriesContext(connection) as ctx:
            turmas = Turma.objects.prefetch_related('alunos')
            for turma in turmas:
                list(turma.alunos.all())

        # Deve ser <= 2 queries (1 turma + 1 alunos)
        self.assertLessEqual(len(ctx.captured_queries), 2)
```

---

## 🔍 ViewSet Otimizado

```python
class TurmaViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TurmaSerializer

    def get_queryset(self):
        """Otimizado: prefetch, select_related, only"""
        queryset = Turma.objects.all()

        # Para list: apenas campos necessários
        if self.action == 'list':
            queryset = queryset.only(
                'id', 'nome', 'serie', 'turno'
            ).prefetch_related('alunos')

        # Para detail: dados completos
        elif self.action == 'retrieve':
            queryset = queryset.prefetch_related(
                'alunos',
                'horarios__professor',
                'horarios__disciplina'
            )

        return queryset
```

---

## 📊 Métricas de Performance

```python
import time

def performance_metric(view_func):
    def wrapper(*args, **kwargs):
        start = time.time()

        with CaptureQueriesContext(connection) as ctx:
            result = view_func(*args, **kwargs)

        elapsed = time.time() - start
        queries = len(ctx.captured_queries)

        print(f"Tempo: {elapsed:.2f}s, Queries: {queries}")
        return result

    return wrapper

@performance_metric
def listar_turmas():
    return Turma.objects.prefetch_related('alunos')
```

---

## ⚠️ Red Flags de Performance

- [ ] Loop com `.count()` ou `.all()` dentro
- [ ] Sem `select_related()` para ForeignKey
- [ ] Sem `prefetch_related()` para M2M
- [ ] Sem índices em campos filtrados
- [ ] Queries raw sem agregação
- [ ] `defer()` em poucos campos
- [ ] Sem caching (queryset reutilizado)

---

## 🎯 Checklist de Performance

Antes de deploy:

- [ ] Analisar queries com Debug Toolbar
- [ ] Nenhum N+1 query
- [ ] `select_related()` para FK
- [ ] `prefetch_related()` para M2M
- [ ] Índices em campos filtrados
- [ ] Teste de carga executado
- [ ] Tempo resposta < 500ms (lista)
- [ ] Tempo resposta < 200ms (detalhe)

---

## 🚀 Otimizações Avançadas

### Caching com Django Cache

```python
from django.core.cache import cache
from django.views.decorators.cache import cache_page

@cache_page(60)  # Cache por 60 segundos
def turma_list(request):
    return Turma.objects.prefetch_related('alunos')

# Ou manual
def get_turmas():
    key = 'turmas_list'
    turmas = cache.get(key)

    if turmas is None:
        turmas = Turma.objects.prefetch_related('alunos')
        cache.set(key, turmas, 60)

    return turmas
```

### Database Replication (Read-Only)

```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'principale',
    },
    'read_only': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'replica',
    }
}

# Usar no código
turmas = Turma.objects.using('read_only').all()  # Read from replica
```

---

## 📖 Recursos

- [Django Query Optimization](https://docs.djangoproject.com/en/6.0/topics/db/optimization/)
- [Database Access Optimization](https://docs.djangoproject.com/en/6.0/topics/db/optimization/)
- [Django Debug Toolbar](https://django-debug-toolbar.readthedocs.io/)

---

**Última atualização**: Março 2025
