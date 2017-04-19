# -*- coding: utf-8 -*-

from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        regex=r'^add/$',
        view=views.PublicationCreate.as_view(),
        name='publication-create'
    ),
]