# Generated by Django 5.1.7 on 2025-03-20 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_framework_language'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='priority',
            field=models.IntegerField(blank=True, help_text='Lower numbers appear first', null=True),
        ),
    ]
