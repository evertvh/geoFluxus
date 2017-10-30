from django.conf.urls import url

from repair.apps.studyarea import views

urlpatterns = [
    url(r'^$', views.index, name='index'),


    # ex: /stakeholdercategories/3
    url(r'^stakeholdercategories/(?P<stakeholder_category_id>[0-9]+)/$',
        views.stakeholdercategories,
        name='stakeholdercategories'),

    # ex: /stakeholders/3
    url(r'^stakeholders/(?P<stakeholder_id>[0-9]+)/$',
        views.stakeholders,
        name='stakeholders'),
]