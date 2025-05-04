from datetime import timedelta
from django.db.models import Sum
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView, PasswordResetConfirmView
from admin_soft.forms import RegistrationForm, LoginForm, UserPasswordResetForm, UserSetPasswordForm, UserPasswordChangeForm
from django.contrib.auth import logout

from job.models import Job, Location, Search
from relocate.models import Relocate
from .utils import get_chart

# Create your views here.

# Pages
@login_required()
def index(request):
    chart_data = get_chart()
    chart = {
        "bar_keys": chart_data[0],
        "bar_values": chart_data[1],
        "line_keys": chart_data[2],
        "line_values_relocates": chart_data[3],
        "line_values_jobs": chart_data[4],
    }
    # Use timezone-aware datetime
    # includes today, so 9 days total
    nine_days_ago = timezone.now().date() - timedelta(days=8)
    return render(request, 'admin/index.html', {'segment': 'index', 
                                                'chart': chart,
                                                'processed_jobs': Job.all_objects.count(),
                                                'relocation_jobs': Job.all_objects.filter(relocation=True).count(),
                                                'locations': Location.objects.count(),
                                                'locations_list': Location.objects.all(),
                                                'search_terms': Search.objects.count(),
                                                'search_terms_list': Search.objects.all(),
                                                'recent_9_days_jobs': Job.objects.filter(gathered_at__date__gte=nine_days_ago).count(),
                                                'recent_9_days_relocations': Job.objects.filter(relocation=True,
                                                            gathered_at__date__gte=nine_days_ago).count(),
                                                'recent_9_days_upvotes': Relocate.objects.filter(gathered_at__date__gte=nine_days_ago
                                                            ).aggregate(sum=Sum('upvotes'))['sum'] or 0})


# Authentication
class UserLoginView(LoginView):
    template_name = 'accounts/login.html'
    form_class = LoginForm

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/dashboard/accounts/login/')
    else:
        form = RegistrationForm()

    context = { 'form': form }
    return render(request, 'accounts/register.html', context)

def logout_view(request):
    logout(request)
    return redirect('/dashboard/accounts/login/')

class UserPasswordResetView(PasswordResetView):
    template_name = 'accounts/password_reset.html'
    form_class = UserPasswordResetForm

class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    form_class = UserSetPasswordForm

class UserPasswordChangeView(PasswordChangeView):
    template_name = 'accounts/password_change.html'
    form_class = UserPasswordChangeForm