from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django_tables2 import SingleTableView

from social_autoscheduler.publication_scheduler.models import (Publication,
                                                               SocialNetwork)
from social_autoscheduler.publication_scheduler.tables import PublicationTable


class PublicationCreate(LoginRequiredMixin, CreateView):
    """View managing the creation of `Publication` instances.
    """

    model = Publication
    fields = ['content', 'category', 'social_network']
    success_url = '/'

    def get_form(self, form_class=None):
        """Generates a `ModelForm` and adds a `Submit` button to it.

        Returns:
            form (:obj:`ModelForm`): the generated form.
        """
        form = super().get_form(form_class=form_class)
        form.helper = FormHelper()
        form.helper.add_input(Submit('submit', 'Submit'))
        return form

    def get_initial(self):
        """Generates initial data and sets `social_network` fields.

        Returns:
            initial_data (dict): a dict in the form `{'field_name': field_value}`
        """
        initial_data = super().get_initial()
        if SocialNetwork.objects.count() == 1:
            initial_data.update({'social_network': SocialNetwork.objects.get()})
        return initial_data

    def form_valid(self, form):
        """Sets `author` `Publication` field to current user then redirect to
        success url.
        """
        form.instance.author = self.request.user
        return super().form_valid(form)


class PublicationList(LoginRequiredMixin, SingleTableView):
    """View for showing the list of current user publications.

    Notes:
        django-tables2 `SingleTableView` already inherits from Django `ListView`.
    """

    model = Publication
    table_class = PublicationTable

    def get_queryset(self):
        """Filters and returns all publications created by current user.

        Returns:
            _ (:obj:QuerySet): a Django `QuerySet` instance.
        """
        return Publication.objects.filter(author=self.request.user)
