# Generated by Django 3.1.5 on 2021-03-11 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dummy_csv', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='scheme',
            name='column_separator',
            field=models.CharField(choices=[(',', 'Comma (,)'), (';', 'Semicolon (;)')], default='', max_length=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='scheme',
            name='string_character',
            field=models.CharField(choices=[('"', 'Double-quote (")')], default='', max_length=1),
            preserve_default=False,
        ),
    ]
