# Generated by Django 5.1.2 on 2024-10-27 21:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contas', '0001_initial'),
        ('historico', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historico',
            name='account_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contas.conta'),
        ),
        migrations.AlterField(
            model_name='historico',
            name='event_type',
            field=models.CharField(choices=[('1', 'Portão destravado pelo gancho'), ('2', 'Portão aberto remotamente'), ('3', 'Mensagens anunciadas'), ('4', 'Interfone tocou')], max_length=50),
        ),
    ]
