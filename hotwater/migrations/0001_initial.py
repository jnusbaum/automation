# Generated by Django 3.1.7 on 2021-03-29 12:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('devices', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='WaterHeater',
            fields=[
                ('name', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=512, null=True)),
                ('sensor_burn', models.OneToOneField(on_delete=django.db.models.deletion.RESTRICT, related_name='+', to='devices.tempsensor')),
                ('sensor_in', models.OneToOneField(on_delete=django.db.models.deletion.RESTRICT, related_name='+', to='devices.tempsensor')),
                ('sensor_out', models.OneToOneField(on_delete=django.db.models.deletion.RESTRICT, related_name='+', to='devices.tempsensor')),
            ],
            options={
                'verbose_name': 'WaterHeater',
                'verbose_name_plural': 'WaterHeaters',
            },
        ),
        migrations.CreateModel(
            name='CircPump',
            fields=[
                ('name', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=512, null=True)),
                ('relay', models.OneToOneField(on_delete=django.db.models.deletion.RESTRICT, related_name='+', to='devices.relay')),
                ('sensor', models.OneToOneField(on_delete=django.db.models.deletion.RESTRICT, related_name='+', to='devices.tempsensor')),
            ],
            options={
                'verbose_name': 'CircPump',
                'verbose_name_plural': 'CircPumps',
            },
        ),
    ]