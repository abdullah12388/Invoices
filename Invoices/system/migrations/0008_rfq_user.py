# Generated by Django 4.2.5 on 2024-01-08 16:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
        ('system', '0007_quotation_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='rfq',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='account.useraccount'),
            preserve_default=False,
        ),
    ]
