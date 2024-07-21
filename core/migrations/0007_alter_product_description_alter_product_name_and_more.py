# Generated by Django 5.0.7 on 2024-07-15 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_product_warning'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.CharField(blank=True, default='', max_length=9000, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='product',
            name='specification1',
            field=models.CharField(blank=True, default='', max_length=9000, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='specification2',
            field=models.CharField(blank=True, default='', max_length=9000, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='specification3',
            field=models.CharField(blank=True, default='', max_length=9000, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='specification4',
            field=models.CharField(blank=True, default='', max_length=9000, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='specification5',
            field=models.CharField(blank=True, default='', max_length=9000, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='warning',
            field=models.CharField(blank=True, default='', max_length=9000, null=True),
        ),
    ]
