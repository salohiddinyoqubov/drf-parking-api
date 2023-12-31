# Generated by Django 4.2.7 on 2023-12-06 04:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('booking', '0002_rename_percent_basesum_sum_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeeOfParking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee', models.IntegerField(choices=[(0, 'Qorovul'), (1, 'Director')], default=0)),
                ('parking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.parking')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
