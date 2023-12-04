# Generated by Django 4.2.5 on 2023-10-05 10:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0007_alter_comment_created_by'),
        ('campaigns', '0007_campaign_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='CampaignClient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='clients', to='campaigns.campaign')),
                ('client', models.ManyToManyField(related_name='campaigns', to='client.client')),
            ],
        ),
    ]
