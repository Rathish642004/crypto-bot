# Generated by Django 4.2.6 on 2024-04-25 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mybot', '0005_placedorder_side'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='placedorder',
            name='side',
        ),
        migrations.AddField(
            model_name='placedorder',
            name='orderid',
            field=models.DecimalField(decimal_places=2, default=20, max_digits=20),
            preserve_default=False,
        ),
    ]
