# Generated by Django 4.1.7 on 2023-03-22 02:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taxes', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='entry',
            old_name='categroy',
            new_name='category',
        ),
    ]
