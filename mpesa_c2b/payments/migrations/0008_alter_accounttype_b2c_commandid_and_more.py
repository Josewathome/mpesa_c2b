# Generated by Django 5.1.3 on 2025-02-17 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0007_alter_accounttype_b2c_commandid_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accounttype',
            name='b2c_commandid',
            field=models.CharField(choices=[('PromotionPayment', 'PromotionPayment'), ('SalaryPayment', 'SalaryPayment'), ('BusinessPayment', 'BusinessPayment')], default='BusinessPayment', max_length=255),
        ),
        migrations.AlterField(
            model_name='accounttype',
            name='c2b_responsetype',
            field=models.CharField(choices=[('Cancelled', 'Cancelled'), ('Completed', 'Completed')], default='Completed', max_length=225),
        ),
    ]
