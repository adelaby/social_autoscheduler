import calendar
import datetime

from django import forms
from django.forms import widgets
from django.utils import dates

from schedule.models import Rule

from social_autoscheduler.publication_scheduler.models import (SocialNetwork,
                                                               Category,
                                                               PublishEvent)


def get_round_up_time_tuple(time):
    """Rounds up a `datetime.time` using 10th multiple minute steps.

    Rounds up a given `datetime.time` instance according to the following rules:
        - hour is rounded up cycling from 0 to 23
        - minute is rounded up to nearest 10th multiple cycling from 0 to 50

    Args:
        time (:obj:`datetime.time`): the `datetime.time` instance to be rounded
            up.

    Returns:
        (int, int): the rounded up (hour, minute) tuple
    """
    hour, minute = time.hour, round(time.minute, -1)
    if time.minute >= 55:
        hour = (time.hour + 1) % 24
        minute = 0
    return (hour, minute)


def get_next_year(date):
    """Returns a copy of the given date with an incremented year.

    Args:
        date (:obj:`datetime.date`): the date to increment.

    Returns:
        :obj:`datetime.date`: the incremented date.
    """
    if calendar.isleap(date.year):
        return date + datetime.timedelta(days=365)
    return date.replace(year=date.year + 1)


class SelectTimeWidget(widgets.MultiWidget):
    """Widget to choose a time by selecting hour and minute separately.
    """
    HOUR_CHOICES = [(hour, hour) for hour in range(0, 24)]
    MINUTE_CHOICES = [(minute, minute) for minute in range(0, 60, 10)]

    def __init__(self, attrs=None):
        """Initializes widget with an hour and a minute select widgets.

        Note:
            Minutes are tenth multiples.
        """
        _widgets = [
            widgets.Select(attrs=attrs, choices=self.HOUR_CHOICES),  # hours
            widgets.Select(attrs=attrs, choices=self.MINUTE_CHOICES),  # minutes
        ]
        super().__init__(_widgets, attrs=attrs)

    def decompress(self, value):
        """Splits given `datetime.time` instance in a rounded up hour, minutes
        tuple.

        Returns:
            (int, int): rounded up (hour, minutes) tuple.
        """
        if value:
            return get_round_up_time_tuple(value)
        return [None, None]

    def value_from_datadict(self, data, files, name):
        """Puts back separate widgets values into a proper `datetime.time`
        instance.

        Returns:
            :obj:`time`: the `datetime.time` instance.
        """
        hour, minute = [
            widget.value_from_datadict(data, files, name + '_%s' % i)
            for i, widget
            in enumerate(self.widgets)
        ]
        return datetime.time(hour=int(hour), minute=int(minute))


class EventForm(forms.Form):
    """Form used to create a recurring publication publish event.
    """

    WEEKDAY_CHOICES = [(weekday_number, weekday_name)
                       for weekday_number, weekday_name
                       in dates.WEEKDAYS.items()]

    weekday = forms.ChoiceField(choices=WEEKDAY_CHOICES)
    time = forms.TimeField(widget=SelectTimeWidget())
    social_network = forms.ModelChoiceField(
        queryset=SocialNetwork.objects.all()
    )
    category = forms.ModelChoiceField(queryset=None)

    def __init__(self, *args, user, **kwargs):
        """Initializes the form, sets `user` attribute and `category` queryset.

        Args:
            user (:obj:`User`): the user who wants to create the `PublishEvent`.
        """
        super().__init__(*args, **kwargs)
        self.user = user
        self.fields['category'].queryset = Category.objects.filter(
            created_by=self.user
        )

    def clean_category(self):
        """Ensures selected `category` belongs to current user.
        """
        category = self.cleaned_data['category']
        if category.created_by != self.user:
            raise forms.ValidationError('You must choose a category you own')
        return category

    def get_or_create_event(self):
        """Gets or Create a `PublishEvent` instance matching the form criterias.

        Returns:
            publish_event (:obj:`PublishEvent`): the retrieved or created
                `PublishEvent` instance.
            created (bool): a boolean telling whether the `PublishEvent` has
                been created or retrieved.
        """
        social_network = self.cleaned_data['social_network']
        weekday = int(self.cleaned_data['weekday'])
        time = self.cleaned_data['time']
        category = self.cleaned_data['category']
        now = datetime.datetime.now()
        time_description = ' every {weekday} at {time}'.format(
            weekday=dates.WEEKDAYS[weekday],
            time=time
        )
        rule, created = Rule.objects.get_or_create(
            name=time_description.strip().capitalize(),
            description='Event occurring' + time_description,
            frequency='WEEKLY',
            params=';'.join([
                'byweekday:%s' % weekday,
                'byhour:%s' % time.hour,
                'byminute:%s' % time.minute,
            ])
        )
        publish_event, created = PublishEvent.objects.get_or_create(
            rule=rule,
            creator=self.user,
            start=now,
            end=get_next_year(now),
            title=('{social_network} post' + time_description).format(
                social_network=social_network,
            ),
            category=category,
            social_network=social_network,
        )
        return publish_event, created

