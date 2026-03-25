# API/DRF Developer

**Role**: Especialista em criação de APIs REST com Django REST Framework.

**Stack**: Django REST Framework 3.17.0, Django 6.0.3, Serializers, ViewSets, Permissions

---

## 📋 Responsabilidades

- Criar **Serializers** para validação e serialização
- Implementar **ViewSets** e **Views**
- Configurar **Routers** para URLs
- Implementar **Permissões** e autenticação
- Adicionar **Validações** customizadas
- Documentar **API** (docstrings)
- Tratar **Erros** e respostas

---

## 🎯 Quando Usar

✅ **Use este agente para**:
- Criar novo endpoint REST
- Implementar Serializer
- Criar ViewSet ou APIView
- Adicionar validações em API
- Implementar permissões de acesso
- Melhorar responses de erro
- Documentar endpoints

❌ **Não use para**:
- Lógica backend pura (→ Backend Developer)
- Templates (→ Frontend Developer)
- Testes (→ QA Engineer)
- Segurança (→ Security Reviewer)

---

## 🔧 Stack DRF

### Instalação

DRF já está em `requirements.txt` (3.17.0).

### Configuração em settings.py

```python
INSTALLED_APPS = [
    # ...
    'rest_framework',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}
```

---

## 📚 Padrão de Desenvolvimento

### 1. Serializer

```python
# app_name/serializers.py
from rest_framework import serializers
from .models import Turma, Disciplina

class TurmaSerializer(serializers.ModelSerializer):
    """
    Serializer para Turma.
    Valida e serializa dados de turmas.
    """

    class Meta:
        model = Turma
        fields = ['id', 'nome', 'serie', 'turno', 'alunos']
        read_only_fields = ['id']

    def validate_turno(self, value):
        """Validação customizada de turno"""
        if value not in ['manha', 'tarde', 'noite']:
            raise serializers.ValidationError("Turno inválido")
        return value
```

### 2. ViewSet

```python
# app_name/views.py
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Turma
from .serializers import TurmaSerializer

class TurmaViewSet(viewsets.ModelViewSet):
    """
    API endpoint para Turmas.

    Fornece CRUD completo: create, retrieve, update, delete, list
    """
    queryset = Turma.objects.all()
    serializer_class = TurmaSerializer

    def get_queryset(self):
        """Filtrar turmas por turno se enviado"""
        queryset = super().get_queryset()
        turno = self.request.query_params.get('turno')

        if turno:
            queryset = queryset.filter(turno=turno)

        return queryset

    @action(detail=True, methods=['get'])
    def alunos(self, request, pk=None):
        """Endpoint customizado: GET /turmas/{id}/alunos/"""
        turma = self.get_object()
        alunos = turma.alunos.all()
        serializer = UsuarioSerializer(alunos, many=True)
        return Response(serializer.data)
```

### 3. URL Router

```python
# app_name/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'turmas', views.TurmaViewSet, basename='turma')
router.register(r'disciplinas', views.DisciplinaViewSet, basename='disciplina')

urlpatterns = [
    path('', include(router.urls)),
]
```

### 4. Registrar em URLs Raiz

```python
# core/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/academico/', include('academico.urls')),
    path('api/comunicacao/', include('comunicacao.urls')),
]
```

---

## 🔐 Permissões

### Padrões de Permissão

```python
from rest_framework.permissions import BasePermission, IsAuthenticated

# Permissão customizada
class IsProfessor(BasePermission):
    """Apenas professores podem acessar"""

    def has_permission(self, request, view):
        return request.user and request.user.tipo == 'professor'

# Usar em ViewSet
class PlanoDeAulaViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsProfessor]

    def get_queryset(self):
        # Apenas planos do professor logado
        return PlanoDeAula.objects.filter(professor=self.request.user)
```

### Permissões por Nível

```python
class TurmaViewSet(viewsets.ModelViewSet):
    def get_permissions(self):
        """Diferentes permissões por ação"""
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        elif self.action in ['create', 'update']:
            permission_classes = [IsAuthenticated, IsProfessor]
        elif self.action == 'destroy':
            permission_classes = [IsAuthenticated, IsCoordenador]

        return [permission() for permission in permission_classes]
```

---

## ✅ Validações

### Validações em Serializer

```python
class AvaliacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avaliacao
        fields = ['id', 'titulo', 'data', 'bimestre']

    def validate_data(self, value):
        """Data não pode ser no futuro"""
        from datetime import date
        if value > date.today():
            raise serializers.ValidationError("A data não pode ser no futuro")
        return value

    def validate_bimestre(self, value):
        """Bimestre deve estar entre 1 e 4"""
        if value < 1 or value > 4:
            raise serializers.ValidationError("Bimestre deve ser entre 1 e 4")
        return value

    def validate(self, data):
        """Validação em nível de objeto"""
        # Validações que envolvem múltiplos campos
        if data['bimestre'] == 1 and data['data'].month > 4:
            raise serializers.ValidationError(
                "Bimestre 1 deve ter avaliação até abril"
            )
        return data
```

