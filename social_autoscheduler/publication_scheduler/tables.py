from django_tables2 import tables

from social_autoscheduler.publication_scheduler.models import Publication


class PublicationTable(tables.Table):
    """Table class for rendering `Publication` query sets as an HTML table.
    """
    class Meta:
        """Meta data for `PublicationTable` class.
        """
        model = Publication
