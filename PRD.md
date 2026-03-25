# Product Requirements Document (PRD) - EduCore

## 1. Visão Geral

O EduCore é um sistema de gestão escolar web desenvolvido de forma enxuta (sem *over-engineering*) utilizando Python e Django Full-Stack. A interface visual é renderizada no servidor via Django Template Language + TailwindCSS, entregando uma experiência de usuário harmoniosa, limpa e responsiva. Banco de dados: SQLite.

---

## 2. Sobre o Produto

O sistema unifica as operações de uma instituição de ensino. Oferece uma **Landing Page** pública institucional e uma **área logada** segmentada para quatro perfis: Alunos, Professores, Pais/Responsáveis e Coordenadores.

A plataforma abrange:
- Gestão de identidade (autenticação por e-mail, grupos de perfil)
- Administração acadêmica (turmas, disciplinas, horários, presenças, notas)
- Vínculo Pai-Aluno (pais acompanham o progresso dos filhos)
- Comunicação interna (murais segmentados por grupo + mensagens diretas)

---

## 3. Público-Alvo

| Perfil (Group)    | Acesso                                                                 |
|-------------------|------------------------------------------------------------------------|
| **Students**      | Notas, boletim, presença, horários, murais, mensagens                  |
| **Teachers**      | Planos de aula, lançamento de presenças/notas, mensagens               |
| **Parents**       | Progresso acadêmico dos **seus filhos** vinculados, murais, mensagens  |
| **Coordinators**  | Gestão global: turmas, matrículas, relatórios, murais, usuários        |

---

## 4. Objetivos

- Arquitetura modular com Django apps isolados.
- Autenticação via **e-mail** (sem username).
- Internacionalização nativa: PT-BR, EN, RU (100% da UI).
- Design system minimalista, responsivo e consistente.
- **Rastreabilidade total** via campo `historical` (JSONField) em todos os modelos.
- **Vínculo Pai→Aluno** explícito no banco, com visibilidade isolada por filho.

---

## 5. Requisitos Funcionais

| ID    | Requisito                                                                                           |
|-------|-----------------------------------------------------------------------------------------------------|
| RF01  | Autenticação via `email` + senha.                                                                   |
| RF02  | Perfis via *Django Groups* (`Students`, `Teachers`, `Parents`, `Coordinators`).                     |
| RF03  | Internacionalização completa da UI (PT-BR, EN, RU).                                                 |
| RF04  | Landing page pública.                                                                               |
| RF05  | Dashboard dinâmico por perfil.                                                                      |
| RF06  | Todos os models herdam `BaseModel` (`created_at`, `updated_at`, `historical`).                      |
| RF07  | Módulo Acadêmico: Turmas, Disciplinas, Planos de Aula, Presenças, Notas.                            |
| RF08  | Módulo de Comunicação: Murais segmentados + Mensagens diretas.                                      |
| RF09  | **Vínculo Guardian**: Pai/Responsável vinculado ao(s) aluno(s). Pais veem apenas seus filhos.       |
| RF10  | **Ano Letivo (AcademicYear)**: Cursos e matrículas associados a um ano letivo ativo.                |
| RF11  | **Horário (Schedule)**: Grade horária semanal por disciplina (dia + hora).                          |
| RF12  | **Boletim (ReportCard)**: Consolidado de notas e frequência do aluno por ano letivo.                |

### Flowchart de UX

```
Acesso → Landing Page → Login (email/senha)
                              ↓
              ┌───────────────┴────────────────┐
              ↓               ↓                ↓                 ↓
    Dashboard Coord    Dashboard Teacher  Dashboard Student  Dashboard Parent
         ↓                   ↓                 ↓                  ↓
  Gerenciar Turmas    Planos de Aula      Ver Boletim       Ver filhos vinculados
  Matrículas          Lançar Presenças    Ver Presenças     Notas dos filhos
  Relatórios          Lançar Notas        Ver Horários      Murais segmentados
  Murais Globais      Mensagens           Mensagens         Mensagens
```

---

## 6. Requisitos Não-Funcionais

| ID    | Requisito                                                                                  |
|-------|--------------------------------------------------------------------------------------------|
| RNF01 | Código 100% em **Inglês** (variáveis, classes, métodos, comentários).                      |
| RNF02 | PEP8 estrito, aspas simples `'` sempre.                                                    |
| RNF03 | Exclusivamente **CBVs** (Class-Based Views).                                               |
| RNF04 | Signals obrigatoriamente em `signals.py` de cada app, registrados no `apps.py`.            |
| RNF05 | Sem dependências pesadas de frontend (somente DTL + TailwindCSS compilado).                |
| RNF06 | Banco de dados: SQLite (`db.sqlite3`).                                                     |
| RNF07 | `settings.AUTH_USER_MODEL` sempre (nunca hardcode `User`).                                 |

---

## 7. Arquitetura Técnica

**Stack:**
- Python 3.12+, Django 6.0.3
- TailwindCSS 3+ via PostCSS (compilado, sem CDN)
- SQLite

### Diagrama de Entidades (ER)

