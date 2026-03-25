from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def dashboard(request):
    # TODO: Sprint 3 - implement role-based dashboard
    return render(request, 'academico/dashboard.html')
