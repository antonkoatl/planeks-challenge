# Generated by Django 3.1.5 on 2021-03-11 15:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dummy_csv', '0006_dataset_schema'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dataset',
            options={'ordering': ['-created']},
        ),
        migrations.AlterModelOptions(
            name='scheme',
            options={'ordering': ['-modified']},
        ),
        migrations.AlterField(
            model_name='dataset',
            name='status',
            field=models.CharField(choices=[('p', 'Processing'), ('r', 'Ready')], default='p', max_length=1),
        ),
        migrations.CreateModel(
            name='PendingJob',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_id', models.CharField(max_length=200)),
                ('dataset', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='dummy_csv.dataset')),
            ],
        ),
    ]