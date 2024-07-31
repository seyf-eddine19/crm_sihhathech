# Generated by Django 4.1.13 on 2024-07-19 14:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0002_clientprofil_remove_client_agenda_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='renouvellement',
            name='id',
        ),
        migrations.AlterField(
            model_name='renouvellement',
            name='abonnement',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='renouvellement', serialize=False, to='crm.abonnement'),
        ),
    ]