# Generated by Django 4.2.7 on 2023-12-05 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_rename_password2_user_repeat_password'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geeks_field', models.IntegerField(choices=[(0, 'Qorovul'), (1, 'Director')], default=0)),
            ],
        ),
    ]
