from django.contrib import admin
from .models import Client, ClientProfil, ClientDocument, Telephone, AbonnementType, Version, Abonnement, Renouvellement, BoostService, ClientService
from .forms import AbonnementForm, BoostServiceForm
from .actions import export_to_excel, import_from_excel
from django.urls import reverse, path
from django.utils.html import format_html
from django.shortcuts import render, get_object_or_404
from django.utils.timezone import now
from django.db import transaction
from datetime import timedelta

# Inline Models
class TelephoneInline(admin.TabularInline):
    model = Telephone
    extra = 1

class ClientDocumentInline(admin.TabularInline):
    model = ClientDocument
    extra = 1
    readonly_fields = ('document_preview',)

    def document_preview(self, obj):
        if obj.is_image:
            return format_html('<img src="{}" style="max-width: 200px; max-height: 200px;" />', obj.document.url)
        elif obj.is_pdf:
            return format_html('<a href="{}" target="_blank">View PDF</a>', obj.document.url)
        elif obj.is_excel or obj.is_word:
            return format_html('<a href="{}" target="_blank">Download Document</a>', obj.document.url)
        return "No preview available"
    document_preview.short_description = "Document Preview"

class ClientProfilInline(admin.StackedInline):
    model = ClientProfil
    extra = 1

class RenouvellementInline(admin.StackedInline):
    model = Renouvellement
    extra = 1

class VersionInline(admin.TabularInline):
    model = Version
    extra = 1

class ClientServiceInline(admin.StackedInline):
    model = ClientService
    readonly_fields = ('boost_service',)
    extra = 0

    def has_add_permission(self, request, obj=None):
        return False  # Disable adding new instances

    def has_delete_permission(self, request, obj=None):
        return False  # Disable deleting instances

    def has_change_permission(self, request, obj=None):
        return True  # Allow changing existing instances
    
class BoostServiceInline(admin.StackedInline):
    model = BoostService
    form = BoostServiceForm
    extra = 0 

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        formset.form.abonnement = obj
        return formset

# Admin Classes
class ClientAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'client_or_prospect', 'nom_commercial', 'wilaya', 'commune', 'is_data_complete', 'view_details_button')
    search_fields = ('nom', 'prenom', 'nom_commercial')
    list_filter = ('client_or_prospect', 'wilaya', 'commune')
    inlines = [TelephoneInline, ClientProfilInline, ClientDocumentInline]
    actions = [export_to_excel, import_from_excel]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:client_id>/details/', self.admin_site.admin_view(self.client_details_view), name='client_details'),
        ]
        return custom_urls + urls
    
    def is_data_complete(self, obj):
        client_fields = [obj.nom, obj.prenom, obj.nom_commercial, obj.specialites, obj.wilaya, obj.commune]
        if not all(client_fields):
            return format_html('<span style="color: red;">Incomplete</span>')

        try:
            client_profile = obj.clientprofil
            profile_fields = [
                client_profile.insertion_gps,
                client_profile.integration_photos,
                client_profile.remplissage_services_cabinet,
                client_profile.agenda,
                client_profile.mot_de_passe_contrat,
                client_profile.logo_recherche_premium,
                client_profile.ordre_logo_pub_recherche,
                client_profile.mail_bienvenue,
                client_profile.appel_activation,
            ]

            if not all(profile_fields):
                return format_html('<span style="color: red;"><i class="fas fa-times-circle"></i></span>')
        except ClientProfil.DoesNotExist:
            return format_html('<span style="color: red;"><i class="fas fa-exclamation-circle"></i></span>')

        return format_html('<span style="color: green;"><i class="fas fa-check-circle"></i></span>')

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

    def view_details_button(self, obj):
        return format_html('<a class="button" href="{}">View Details</a>', reverse('admin:client_details', args=[obj.pk]))
    view_details_button.short_description = 'View Details'
    view_details_button.allow_tags = True

