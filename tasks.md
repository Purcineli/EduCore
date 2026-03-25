Sprint 1: Configuração Core e Autenticação Nativa (App: usuarios, core)
[x] Task 1.1: Preparação do ambiente e base de dados

[x] 1.1.1: Criar/Verificar venv e garantir Django instalado via requirements.txt.

[x] 1.1.2: Configurar core/settings.py para usar db.sqlite3.

[x] 1.1.3: Ajustar aspas duplas para simples (') no settings.py.

[x] Task 1.2: Modelagem Base (Auditoria)

[x] 1.2.1: Criar arquivo core/models.py.

[x] 1.2.2: Implementar classe abstrata BaseModel com campos created_at (auto_now_add), updated_at (auto_now) e historical (JSONField, default=dict).

[x] Task 1.3: Custom User Model (App usuarios)

[x] 1.3.1: Criar classe User herdando de AbstractBaseUser, PermissionsMixin e BaseModel.

[x] 1.3.2: Definir email como unique e USERNAME_FIELD = 'email'. Remover campo username.

[x] 1.3.3: Criar classe UserManager em usuarios/models.py herdando de BaseUserManager (sobrescrever create_user e create_superuser).

[x] 1.3.4: Alterar AUTH_USER_MODEL = 'usuarios.User' no settings.py.

[x] 1.3.5: Gerar a primeira migration inicial: python manage.py makemigrations usuarios.

[x] 1.3.6: Aplicar migration inicial do banco: python manage.py migrate.

[x] 1.3.7: Criar admin customizado UserAdmin em usuarios/admin.py.

[x] Task 1.4: Configuração I18n e L10n

[x] 1.4.1: Ativar USE_I18N = True no settings.py.

[x] 1.4.2: Configurar LANGUAGES = [('pt-br', 'Portuguese'), ('en', 'English'), ('ru', 'Russian')].

[x] 1.4.3: Criar pasta locale na raiz.

[x] 1.4.4: Adicionar middleware LocaleMiddleware no settings.py.

Sprint 2: Frontend Pipeline e Módulo Institucional (App: institucional)
[x] Task 2.1: Setup do Tailwind e DTL

[x] 2.1.1: Verificar EduCore/static_src/package.json possui dependência tailwindcss; garantir tailwind.config.js com content: ['../../**/*.html', '../../**/*.py'].

[x] 2.1.2: Verificar/criar EduCore/static_src/src/styles.css com @tailwind base/components/utilities.

[x] Task 2.2: Base Template e Design System

[x] 2.2.1: Criar EduCore/templates/base.html com estrutura HTML5 completa.

[x] 2.2.2: Importar CSS compilado via {% load static %} e {% static 'css/dist/styles.css' %}.

[x] 2.2.3: Navbar global: logo "EduCore" (gradiente brand), links Home/Dashboard/Login-Logout condicionais, responsivo (hamburger mobile).

[x] 2.2.4: Footer minimalista: "© 2025 EduCore. All rights reserved." em text-slate-500.

[x] 2.2.5: Incluir blocos {% block content %}, {% block extra_js %} e flash messages (django.contrib.messages).

[x] Task 2.3: Landing Page

[x] 2.3.1: Criar LandingPageView (TemplateView) em institucional/views.py.

[x] 2.3.2: Criar institucional/templates/institucional/landing.html:
         - Hero: gradiente bg-gradient-to-br from-blue-600 via-indigo-600 to-purple-700, h1 branco, subtítulo, CTA "Access Portal" → /login/.
         - Seção Features: 3 cards (Academic Management, Guardian Portal, Communication) com ícones SVG inline.
         - Seção Profiles: 4 perfis (Students, Teachers, Parents, Coordinators) com descrição e ícone.

[x] 2.3.3: Criar institucional/urls.py (app_name='institucional') e incluir no core/urls.py.

[x] Task 2.4: Login / Logout Flow

[x] 2.4.1: CustomLoginView (LoginView) em usuarios/views.py com template_name='usuarios/login.html' e redirect_authenticated_user=True.

[x] 2.4.2: Criar usuarios/templates/usuarios/login.html:
         - Centralizado min-h-screen flex items-center justify-center bg-slate-50.
         - Card branco max-w-md, campos Email e Password com classes Tailwind, botão gradiente.
         - Exibir erros genéricos (não revelar se é email ou senha).

[x] 2.4.3: CustomLogoutView (LogoutView) com next_page='institucional:home'.

[x] 2.4.4: Criar usuarios/urls.py (app_name='usuarios') com /login/ e /logout/.

[x] 2.4.5: Incluir usuarios.urls no core/urls.py.

Sprint 3: Vínculo Pai-Aluno e Gestão Acadêmica (Apps: usuarios, academico)
[ ] Task 3.1: Model Guardian (vínculo Pai → Aluno)

[ ] 3.1.1: Adicionar model Guardian em usuarios/models.py herdando BaseModel:
         - parent → FK settings.AUTH_USER_MODEL (related_name='guardianships', limit_choices_to={'groups__name': 'Parents'})
         - student → FK settings.AUTH_USER_MODEL (related_name='guardians', limit_choices_to={'groups__name': 'Students'})
         - relationship_type: choices father|mother|guardian|other
         - unique_together: (parent, student)

[ ] 3.1.2: Registrar Guardian no usuarios/admin.py com list_display e search.

[ ] 3.1.3: Gerar e aplicar migration: python manage.py makemigrations usuarios && migrate.

[ ] Task 3.2: Model AcademicYear

[ ] 3.2.1: Criar model AcademicYear em academico/models.py herdando BaseModel:
         - year: IntegerField(unique=True)
         - start_date, end_date: DateField
         - is_active: BooleanField(default=False)
         - Método classmethod get_active() retornando o ano letivo ativo.

[ ] Task 3.3: Models do núcleo acadêmico

[ ] 3.3.1: Criar model Course (Turma) herdando BaseModel:
         - name, shift (morning|afternoon|evening)
         - academic_year → FK AcademicYear (related_name='courses')
         - coordinator → FK AUTH_USER_MODEL (limit_choices_to Coordinators, null=True)

[ ] 3.3.2: Criar model Subject (Disciplina) herdando BaseModel:
         - name, workload_hours: IntegerField(default=40)
         - course → FK Course (related_name='subjects')
         - teacher → FK AUTH_USER_MODEL (limit_choices_to Teachers, null=True)

[ ] 3.3.3: Criar model Schedule (Horário Semanal) herdando BaseModel:
         - subject → FK Subject (related_name='schedules')
         - weekday: choices (mon|tue|wed|thu|fri)
         - start_time, end_time: TimeField

[ ] 3.3.4: Criar model Enrollment (Matrícula) herdando BaseModel:
         - student → FK AUTH_USER_MODEL (limit_choices_to Students)
         - course → FK Course
         - enrolled_at: DateField(auto_now_add=True)
         - is_active: BooleanField(default=True)
         - unique_together: (student, course)

[ ] 3.3.5: Criar model LessonPlan (Plano de Aula) herdando BaseModel:
         - title, content: TextField, lesson_date: DateField
         - teacher → FK AUTH_USER_MODEL (limit_choices_to Teachers)
         - subject → FK Subject (related_name='lesson_plans')

[ ] 3.3.6: Criar model Attendance (Presença) herdando BaseModel:
         - student → FK AUTH_USER_MODEL (limit_choices_to Students)
         - lesson_plan → FK LessonPlan (related_name='attendances')
         - is_present: BooleanField(default=False)
         - unique_together: (student, lesson_plan)

[ ] 3.3.7: Criar model Grade (Nota) herdando BaseModel:
         - student → FK AUTH_USER_MODEL (limit_choices_to Students)
         - subject → FK Subject (related_name='grades')
         - academic_year → FK AcademicYear
         - value: DecimalField(max_digits=5, decimal_places=2)
         - term: IntegerField choices 1–4
         - grade_type: choices exam|assignment|project|participation
         - unique_together: (student, subject, term, grade_type)

[ ] 3.3.8: Registrar todos os models no academico/admin.py.

[ ] 3.3.9: Gerar e aplicar migrations: makemigrations academico && migrate.

[ ] Task 3.4: Views e Templates do Dashboard Acadêmico

[ ] 3.4.1: Criar DashboardView (LoginRequiredMixin + TemplateView) em academico/views.py.
         Contexto por grupo:
         - Coordinators: total courses/enrollments/users, recent notices.
         - Teachers: seus subjects, últimos lesson_plans, alunos com falta.
         - Students: suas enrollments, grades por term, próximas aulas (schedule).
         - Parents: filhos vinculados (Guardian), para cada filho: enrollments + grades + attendance %.

[ ] 3.4.2: Criar academico/templates/academico/dashboard.html com Cards em grid-cols-1 md:grid-cols-3.
         - Cards de estatísticas no topo (bg-white rounded-lg shadow-sm).
         - Tabelas com listas de alunos/notas/presenças.
         - Seção especial para Parents: seletor de filho com tabs ou accordion.

[ ] Task 3.5: Views de CRUD Acadêmico

[ ] 3.5.1: CourseListView (LoginRequiredMixin + ListView) com paginação.

[ ] 3.5.2: GradeCreateView (LoginRequiredMixin + CreateView) com filtro de students by subject.

[ ] 3.5.3: AttendanceCreateView ou formset inline para lançamento em lote por LessonPlan.

[ ] 3.5.4: Criar academico/forms.py com GradeForm, AttendanceForm usando classes Tailwind nos widgets.

[ ] 3.5.5: Criar academico/urls.py (app_name='academico') e incluir no core/urls.py.

[ ] 3.5.6: Criar templates: academico/course_list.html, academico/grade_form.html.

Sprint 4: Comunicação, Signals e Internacionalização (App: comunicacao)
[ ] Task 4.1: Models de Comunicação

[ ] 4.1.1: Criar model NoticeBoard em comunicacao/models.py herdando BaseModel:
         - title, content: TextField
         - author → FK AUTH_USER_MODEL (related_name='notices')
         - target_groups → ManyToManyField('auth.Group', blank=True)
           (vazio = visível para todos os grupos logados)
         - is_published: BooleanField(default=False)
         - published_at: DateTimeField(null=True, blank=True)

[ ] 4.1.2: Criar model Message herdando BaseModel:
         - sender   → FK AUTH_USER_MODEL (related_name='sent_messages')
         - receiver → FK AUTH_USER_MODEL (related_name='received_messages')
         - subject: CharField(max_length=200)
         - body: TextField
         - is_read: BooleanField(default=False)
         - read_at: DateTimeField(null=True, blank=True)

[ ] 4.1.3: Registrar no comunicacao/admin.py com filtros por target_groups e is_published.

[ ] 4.1.4: Gerar e aplicar migrations: makemigrations comunicacao && migrate.

[ ] Task 4.2: Signals

[ ] 4.2.1: Criar comunicacao/signals.py com signal post_save no NoticeBoard:
         - Ao criar NoticeBoard, gravar no campo historical: {'event': 'created', 'author': email, 'timestamp': str(now)}.
         - Ao publicar (is_published muda para True), gravar: {'event': 'published', 'timestamp': str(now)}.

[ ] 4.2.2: Registrar signal no comunicacao/apps.py no método ready().

[ ] Task 4.3: Views e Templates de Comunicação

[ ] 4.3.1: NoticeBoardListView (LoginRequiredMixin + ListView):
         - Filtrar: NoticeBoard.objects.filter(is_published=True, target_groups__in=request.user.groups.all()) | filter(target_groups__isnull=True)
         - Ordenar por -published_at.

[ ] 4.3.2: MessageInboxView (LoginRequiredMixin + ListView):
         - Listar mensagens recebidas do usuário logado, ordenadas por -created_at.
         - Marcar como lida ao abrir (read_at=now).

[ ] 4.3.3: MessageCreateView (LoginRequiredMixin + CreateView):
         - Sender = request.user (setado no form_valid, não no form).
         - Receiver: select de usuários ativos.

[ ] 4.3.4: Criar template comunicacao/templates/comunicacao/noticeboard_list.html:
         - Layout "Feed/Timeline": cada aviso como card com border-l-4 border-blue-500.
         - Badge de grupo alvo (ex: "Parents only", "All").
         - Datas formatadas via |date template filter.

[ ] 4.3.5: Criar comunicacao/urls.py (app_name='comunicacao') e incluir no core/urls.py.

[ ] 4.3.6: Integrar tags {% trans %} e {% blocktrans %} nos templates de comunicação.

[ ] Task 4.4: Internacionalização Completa

[ ] 4.4.1: Adicionar {% trans %} e {% blocktrans %} em todos os templates (base.html, landing.html, login.html, dashboard.html, noticeboard_list.html).

[ ] 4.4.2: Executar: python manage.py makemessages -l pt_BR e preencher locale/pt_BR/LC_MESSAGES/django.po.

[ ] 4.4.3: Executar: python manage.py makemessages -l ru e preencher locale/ru/LC_MESSAGES/django.po.

[ ] 4.4.4: Compilar: python manage.py compilemessages.

Sprint 5: Boletim, Horários e Refinamentos UX
[ ] Task 5.1: Boletim do Aluno (ReportCard View)

[ ] 5.1.1: Criar ReportCardView (LoginRequiredMixin + TemplateView) em academico/views.py:
         - Aluno vê o próprio boletim.
         - Pai vê boletim de qualquer filho vinculado via Guardian (verificar ownership).
         - Contexto: grades agrupadas por subject + term em dicionário aninhado.
         - Calcular média por disciplina e % de presença.

[ ] 5.1.2: Criar template academico/templates/academico/report_card.html:
         - Tabela responsiva com colunas: Disciplina | 1º Bim | 2º Bim | 3º Bim | 4º Bim | Média | Frequência %.
         - Cor condicional: média < 5 → text-red-600, 5–7 → text-yellow-600, ≥ 7 → text-green-600.
         - Botão de impressão (window.print() via JS inline).

[ ] Task 5.2: Grade Horária (Schedule View)

[ ] 5.2.1: Criar ScheduleView (LoginRequiredMixin + TemplateView) em academico/views.py:
         - Para Student: schedules dos subjects do seu course.
         - Para Teacher: schedules dos subjects que ensina.
         - Contexto: dicionário {weekday: [schedules]}.

[ ] 5.2.2: Criar academico/templates/academico/schedule.html:
         - Tabela semanal: colunas = dias da semana, linhas = horários.
         - Cells com nome da disciplina + professor/turma.

[ ] Task 5.3: Melhorias de UX no Dashboard

[ ] 5.3.1: Adicionar contadores de notificações na Navbar: mensagens não lidas (is_read=False para o usuário) via context_processor.

[ ] 5.3.2: Criar core/context_processors.py com função unread_messages_count(request) e registrar em TEMPLATES > context_processors no settings.py.

[ ] 5.3.3: Dashboard de Parent: accordion ou tabs por filho vinculado (via Guardian), mostrando notas + frequência de cada filho separadamente.

[ ] Task 5.4: Testes Automatizados

[ ] 5.4.1: Criar tests em usuarios/tests.py: test_create_user_with_email, test_login_with_email, test_guardian_relationship.

[ ] 5.4.2: Criar tests em academico/tests.py: test_enrollment, test_grade_unique_together, test_dashboard_context_by_group.

[ ] 5.4.3: Criar tests em comunicacao/tests.py: test_noticeboard_filter_by_group, test_message_mark_as_read.

[ ] 5.4.4: Rodar: python manage.py test --verbosity=2 e garantir 0 falhas.
