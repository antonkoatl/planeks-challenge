# Generated by Django 3.1.5 on 2021-03-11 09:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dummy_csv', '0002_auto_20210311_1415'),
    ]

    operations = [
        migrations.RenameField(
            model_name='scheme',
            old_name='title',
            new_name='name',
        ),
    ]
