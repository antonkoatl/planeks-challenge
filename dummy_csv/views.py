import celery
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views import generic
from django.views.generic import CreateView, FormView
from django.views.generic.edit import FormMixin

from dummy_csv.forms import SchemeColumnsFormSet, SchemeForm, ColumnForm, DatasetForm
from dummy_csv.models import Scheme, Column, Dataset
from dummy_csv.tasks import generate_dataset


class SchemasView(LoginRequiredMixin, generic.ListView):
    model = Scheme

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class DatasetsView(LoginRequiredMixin, FormMixin, generic.ListView):
    model = Dataset
    form_class = DatasetForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()

        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        rows = form.cleaned_data['rows']
        dataset = Dataset(schema_id=self.kwargs['pk'])
        dataset.save()
        generate_dataset.delay(dataset.id, rows)
        return super().form_valid(form)

    def get_success_url(self):
        return '#'

    def get_queryset(self):
        return self.model.objects.filter(schema_id=self.kwargs['pk'])


class NewScheme(LoginRequiredMixin, FormView):
    form_class = SchemeForm
    template_name = 'dummy_csv/scheme_form.html'


    def get_context_data(self, **kwargs):
        context = super(NewScheme, self).get_context_data(**kwargs)

        if 'columns' not in context: context['columns'] = SchemeColumnsFormSet(instance=context['form'].instance)

        context['new_column_form'] = ColumnForm(prefix="new")

        return context


    def post(self, request, **kwargs):
        scheme_form = self.get_form()

        columns_form = SchemeColumnsFormSet(instance=scheme_form.instance, **self.get_form_kwargs())

        if scheme_form.is_valid() and columns_form.is_valid():
            return self.form_valid_and_save(scheme_form, columns_form)
        else:
            return self.form_invalid_with_columns(scheme_form, columns_form)

    def get_success_url(self):
        return reverse('schemas')


    def form_valid_and_save(self, scheme_form, columns_form):
        scheme_form.instance.user = self.request.user
        scheme_form.save()
        columns_form.save()
        return super(NewScheme, self).form_valid(scheme_form)


    def form_invalid_with_columns(self, scheme_form, columns_form):
        """If the form is invalid, render the invalid form."""
        return self.render_to_response(self.get_context_data(form=scheme_form, columns=columns_form))


    def get_form(self, form_class=None):
        if 'pk' in self.kwargs:
            if form_class is None:
                form_class = self.get_form_class()
            return form_class(instance=Scheme.objects.get(pk=self.kwargs['pk']), **self.get_form_kwargs())
        else:
            return super(NewScheme, self).get_form(form_class)


class NewColumnt(CreateView):
    model = Column
    fields = ['name', 'type', 'parameter_one', 'parameter_two', 'order']


def delete_schema(request, pk):
    Scheme.objects.get(pk=pk).delete()
    return redirect('schemas')


def poll_state(request):
    """ A view to report the progress to the user """
    dataset_ids = request.GET.getlist('dataset_ids[]')
    ready_datasets = Dataset.objects.filter(status=Dataset.Status.READY, id__in=dataset_ids)
    data = [[x.id, x.file.url] for x in ready_datasets]
    return JsonResponse(data, safe=False)

