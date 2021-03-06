# Generated by Django 4.0.4 on 2022-06-10 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myshop', '0003_admin'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='admin',
            options={'verbose_name_plural': 'Admin'},
        ),
        migrations.AddField(
            model_name='order',
            name='payment_method',
            field=models.CharField(choices=[('Cash On Delivery', 'Cash On Delivery'), ('Khalti', 'Khalti')], default='Cash On Delivery', max_length=50),
        ),
        migrations.AddField(
            model_name='order',
            name='paymet_completed',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
