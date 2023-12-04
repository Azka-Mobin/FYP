# Generated by Django 4.1.7 on 2023-09-25 12:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0004_alter_team_plan'),
        ('userprofile', '0002_rename_user_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='active_team_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='userprofiles', to='team.team'),
        ),
    ]
