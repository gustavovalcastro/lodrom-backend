# Generated by Django 5.1.2 on 2024-10-18 22:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contas', '0001_initial'),
        ('dispositivos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Portao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pin', models.CharField(blank=True, max_length=4, null=True)),
                ('account_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contas.conta')),
                ('device_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dispositivos.dispositivo')),
            ],
            options={
                'verbose_name_plural': 'Portoes',
            },
        ),
    ]