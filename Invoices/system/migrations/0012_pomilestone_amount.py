# Generated by Django 4.2.5 on 2024-01-15 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0011_pomilestone_purchaseorder_pofilehandler'),
    ]

    operations = [
        migrations.AddField(
            model_name='pomilestone',
            name='amount',
            field=models.PositiveBigIntegerField(blank=True, null=True),
        ),
    ]
