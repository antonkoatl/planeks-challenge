from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class Scheme(models.Model):
    class Meta:
        ordering = ['-modified', ]

    class ColumnSeparators(models.TextChoices):
        COMMA = ",", _("Comma (,)")
        SEMICOLON = ";", _("Semicolon (;)")

    class StringCharacters(models.TextChoices):
        DOUBLE_QUOTE = "\"", _("Double-quote (\")")

    name = models.CharField(max_length=200)
    column_separator = models.CharField(max_length=1, choices=ColumnSeparators.choices, default=ColumnSeparators.COMMA)
    string_character = models.CharField(max_length=1, choices=StringCharacters.choices, default=StringCharacters.DOUBLE_QUOTE)
    modified = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    columns = models.TextField()


class Column(models.Model):
    class Meta:
        ordering = ['order', ]

    class ColumnType(models.TextChoices):
        FULL_NAME = "fullname", _("Full name")
        JOB = "job", _("Job")
        EMAIL = "email", _("Email")
        DOMAIN_NAME = "domain", _("Domain name")
        PHONE_NUMBER = "phone", _("Phone number")
        COMPANY_NAME = "company", _("Company name")
        TEXT = "text", _("Text")
        INTEGER = "int", _("Integer")
        ADDRESS = "address", _("Address")
        DATE = "date", _("Date")


    scheme = models.ForeignKey(Scheme, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=10, choices=ColumnType.choices)
    order = models.PositiveIntegerField()
    parameter_one = models.PositiveIntegerField(null=True, blank=True)
    parameter_two = models.PositiveIntegerField(null=True, blank=True)


class Dataset(models.Model):
    class Meta:
        ordering = ['-created', ]

    class Status(models.TextChoices):
        PROCESSING = "p", _("Processing")
        READY = "r", _("Ready")

    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=Status.choices, default=Status.PROCESSING)
    file = models.FileField(null=True)
    schema = models.ForeignKey(Scheme, on_delete=models.CASCADE)


class PendingJob(models.Model):
    dataset = models.ForeignKey(Dataset, on_delete=models.PROTECT)
    job_id = models.CharField(max_length=200)