class AbonnementAdmin(admin.ModelAdmin):
    form = AbonnementForm
    list_display = ('client', 'type_abonnement', 'nombre_mois', 'date_de_payement', 'statut_de_payement')
    search_fields = ('client__nom', 'client__prenom', 'type_abonnement__abonnement', 'type_abonnement__version')
    list_filter = ('type_abonnement', 'statut_de_payement')
    inlines = [RenouvellementInline, BoostServiceInline, ClientServiceInline]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        print(change)
        if not change:  # Only execute if creating a new Abonnement
            with transaction.atomic():
                # Create Renouvellement instance
                Renouvellement.objects.create(
                    abonnement=obj,
                    date_fin_abonnement=obj.date_debut_abonnement + timedelta(days=obj.nombre_mois*30),  # Assuming 30 days per month
                    date_preavis_renouvellement=obj.date_debut_abonnement + timedelta(days=(obj.nombre_mois)*30 + 3),
                    mail_fin_abonnement=False,
                    viber_fin_abonnement=False,
                    appel_rdv_renouvellement=False,
                    mail_preavis_abonnement=False,
                )

                # Create BoostService instances based on the number of months
                for mois in range(1, obj.nombre_mois + 1):
                    BoostService.objects.create(
                        abonnement=obj,
                        mois=mois,
                        publication_affiche_fb=False,
                        boost_prix=obj.type_abonnement.abonnement_type.prix,
                        date_boost=obj.date_debut_abonnement + timedelta(days=(mois-1)*30),
                        date_fin=obj.date_debut_abonnement + timedelta(days=mois*30)
                    )

# Notification Function
def notify_expiring_boosts(modeladmin, request, queryset):
    # Calculate the date 3 days from now
    three_days_from_now = now().date() + timedelta(days=3)
    
    # Filter BoostService objects with date_fin less than 3 days from now
    expiring_boosts = queryset.filter(date_fin__lte=three_days_from_now, date_fin__gte=now().date())
    
    # If there are expiring boosts, display them
    if expiring_boosts.exists():
        message = "Boosts expiring within 3 days:\n"
        for boost in expiring_boosts:
            message += f"{boost}\n"
        modeladmin.message_user(request, message)
    else:
        modeladmin.message_user(request, "No boosts expiring within 3 days.")

notify_expiring_boosts.short_description = "Notify expiring Boost Services within 3 days"

class AbonnementTypeAdmin(admin.ModelAdmin):
    list_display = ('abonnement',)
    search_fields = ('abonnement',)
    inlines = [VersionInline]

class BoostServiceAdmin(admin.ModelAdmin):
    actions = [notify_expiring_boosts]
    list_display = ('abonnement', 'mois', 'publication_affiche_fb', 'boost_prix', 'date_boost', 'date_fin')
    search_fields = ('abonnement__client__nom', 'abonnement__client__prenom')
    list_filter = ('publication_affiche_fb',)
    inlines = [ClientServiceInline]  # Include ClientService as inline

class ClientServiceAdmin(admin.ModelAdmin):
    list_display = ('boost_service', 'abonnement', 'mail_pub_facebook', 'comment_mail_pub_facebook', 'mail_resultat_fb', 'comment_mail_resultat_fb', 'mail_temoignage_positive', 'comment_mail_temoignage_positive', 'appel_resultat', 'comment_appel_resultat')
    search_fields = ('boost_service__abonnement__client__nom', 'boost_service__abonnement__client__prenom')
    list_filter = ('boost_service',)

    def has_add_permission(self, request, obj=None):
        return False  # Disable adding new instances

    def has_delete_permission(self, request, obj=None):
        return False  # Disable deleting instances

    def has_change_permission(self, request, obj=None):
        return True  # Allow changing existing instances

# Register Admin Classes
admin.site.register(Client, ClientAdmin)
admin.site.register(AbonnementType, AbonnementTypeAdmin)
admin.site.register(Abonnement, AbonnementAdmin)
admin.site.register(BoostService, BoostServiceAdmin)
admin.site.register(ClientService, ClientServiceAdmin)
