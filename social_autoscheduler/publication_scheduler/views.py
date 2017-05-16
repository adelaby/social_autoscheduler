import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, FormView

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django_tables2 import SingleTableView

from social_autoscheduler.publication_scheduler.forms import EventForm
from social_autoscheduler.publication_scheduler.models import (Publication,
                                                               SocialNetwork,
                                                               Category)
from social_autoscheduler.publication_scheduler.tables import PublicationTable


def set_initial_social_network(initial_data):
    if SocialNetwork.objects.count() == 1:
        initial_data.update({'social_network': SocialNetwork.objects.get()})


class CrispySubmitMixin(object):
    """Mixin adding a `Submit` input helper to a `FormView`'s form.

    Use this mixin with any Django `FormView` class (or inheriting class) to add
    a submit button to the generated form.

    Note:
        Do not forget to render the form's helpers when using `crispy` template
        tag.
    """

    def get_form(self, form_class=None):
        """Generates a `ModelForm` and adds a `Submit` button to it.

        Returns:
            form (:obj:`ModelForm`): the generated form.
        """
        form = super().get_form(form_class=form_class)
        form.helper = FormHelper()
        form.helper.add_input(Submit('submit', 'Submit'))
        return form


class PublicationCreate(LoginRequiredMixin, SuccessMessageMixin,
                        CrispySubmitMixin, CreateView):
    """View managing the creation of `Publication` instances.
    """

    model = Publication
    fields = ['content', 'category', 'social_network']
    success_url = '/'
    success_message = 'Publication created successfully'

    def get_initial(self):
        """Generates initial data and sets `social_network` fields.

        Returns:
            initial_data (dict): a dict in the form `{'field_name': field_value}`
        """
        initial_data = super().get_initial()
        set_initial_social_network(initial_data)
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
            _ (:obj:`QuerySet`): a Django `QuerySet` instance.
        """
        return Publication.objects.filter(author=self.request.user)


class CategoryCreate(LoginRequiredMixin, SuccessMessageMixin,
                     CrispySubmitMixin, CreateView):
    """View managing the creation of `Category` instances.
    """

    model = Category
    fields = ['name']
    success_url = '/'
    success_message = 'Category created successfully'

    def form_valid(self, form):
        """Sets `created_by` `Category` field to current user then redirect to
        success url.
        """
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class PublishEventCreate(LoginRequiredMixin, SuccessMessageMixin,
                         CrispySubmitMixin, FormView):
    """View managing the creation of a `PublishEvent` instance.
    """

    template_name = 'publication_scheduler/rule_form.html'
    form_class = EventForm
    success_url = '/'
    success_message = 'Rule created successfully'

    def get_initial(self):
        """Generates initial data and adds current weekday, time and social
        network to it.
        """
        now = datetime.datetime.now()
        initial_data = {'weekday': now.weekday(), 'time': now.time()}
        set_initial_social_network(initial_data)
        return initial_data

    def get_form_kwargs(self):
        """Generates form kwargs and adds current user to it.
        """
        form_kwargs = super().get_form_kwargs()
        form_kwargs['user'] = self.request.user
        return form_kwargs

    def form_valid(self, form):
        """Ensures event creation before rendering response.
        """
        form.get_or_create_event()
        return super().form_valid(form)
