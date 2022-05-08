# Generated by Django 4.0.4 on 2022-04-27 14:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0002_alter_user_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.ForeignKey(blank=True, default=0, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='users', to='user_profile.gender'),
        ),
    ]