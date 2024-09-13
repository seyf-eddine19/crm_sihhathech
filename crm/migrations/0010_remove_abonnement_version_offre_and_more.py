# Generated by Django 5.0.7 on 2024-08-23 00:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0009_alter_clientservice_appel_resultat_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='abonnement',
            name='version_offre',
        ),
        migrations.AlterField(
            model_name='abonnement',
            name='type_abonnement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='abonnements', to='crm.version'),
        ),
    ]