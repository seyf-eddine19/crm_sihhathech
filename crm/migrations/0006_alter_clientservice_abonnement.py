# Generated by Django 5.0.7 on 2024-08-22 17:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0005_clientservice_abonnement_alter_abonnement_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientservice',
            name='abonnement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='client_services', to='crm.abonnement'),
        ),
    ]
