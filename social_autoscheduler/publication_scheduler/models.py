from django.conf import settings
from django.db import models
from django.utils.text import Truncator


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
