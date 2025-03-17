# Generated by Django 5.1.7 on 2025-03-17 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_githubstats'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteConfiguration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('github_username', models.CharField(blank=True, max_length=30)),
                ('twitter_username', models.CharField(blank=True, max_length=30)),
                ('linkedin_username', models.CharField(blank=True, max_length=30)),
                ('youtube_username', models.CharField(blank=True, max_length=30)),
                ('medium_username', models.CharField(blank=True, max_length=30)),
            ],
            options={
                'verbose_name': 'Site Configuration',
            },
        ),
        migrations.AlterModelOptions(
            name='githubstats',
            options={'verbose_name_plural': 'GitHub Stats'},
        ),
    ]
