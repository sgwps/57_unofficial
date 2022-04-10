# Generated by Django 4.0.3 on 2022-04-10 18:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0003_remove_student_graduation_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='grade',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='students', to='user_profile.grade'),
        ),
    ]
