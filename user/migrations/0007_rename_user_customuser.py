# Generated by Django 4.2.7 on 2023-12-05 13:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('authtoken', '0003_tokenproxy'),
        ('booking', '0002_rename_percent_basesum_sum_and_more'),
        ('admin', '0003_logentry_add_action_flag_choices'),
        ('user', '0006_employer'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='User',
            new_name='CustomUser',
        ),
    ]
