# Generated by Django 4.2.5 on 2023-12-30 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0003_product_productcategory_productuom_rfq_rfqcurrency_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productcategory',
            name='name',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='productuom',
            name='name',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='rfqcurrency',
            name='name',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='rfqtype',
            name='name',
            field=models.CharField(max_length=256),
        ),
    ]
