# Generated by Django 5.1.7 on 2025-03-16 18:16

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_contactsubmission_alter_tag_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='GitHubStats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stars', models.IntegerField(default=0)),
                ('forks', models.IntegerField(default=0)),
                ('open_issues', models.IntegerField(default=0)),
                ('open_prs', models.IntegerField(default=0)),
                ('last_updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('project', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='github_stats', to='app.project')),
            ],
        ),
    ]
