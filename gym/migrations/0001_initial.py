# Generated by Django 5.1.5 on 2025-02-03 15:18

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='GymClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('trainer', models.CharField(max_length=100)),
                ('capacity', models.PositiveIntegerField(default=10)),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('gym_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schedules', to='gym.gymclass')),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reservation_date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to=settings.AUTH_USER_MODEL)),
                ('schedule', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='gym.schedule')),
            ],
            options={
                'unique_together': {('user', 'schedule')},
            },
        ),
    ]
