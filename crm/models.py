from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Client(models.Model):
    CLIENT_OR_PROSPECT_CHOICES = [
        ('Client', 'Client'),
        ('Prospect', 'Prospect'),
    ]
    id = models.AutoField(primary_key=True)
    client_or_prospect = models.CharField(max_length=50, choices=CLIENT_OR_PROSPECT_CHOICES)
    nom_commercial = models.CharField(max_length=100)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    specialites = models.CharField(max_length=255)
    wilaya = models.CharField(max_length=100)
    commune = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.nom} {self.prenom}"
    

class ClientProfil(models.Model):
    client = models.OneToOneField(Client, on_delete=models.CASCADE, primary_key=True)
    insertion_gps = models.BooleanField()
    comment_insertion_gps = models.CharField(max_length=255, blank=True, null=True)

    integration_photos = models.BooleanField()
    comment_integration_photos = models.CharField(max_length=255, blank=True, null=True)  

    remplissage_services_cabinet = models.BooleanField()
    comment_remplissage_services_cabinet = models.CharField(max_length=255, blank=True, null=True)
    
    remarque_client = models.TextField(blank=True, null=True)
    agenda = models.BooleanField()
    comment_agenda = models.CharField(max_length=255, blank=True, null=True)

    mot_de_passe_contrat = models.BooleanField()
    comment_mot_de_passe_contrat = models.CharField(max_length=255, blank=True, null=True)

    logo_recherche_premium = models.BooleanField()
    comment_logo_recherche_premium = models.CharField(max_length=255, blank=True, null=True)

    ordre_logo_pub_recherche = models.IntegerField(blank=True, null=True)
    mail_bienvenue = models.BooleanField()
    comment_mail_bienvenue = models.CharField(max_length=255, blank=True, null=True)

    appel_activation = models.BooleanField()
    comment_appel_activation = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Profile for {self.client.nom} {self.client.prenom}"


class Telephone(models.Model):
    id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='telephones')
    telephone_number = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.telephone_number}"


class AbonnementType(models.Model):
    abonnement = models.CharField(max_length=50)
    prix = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)

    def __str__(self):
        return self.abonnement


class Version(models.Model):
    version = models.CharField(max_length=50)
    abonnement_type = models.ForeignKey(AbonnementType, on_delete=models.CASCADE, related_name='versions')
    
    def __str__(self):
        return f"{self.abonnement_type}|{self.version}"


class Abonnement(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='abonnements')
    type_abonnement = models.ForeignKey(AbonnementType, on_delete=models.CASCADE, related_name='abonnements')
    version_offre = models.ForeignKey(Version, on_delete=models.CASCADE, related_name='abonnements')
    nombre_mois = models.IntegerField()
    date_de_payement = models.DateField()
    moyen_de_payement = models.CharField(max_length=50)
    statut_de_payement = models.CharField(max_length=50)
    date_debut_abonnement = models.DateField()
    
    def __str__(self):
        return f"{self.client} - {self.version_offre}"


class Renouvellement(models.Model):
    abonnement = models.OneToOneField(Abonnement, on_delete=models.CASCADE, related_name='renouvellement', primary_key=True)
    date_fin_abonnement = models.DateField()
    date_preavis_renouvellement = models.DateField()

    mail_fin_abonnement = models.BooleanField()
    comment_mail_fin_abonnement = models.CharField(max_length=255, blank=True, null=True)
    viber_fin_abonnement = models.BooleanField()
    comment_viber_fin_abonnement = models.CharField(max_length=255, blank=True, null=True)
    appel_rdv_renouvellement = models.BooleanField()
    comment_appel_rdv_renouvellement = models.CharField(max_length=255, blank=True, null=True)

    remarque = models.TextField(blank=True, null=True)
    possibilite_renouvellement = models.IntegerField(default=0, blank=True, null=True, validators=[MinValueValidator(0), MaxValueValidator(100)], help_text="de 0 à 100")
    mail_preavis_abonnement = models.BooleanField()
    comment_mail_preavis_abonnement = models.CharField(max_length=255, blank=True, null=True)
    date_rdv_renouvellement = models.DateField(blank=True, null=True)
    resultat_rdv = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Renouvellement pour {self.abonnement}"


class BoostService(models.Model):
    abonnement = models.ForeignKey(Abonnement, on_delete=models.CASCADE)
    mois = models.IntegerField()
    publication_affiche_fb = models.BooleanField()
    boost_prix = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    date_boost = models.DateField(default='')
    date_fin = models.DateField()

    def __str__(self):
        return f"Boost mois {self.mois} - {self.abonnement}"


class ClientService(models.Model):
    boost_service = models.OneToOneField(BoostService, on_delete=models.CASCADE, related_name='client_service')
    mail_pub_facebook = models.BooleanField()
    comment_mail_pub_facebook = models.CharField(max_length=255, blank=True, null=True)
    mail_resultat_fb = models.BooleanField()
    comment_mail_resultat_fb = models.CharField(max_length=255, blank=True, null=True)
    mail_temoignage_positive = models.BooleanField()
    comment_mail_temoignage_positive = models.CharField(max_length=255, blank=True, null=True)
    appel_resultat = models.BooleanField()
    comment_appel_resultat = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Client Service for {self.boost_service.abonnement} - mois {self.boost_service.mois}"
    
