# Generated by Django 4.2.5 on 2024-01-11 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0008_rfq_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='quotation',
            name='feedback',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]