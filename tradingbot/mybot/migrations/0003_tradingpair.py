# Generated by Django 4.2.6 on 2024-04-14 05:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mybot', '0002_alter_order_price_alter_order_quantity'),
    ]

    operations = [
        migrations.CreateModel(
            name='TradingPair',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(max_length=10)),
                ('quantity', models.DecimalField(decimal_places=3, max_digits=10)),
                ('buy_price', models.DecimalField(blank=True, decimal_places=8, max_digits=10, null=True)),
                ('sell_price', models.DecimalField(blank=True, decimal_places=8, max_digits=10, null=True)),
            ],
        ),
    ]