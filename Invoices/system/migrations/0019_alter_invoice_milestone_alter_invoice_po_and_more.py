# Generated by Django 4.2.5 on 2024-01-24 11:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0018_purchaseorder_remaining_value_purchaseorder_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='milestone',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.pomilestone'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='po',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.purchaseorder'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='project_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.project'),
        ),
        migrations.AlterField(
            model_name='rfq',
            name='status',
            field=models.CharField(choices=[('s', 'Sent'), ('v', 'Viewed'), ('r', 'Replyed')], default='s', max_length=50),
        ),
    ]
