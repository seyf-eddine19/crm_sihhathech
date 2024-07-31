from django.contrib import admin
from .models import Client, ClientProfil, Telephone, AbonnementType, Version, Abonnement, Renouvellement, BoostService, ClientService
from .forms import AbonnementForm


class TelephoneInline(admin.TabularInline):
    model = Telephone
    extra = 1

class ClientProfilInline(admin.StackedInline):
    model = ClientProfil
    extra = 1

class RenouvellementInline(admin.StackedInline):
    model = Renouvellement
    extra = 1


from django.urls import reverse,  path
from django.utils.html import format_html
from django.shortcuts import render, get_object_or_404

class ClientAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'client_or_prospect', 'nom_commercial', 'wilaya', 'commune', 'view_details_button')
    search_fields = ('nom', 'prenom', 'nom_commercial')
    list_filter = ('client_or_prospect', 'wilaya', 'commune')
    inlines = [TelephoneInline, ClientProfilInline]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:client_id>/details/', self.admin_site.admin_view(self.client_details_view), name='client_details'),
        ]
        return custom_urls + urls
    
    def view_details_button(self, obj):
        return format_html('<a class="button" href="{}">View Details</a>', reverse('admin:client_details', args=[obj.pk]))
    view_details_button.short_description = 'View Details'
    view_details_button.allow_tags = True

    def client_details_view(self, request, client_id):
        client = get_object_or_404(Client, pk=client_id)
        abonnements = Abonnement.objects.filter(client=client)
        
        boosts_by_abonnement = {}
        client_services_by_boost = {}
        renouvelements = {}

        for abonnement in abonnements:
            boosts = BoostService.objects.filter(abonnement=abonnement)
            boosts_by_abonnement[abonnement.id] = boosts if boosts else []
            
            for boost in boosts:
                client_services = ClientService.objects.filter(boost_service=boost)
                client_services_by_boost[boost.id] = client_services if client_services else []
            renouvelements[abonnement.id] = Renouvellement.objects.filter(abonnement=abonnement)

        telephones = client.telephones.all()
        profils = ClientProfil.objects.filter(client=client)
        
        context = {
            'client': client,
            'abonnements': abonnements,
            'boosts_by_abonnement': boosts_by_abonnement,
            'client_services_by_boost': client_services_by_boost,
            'telephones': telephones,
            'profils': profils,
            'renouvelements': renouvelements,
        }
        return render(request, 'admin/client_details.html', context)
    

class VersionInline(admin.TabularInline):
    model = Version
    extra = 1

class AbonnementTypeAdmin(admin.ModelAdmin):
    list_display = ('abonnement',)
    search_fields = ('abonnement',)
    inlines = [VersionInline]

class ClientServiceInline(admin.StackedInline):
    model = ClientService
    extra = 0  # umber of empty forms to displayN

class BoostServiceInline(admin.StackedInline):
    model = BoostService
    extra = 0  # Number of empty forms to display
    inlines = [ClientServiceInline]

class AbonnementAdmin(admin.ModelAdmin):
    form = AbonnementForm
    list_display = ('client', 'type_abonnement', 'version_offre', 'nombre_mois', 'date_de_payement', 'statut_de_payement')
    search_fields = ('client__nom', 'client__prenom', 'type_abonnement__abonnement', 'version_offre__version')
    list_filter = ('type_abonnement', 'version_offre', 'statut_de_payement')
    inlines = [RenouvellementInline, BoostServiceInline]

    # class Media:
    #     js = ('crm/js/abonnement_form.js',)

class BoostServiceAdmin(admin.ModelAdmin):
    list_display = ('abonnement', 'mois', 'publication_affiche_fb', 'boost_prix', 'date_boost', 'date_fin')
    search_fields = ('abonnement__client__nom', 'abonnement__client__prenom')
    list_filter = ('publication_affiche_fb',)
    inlines = [ClientServiceInline]  # Include ClientService as inline

class ClientServiceAdmin(admin.ModelAdmin):
    # list_display = ()
    search_fields = ()
    list_filter = ()
    inlines = []  # Include ClientService as inline


admin.site.register(Client, ClientAdmin)
admin.site.register(AbonnementType, AbonnementTypeAdmin)
admin.site.register(Abonnement, AbonnementAdmin)
admin.site.register(ClientService, ClientServiceAdmin)

