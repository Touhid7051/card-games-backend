# Generated by Django 5.1.1 on 2024-09-20 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mile_master', '0003_rename_highest_score_leaderboard_total_score_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='current_flip',
            field=models.IntegerField(default=0),
        ),
    ]