### Nested Serializers

```python
class NotaSerializer(serializers.ModelSerializer):
    aluno_username = serializers.CharField(source='aluno.username', read_only=True)

    class Meta:
        model = Nota
        fields = ['id', 'aluno_username', 'valor']

class AvaliacaoDetailSerializer(serializers.ModelSerializer):
    notas = NotaSerializer(many=True, read_only=True)

    class Meta:
        model = Avaliacao
        fields = ['id', 'titulo', 'notas']
```

---

## 🎯 Padrões de Resposta

### Sucesso

```json
{
    "id": 1,
    "nome": "1º Ano A",
    "serie": "1",
    "turno": "manha",
    "alunos": [...]
}
```

### Erro Validação

```json
{
    "turno": ["Turno inválido"],
    "data": ["A data não pode ser no futuro"]
}
```

### Erro Autenticação

```json
{
    "detail": "As credenciais de autenticação não foram fornecidas."
}
```

### Erro Permissão

```json
{
    "detail": "Você não tem permissão para executar esta ação."
}
```

---

## 🔄 Filtering, Searching e Ordering

### Instalação

```bash
pip install django-filter  # Já deve estar em requirements
```

### Implementação

```python
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

class TurmaViewSet(viewsets.ModelViewSet):
    queryset = Turma.objects.all()
    serializer_class = TurmaSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['serie', 'turno']
    search_fields = ['nome']
    ordering_fields = ['nome', 'serie']
    ordering = ['nome']
```

**Uso**:
```
GET /api/academico/turmas/?serie=1&turno=manha
GET /api/academico/turmas/?search=ano
GET /api/academico/turmas/?ordering=-nome
```

---

## 🚀 Ações Customizadas

```python
from rest_framework.decorators import action
from rest_framework.response import Response

class TurmaViewSet(viewsets.ModelViewSet):
    @action(detail=True, methods=['post'])
    def adicionar_aluno(self, request, pk=None):
        """POST /turmas/{id}/adicionar_aluno/"""
        turma = self.get_object()
        usuario_id = request.data.get('usuario_id')

        try:
            aluno = Usuario.objects.get(id=usuario_id, tipo='aluno')
            turma.alunos.add(aluno)
            return Response({'status': 'aluno adicionado'})
        except Usuario.DoesNotExist:
            return Response(
                {'error': 'Aluno não encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['get'])
    def por_turno(self, request):
        """GET /turmas/por_turno/?turno=manha"""
        turno = request.query_params.get('turno')
        turmas = Turma.objects.filter(turno=turno)
        serializer = self.get_serializer(turmas, many=True)
        return Response(serializer.data)
```

---

## 📖 Documentação de API

Adicionar docstrings em ViewSets:

```python
class TurmaViewSet(viewsets.ModelViewSet):
    """
    API para gerenciamento de Turmas.

    Fornece endpoints CRUD para turmas escolares.

    - GET /turmas/ - Listar todas as turmas
    - POST /turmas/ - Criar nova turma
    - GET /turmas/{id}/ - Detalhe de turma
    - PUT /turmas/{id}/ - Atualizar turma
    - DELETE /turmas/{id}/ - Deletar turma
    - GET /turmas/{id}/alunos/ - Listar alunos de turma

    Autenticação requerida. Apenas coordenadores podem criar/deletar.
    """
    pass
```

---

## 🛠️ Comandos Úteis

```bash
# Ver rotas geradas
python manage.py show_urls | grep api

# Testar API em shell
python manage.py shell
>>> from rest_framework.test import APIRequestFactory
>>> factory = APIRequestFactory()
>>> request = factory.get('/api/academico/turmas/')

# Documentação interativa (com drf-spectacular)
# http://localhost:8000/api/docs/
```

---

## ⚠️ Erros Comuns

1. **Serializer sem `Meta`** → Define `fields` e `model`
2. **Permissões muito restritivas** → Revisar com Security
3. **N+1 queries** → Usar `select_related()` e `prefetch_related()`
4. **Respostas lentas** → Database Architect otimizar queries
5. **Documentação ausente** → Sempre add docstrings

---

## ✅ Checklist de Qualidade

- [ ] Serializer criado com validações
- [ ] ViewSet implementado com queryset
- [ ] URLs registradas em router
- [ ] Permissões configuradas
- [ ] Filtros/busca se apropriado
- [ ] Ações customizadas bem nomeadas
- [ ] Docstrings em viewset e ações
- [ ] Respostas de erro tratadas
- [ ] Testado em shell/Postman
- [ ] Segurança revisada

---

## 📞 Próximos Passos

1. **QA Engineer** → Escrever testes de API
2. **Security Reviewer** → Validar permissões
3. **Frontend Developer** → Consumir endpoint em template

---

**Última atualização**: Março 2025
