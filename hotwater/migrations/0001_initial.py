# Generated by Django 5.1.6 on 2025-03-15 12:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('devices', '0003_sunsensor_windsensor_sunsensordata_windsensordata'),
    ]

    operations = [
        migrations.CreateModel(
            name='CircPump',
            fields=[
                ('name', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=512, null=True)),
                ('relay', models.OneToOneField(on_delete=django.db.models.deletion.RESTRICT, related_name='+', to='devices.relay')),
                ('sensor', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='sensor', to='devices.tempsensor')),
            ],
            options={
                'verbose_name': 'CircPump',
                'verbose_name_plural': 'CircPumps',
            },
        ),
        migrations.CreateModel(
            name='WaterHeater',
            fields=[
                ('name', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=512, null=True)),
                ('sensor_burn', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='sensor_burn', to='devices.tempsensor')),
                ('sensor_in', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='sensor_in', to='devices.tempsensor')),
                ('sensor_out', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='sensor_out', to='devices.tempsensor')),
            ],
            options={
                'verbose_name': 'WaterHeater',
                'verbose_name_plural': 'WaterHeaters',
            },
        ),
    ]
