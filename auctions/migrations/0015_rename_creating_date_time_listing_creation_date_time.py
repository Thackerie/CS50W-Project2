# Generated by Django 4.1.5 on 2023-03-16 00:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0014_listing_creating_date_time'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='creating_date_time',
            new_name='creation_date_time',
        ),
    ]