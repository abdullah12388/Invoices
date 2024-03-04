# Generated by Django 4.2.5 on 2024-01-18 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0017_alter_pomilestone_due'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchaseorder',
            name='remaining_value',
            field=models.FloatField(default=60641),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='status',
            field=models.CharField(choices=[('o', 'Opened'), ('c', 'Closed')], default='o', max_length=256),
        ),
    ]
