# Generated by Django 4.0.3 on 2022-03-31 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news_creation', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='editor',
            field=models.GenericIPAddressField(blank=True, null=True),
        ),
    ]