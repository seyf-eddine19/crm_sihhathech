from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Client, ClientProfil, Telephone, AbonnementType, Version, Abonnement, Renouvellement, BoostService, ClientService
from .forms import DateFilterForm

from django.db.models import Sum, Avg
from django.utils.timezone import now
from datetime import timedelta

from django.db.models.functions import TruncMonth

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.admin.models import LogEntry
from django.http import HttpResponse
from .actions import import_from_excel

def import_excel_view(request):
    if request.method == 'POST' and 'file' in request.FILES:
        file = request.FILES['file']
        import_from_excel(file)
        return HttpResponse('File imported successfully.')
    return HttpResponse('Invalid request.')


@login_required(login_url='login/')
@staff_member_required
def static_admin(request):
    current_date = now()
    current_month_start = current_date.replace(day=1)
    current_month_end = (current_date.replace(month=current_date.month + 1, day=1) if current_date.month < 12 else current_date.replace(year=current_date.year + 1, month=1, day=1)) - timedelta(days=1)

    form = DateFilterForm(request.GET)
    from_date = form['from_date'].value() if form.is_valid() and form['from_date'].value() else current_month_start
    to_date = form['to_date'].value() if form.is_valid() and form['to_date'].value() else current_month_end

    total_clients = Client.objects.filter(client_or_prospect='Client').count()
    total_prospects = Client.objects.filter(client_or_prospect='Prospect').count()
    total_abonnements = Abonnement.objects.filter(date_de_payement__range=[from_date, to_date]).count()
    total_renouvellements = Renouvellement.objects.filter(date_fin_abonnement__range=[from_date, to_date]).count()
    total_boost_services = BoostService.objects.filter(date_boost__range=[from_date, to_date]).count()
    avg_boost_price = BoostService.objects.filter(date_boost__range=[from_date, to_date]).aggregate(Avg('boost_prix'))['boost_prix__avg']

    boost_prices_by_client = BoostService.objects.filter().annotate(
        month=TruncMonth('date_boost')
    ).values('month', 'abonnement__client__nom', 'abonnement__client__prenom').annotate(
        total_boost=Sum('boost_prix')
    ).order_by('month', 'abonnement__client__nom', 'abonnement__client__prenom')

    boost_data = {}
    for entry in boost_prices_by_client:
        client_name = f"{entry['abonnement__client__nom']} {entry['abonnement__client__prenom']}"
        month = entry['month'].strftime("%Y-%m")
        if client_name not in boost_data:
            boost_data[client_name] = {}
        boost_data[client_name][month] = entry['total_boost']
    log_entries = LogEntry.objects.all()
    data = {
        'segment': 'static_admin',
        'form': form,
        'total_clients': total_clients,
        'total_prospects': total_prospects,
        'total_abonnements': total_abonnements,
        'total_renouvellements': total_renouvellements,
        'total_boost_services': total_boost_services,
        'avg_boost_price': avg_boost_price or 0,  # Default to 0 if no boost price data is available
        # 'month': from_date.month,
        # 'year': from_date.year
        'boost_data': boost_data, 
        'log_entries': log_entries,
    }

    return render(request, 'admin/static_page.html', data)

