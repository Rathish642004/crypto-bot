# Generated by Django 4.2.6 on 2024-04-08 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(max_length=100)),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=10)),
                ('side', models.CharField(max_length=50)),
                ('orderid', models.DecimalField(decimal_places=2, max_digits=20)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
    ]