```
BaseModel (abstract)
  └── created_at, updated_at, historical

usuarios app
  ├── User (AbstractBaseUser + PermissionsMixin + BaseModel)
  │     email (UK), first_name, last_name, is_active, is_staff
  │     Groups: Students | Teachers | Parents | Coordinators
  │
  └── Guardian (BaseModel)          ← NOVO: vínculo Pai → Aluno
        parent  → FK User (Parents group)
        student → FK User (Students group)
        relationship_type: father | mother | guardian | other

academico app
  ├── AcademicYear (BaseModel)      ← NOVO: ano letivo
  │     year (unique int), start_date, end_date, is_active
  │
  ├── Course (BaseModel)            ← Turma
  │     name, shift, academic_year → FK AcademicYear
  │     coordinator → FK User (Coordinators)
  │
  ├── Subject (BaseModel)           ← Disciplina
  │     name, workload_hours
  │     course → FK Course
  │     teacher → FK User (Teachers)
  │
  ├── Schedule (BaseModel)          ← NOVO: horário semanal
  │     subject → FK Subject
  │     weekday: mon|tue|wed|thu|fri
  │     start_time, end_time
  │
  ├── Enrollment (BaseModel)        ← Matrícula
  │     student → FK User (Students)
  │     course  → FK Course
  │     enrolled_at, is_active
  │     unique_together: (student, course)
  │
  ├── LessonPlan (BaseModel)        ← Plano de Aula
  │     title, content, lesson_date
  │     teacher  → FK User (Teachers)
  │     subject  → FK Subject
  │
  ├── Attendance (BaseModel)        ← Presença
  │     student     → FK User (Students)
  │     lesson_plan → FK LessonPlan
  │     is_present (bool)
  │     unique_together: (student, lesson_plan)
  │
  └── Grade (BaseModel)             ← Nota
        student  → FK User (Students)
        subject  → FK Subject
        academic_year → FK AcademicYear  ← NOVO
        value (decimal 0–10)
        term: 1|2|3|4
        grade_type: exam|assignment|project|participation
        unique_together: (student, subject, term, grade_type)

comunicacao app
  ├── NoticeBoard (BaseModel)       ← Mural de Avisos
  │     title, content, author → FK User
  │     target_groups → M2M django Group  ← público segmentado
  │     is_published (bool), published_at
  │
  └── Message (BaseModel)           ← Mensagem Direta
        sender   → FK User (related_name='sent_messages')
        receiver → FK User (related_name='received_messages')
        subject, body
        is_read (bool), read_at (DateTimeField null)

institucional app
  └── (sem models — apenas views/templates públicos)
```

### Relacionamentos-Chave

1. **Parent vê filhos**: `Guardian.objects.filter(parent=request.user)` → lista de `student`s vinculados.
2. **Parent vê notas do filho**: `Grade.objects.filter(student__in=children)`.
3. **Parent vê presença do filho**: `Attendance.objects.filter(student__in=children)`.
4. **Mural segmentado**: `NoticeBoard.objects.filter(target_groups__in=request.user.groups.all())`.
5. **Dashboard Teacher**: lista `Subject.objects.filter(teacher=request.user)` → turmas + alunos matriculados.
6. **Boletim do Aluno**: agrupa `Grade` por `subject__name` e `term` → tabela de notas consolidada.

---

## 8. Design System

| Elemento         | Classes Tailwind                                                                 |
|------------------|----------------------------------------------------------------------------------|
| Fundo global     | `bg-slate-50`                                                                    |
| Cards            | `bg-white rounded-lg shadow-sm border border-slate-100 p-6`                     |
| Botão primário   | `px-4 py-2 rounded-md bg-gradient-to-r from-blue-600 to-indigo-600 text-white hover:from-blue-700 hover:to-indigo-700 transition-all shadow-sm` |
| Botão secundário | `px-4 py-2 rounded-md border border-slate-300 bg-white text-slate-700 hover:bg-slate-50 transition-colors` |
| Inputs/Forms     | `w-full rounded-md border border-slate-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm px-3 py-2` |
| Navbar           | `bg-white border-b border-slate-200 shadow-sm`                                  |
| Footer           | `bg-white border-t border-slate-200 text-slate-500 text-sm`                    |
| Texto primário   | `text-slate-800 font-sans`                                                      |
| Texto secundário | `text-slate-500`                                                                 |
| Brand logo       | `bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent`   |

---

## 9. User Stories

### Épico 1: Identidade e Acesso
- **US01**: Como usuário, quero fazer login com email/senha para acessar meu dashboard de perfil.
- **US02**: Como coordenador, quero vincular um pai a um aluno para que o responsável acompanhe o progresso do filho.

### Épico 2: Gestão Acadêmica
- **US03**: Como professor, quero lançar presença para cada aula do meu plano para registrar frequência.
- **US04**: Como professor, quero lançar notas por bimestre e tipo de avaliação para documentar o progresso.
- **US05**: Como aluno, quero ver meu boletim consolidado com notas e frequência por disciplina.
- **US06**: Como coordenador, quero ver a grade horária de cada turma para gerenciar o calendário.

### Épico 3: Vínculo Pai-Aluno
- **US07**: Como pai, quero ver as notas e presença do meu filho para acompanhar seu desempenho sem precisar ir à escola.
- **US08**: Como coordenador, quero vincular múltiplos responsáveis a um aluno (pai e mãe separados, por exemplo).

### Épico 4: Comunicação
- **US09**: Como coordenador, quero publicar um aviso no mural direcionado apenas a "Parents" para comunicação focada.
- **US10**: Como professor, quero enviar mensagem direta a um aluno ou pai para tratar assuntos individuais.

---

## 10. Métricas de Sucesso

- Login via email: 100% dos usuários autenticando sem friction.
- Boletim: Pai consegue ver notas do filho em ≤ 2 cliques após login.
- Performance: Dashboard carrega em < 1.5s.
- I18n: Zero chaves não traduzidas na interface.
- Auditoria: 100% das alterações registradas no campo `historical`.
