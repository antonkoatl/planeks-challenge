from django.forms import inlineformset_factory, ModelForm, Form, IntegerField

from dummy_csv.models import Column, Scheme


class ColumnForm(ModelForm):
    class Meta:
        model = Column
        fields = ['name', 'type', 'order', 'parameter_one', 'parameter_two']

    def is_valid(self):
        pass
        return super(ColumnForm, self).is_valid()


SchemeColumnsFormSet = inlineformset_factory(Scheme, Column, form=ColumnForm, extra=0)


class SchemeForm(ModelForm):
    class Meta:
        model = Scheme
        fields = ['name', 'column_separator', 'string_character']

    def is_valid(self):
        pass
        return super(SchemeForm, self).is_valid()


class DatasetForm(Form):
    rows = IntegerField()
