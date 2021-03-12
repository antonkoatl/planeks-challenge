from django.forms import inlineformset_factory, ModelForm, Form, IntegerField, BaseInlineFormSet

from dummy_csv.models import Column, Scheme


class ColumnForm(ModelForm):
    class Meta:
        model = Column
        fields = ['name', 'type', 'order', 'parameter_one', 'parameter_two']

    def is_valid(self):
        pass
        return super(ColumnForm, self).is_valid()


class ColumnsFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super(ColumnsFormSet, self).__init__(*args, **kwargs)
        for form in self.forms:
            if 'DELETE' not in form.changed_data:
                form.empty_permitted = False


SchemeColumnsFormSet = inlineformset_factory(Scheme, Column, form=ColumnForm, extra=0, formset=ColumnsFormSet)


class SchemeForm(ModelForm):
    class Meta:
        model = Scheme
        fields = ['name', 'column_separator', 'string_character']

    def is_valid(self):
        pass
        return super(SchemeForm, self).is_valid()


class DatasetForm(Form):
    rows = IntegerField()
