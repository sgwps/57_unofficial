# Generated by Django 4.0.3 on 2022-04-10 17:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0002_alter_profile_city'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='graduation_year',
        ),
    ]
