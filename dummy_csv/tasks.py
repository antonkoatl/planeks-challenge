import csv
from datetime import date
from itertools import repeat
from random import randint

from django.core.files.base import ContentFile

from challengesite.celery import app
from dummy_csv.models import Dataset, Column

dummy_dict = {
    Column.ColumnType.FULL_NAME: lambda a, b: 'Benedict Cumberbatch',
    Column.ColumnType.JOB: lambda a, b: 'President of the world',
    Column.ColumnType.EMAIL: lambda a, b: 'simple@mail.com',
    Column.ColumnType.DOMAIN_NAME: lambda a, b: 'Domain',
    Column.ColumnType.PHONE_NUMBER: lambda a, b: '+0123456789',
    Column.ColumnType.COMPANY_NAME: lambda a, b: 'Company inc.',
    Column.ColumnType.TEXT: lambda a, b: " ".join(repeat('Simple text example.', randint(a, b))),
    Column.ColumnType.INTEGER: randint,
    Column.ColumnType.ADDRESS: lambda a, b: '500003, Secunderabad,  Andhra Pradesh, 75 -A, Rajiv Gandhi Rahadari, Vikrampuri',
    Column.ColumnType.DATE: lambda a, b: date.today(),
}


@app.task
def generate_dataset(dataset_id, rows):
    dataset = Dataset.objects.select_related('schema').get(id=dataset_id)
    dataset.file.save('dataset.csv', ContentFile(''))


    with open(dataset.file.path, 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=dataset.schema.column_separator,
                                quotechar=dataset.schema.string_character)
        for i in range(rows):
            spamwriter.writerow(dummy_dict[column.type](column.parameter_one, column.parameter_two) for column in dataset.schema.column_set.all())

    dataset.status = Dataset.Status.READY
    dataset.save()
