# Generated by Django 5.1.2 on 2024-10-23 15:56

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contas', '0001_initial'),
        ('dispositivos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('start_time', models.TimeField(null=True)),
                ('end_time', models.TimeField(null=True)),
                ('days_week', models.CharField(choices=[('sun', 'dom'), ('mon', 'seg'), ('tue', 'ter'), ('wed', 'qua'), ('thu', 'qui'), ('fri', 'sex'), ('sat', 'sab')], max_length=50, null=True)),
                ('account_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contas.conta')),
                ('device_id', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='dispositivos.dispositivo')),
            ],
        ),
    ]
