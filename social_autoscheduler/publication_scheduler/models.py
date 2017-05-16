from django.conf import settings
from django.db import models
from django.utils.text import Truncator

from schedule.models import Event

from categories.base import CategoryBase


class Category(CategoryBase):
    """Model representing a user created Category.

    Note:
        This model inherits from django-categories CategoryBase model, which
        already implements basic attributes such as name, slug, etc.

    Attributes:
        created_by (:obj:`models.ForeignKey`): user who created the category
            (foreign key to custom User model)
    """
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL)


class SocialNetwork(models.Model):
    """Model representing a social network.

    Attributes:
        name (:obj:`models.CharField`): name of the social network.
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Publication(models.Model):
    """Model representing a publication posted on a social network.

    Attributes:
        author (:obj:`models.ForeignKey`): user who posted the publication
            (foreign key to custom User model).
        social_network (:obj:`models.ForeignKey`): social network the
            publication belongs to (foreign key to `SocialNetwork` model).
        content (:obj:`models.TextField`): text content of the publication.
        category (:obj:`models.ForeignKey`): category in which the publication
            belongs to (foreign key to `Category` model).
    """
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    social_network = models.ForeignKey(SocialNetwork)
    content = models.TextField()
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        related_name='publications'
    )

    def __str__(self):
        return Truncator(self.content).chars(89)


class PublishEvent(Event):
    """Model representing a recurring publication publish event.

    Inherits from django-scheduler `Event` class.

    Attributes:
        social_network (:obj:`models.ForeignKey`): social network the event
            belongs to (foreign key to `SocialNetwork` model).
        category (:obj:`models.ForeignKey`): category in which the event belongs
            to (foreign key to `Category` model).
    """
    social_network = models.ForeignKey(SocialNetwork)
    category = models.ForeignKey(Category, related_name='publish_events')

    def __str__(self):
        return self.title
