from django.db import models


class SocialNetwork(models.Model):
    """Model representing a social network.

    Attributes:
        name (:obj:models.CharField): name of the social network.
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
