from django.contrib import admin
from .models import Client, Telephone, AbonnementType, Version, Abonnement, Renouvellement, BoostService, ClientService


class TelephoneInline(admin.TabularInline):
    model = Telephone
    extra = 1


class ClientAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'client_or_prospect', 'nom_commercial', 'wilaya', 'commune')
    search_fields = ('nom', 'prenom', 'nom_commercial')
    list_filter = ('client_or_prospect', 'wilaya', 'commune')
    inlines = [TelephoneInline]


class VersionInline(admin.TabularInline):
    model = Version
    extra = 1


class AbonnementTypeAdmin(admin.ModelAdmin):
    list_display = ('abonnement',)
    search_fields = ('abonnement',)
    inlines = [VersionInline]


class AbonnementAdmin(admin.ModelAdmin):
    list_display = ('client', 'type_abonnement', 'version_offre', 'nombre_mois', 'date_de_payement', 'statut_de_payement')
    search_fields = ('client__nom', 'client__prenom', 'type_abonnement__name', 'version_offre__name')
    list_filter = ('type_abonnement', 'version_offre', 'statut_de_payement')


class RenouvellementAdmin(admin.ModelAdmin):
    list_display = ('abonnement', 'date_fin_abonnement', 'date_preavis_renouvellement', 'mail_fin_abonnement')
    search_fields = ('abonnement__client__nom', 'abonnement__client__prenom', 'abonnement__type_abonnement__name')
    list_filter = ('mail_fin_abonnement', 'viber_fin_abonnement', 'appel_rdv_renouvellement')


class ClientServiceInline(admin.StackedInline):
    model = ClientService
    extra = 0  # Number of empty forms to display


class BoostServiceAdmin(admin.ModelAdmin):
    list_display = ('abonnement', 'mois', 'publication_affiche_fb', 'boost_prix', 'date_boost', 'date_fin')
    search_fields = ('abonnement__client__nom', 'abonnement__client__prenom')
    list_filter = ('publication_affiche_fb',)
    inlines = [ClientServiceInline]  # Include ClientService as inline

admin.site.register(Client, ClientAdmin)
admin.site.register(AbonnementType, AbonnementTypeAdmin)
admin.site.register(Abonnement, AbonnementAdmin)
admin.site.register(Renouvellement, RenouvellementAdmin)
admin.site.register(BoostService, BoostServiceAdmin)
