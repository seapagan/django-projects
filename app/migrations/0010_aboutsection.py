# Generated by Django 5.1.7 on 2025-03-29 08:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_project_priority'),
    ]

    operations = [
        migrations.CreateModel(
            name='AboutSection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(help_text='Content can include HTML tags like: <a>, <strong>, <em>, <p>, <ul>, <ol>, <li>, <h1-h3>, <br>, <hr>')),
                ('config', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='about_sections', to='app.siteconfiguration')),
            ],
            options={
                'verbose_name': 'About Section',
                'verbose_name_plural': 'About Sections',
            },
        ),
    ]
