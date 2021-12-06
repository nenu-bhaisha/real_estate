# Generated by Django 3.2.6 on 2021-12-04 09:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userside', '0008_auto_20211204_1427'),
    ]

    operations = [
        migrations.CreateModel(
            name='property_rented_sold',
            fields=[
                ('property_rented_sold_id', models.AutoField(primary_key=True, serialize=False)),
                ('property_rented_sold_date', models.DateField()),
                ('property_rented_sold_property_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userside.property')),
                ('property_rented_sold_user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userside.user_details')),
            ],
        ),
    ]
