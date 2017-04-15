from django.conf import settings
from django.db import models
from django.utils.text import Truncator

from categories.base import CategoryBase


class Category(CategoryBase):
    """Model representing a user created Category.

    Note:
        This model inherits from django-categories CategoryBase model, which
        already implements basic attributes such as name, slug, etc.

    Attributes:
        created_by (:obj:models.ForeignKey): user who created the category
            (foreign key to custom User model)
    """
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL)


class SocialNetwork(models.Model):
    """Model representing a social network.

    Attributes:
        name (:obj:models.CharField): name of the social network.
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Publication(models.Model):
    """Model representing a publication posted on a social network.

    Attributes:
        author (:obj:models.ForeignKey): user who posted the publication
            (foreign key towards custom User model).
        social_network (:obj:models.ForeignKey): social network the publication
            belongs to (foreign key to `SocialNetwork` model).
        content (:obj:models.TextField): text content of the publication.
    """
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    social_network = models.ForeignKey(SocialNetwork)
    content = models.TextField()

    def __str__(self):
        return Truncator(self.content).chars(89)
