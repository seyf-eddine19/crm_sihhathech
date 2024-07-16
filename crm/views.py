from django.shortcuts import render, redirect
from django.db.models import Q 
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from .models import Client, Telephone, AbonnementType, Version, Abonnement, Renouvellement, BoostService, ClientService

class CustomLoginView(LoginView):
    template_name = 'login.html'
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

class CustomLogoutView(LogoutView):
    pass

@login_required(login_url='login/')
def home(request):
    content = {
    }
    return render(request, 'index.html', content)
