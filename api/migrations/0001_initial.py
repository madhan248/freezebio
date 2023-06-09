# Generated by Django 4.2 on 2023-05-04 14:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DeviceConfiguration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_id', models.CharField(blank=True, default='', max_length=150, null=True)),
                ('location', models.CharField(blank=True, default='', max_length=150, null=True)),
                ('device_name', models.CharField(blank=True, default='', max_length=150, null=True)),
                ('display', models.BooleanField(default=True)),
                ('params', jsonfield.fields.JSONField(default=[])),
                ('device', models.CharField(choices=[('1', 'Cooling'), ('2', 'Heating')], default='1', max_length=10)),
                ('max_limit', models.FloatField(default=0.0, max_length=15)),
                ('min_limit', models.FloatField(default=0.0, max_length=15)),
                ('interval', models.CharField(blank=True, default='1', max_length=15, null=True)),
                ('points', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='DeviceData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_type', models.CharField(blank=True, default='', max_length=150, null=True)),
                ('device_id', models.CharField(blank=True, default='', max_length=15, null=True)),
                ('data', jsonfield.fields.JSONField(default={})),
                ('timestamp', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='DeviceType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_type', models.CharField(blank=True, default='', max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Events',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_id', models.CharField(blank=True, default='', max_length=15, null=True)),
                ('open_timestamp', models.PositiveIntegerField()),
                ('closed_timestamp', models.PositiveIntegerField()),
                ('event_count', models.CharField(blank=True, default='', max_length=15, null=True)),
                ('device_id', models.CharField(blank=True, default='', max_length=15, null=True)),
                ('acknowledged', models.TextField(default='')),
                ('event_status', models.CharField(blank=True, default='', max_length=15, null=True)),
                ('event_type', models.CharField(blank=True, default='', max_length=15, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='LatestData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_type', models.CharField(blank=True, default='', max_length=150, null=True)),
                ('device_id', models.CharField(blank=True, default='', max_length=15, null=True)),
                ('data', jsonfield.fields.JSONField(default={})),
                ('timestamp', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None)),
                ('organization', models.CharField(blank=True, default='', max_length=15, null=True)),
                ('designation', models.CharField(blank=True, default='', max_length=15, null=True)),
                ('verified', models.BooleanField(default=False)),
                ('admin', models.BooleanField(default=False)),
                ('Dob', models.DateField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='users', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player_id', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='DevicePermission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_config', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='config', to='api.deviceconfiguration')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profiles', to='api.userprofile')),
            ],
        ),
        migrations.AddIndex(
            model_name='devicedata',
            index=models.Index(fields=['device_id', '-timestamp'], name='api_deviced_device__e50175_idx'),
        ),
        migrations.AddField(
            model_name='deviceconfiguration',
            name='device_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='type', to='api.devicetype'),
        ),
    ]
