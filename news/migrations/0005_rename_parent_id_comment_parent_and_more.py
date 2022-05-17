# Generated by Django 4.0.4 on 2022-05-16 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_article_comment_delete_publication'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='parent_id',
            new_name='parent',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='user_id',
            new_name='user',
        ),
        migrations.AlterField(
            model_name='comment',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]