from django.conf.urls import url

from . import views

app_name = 'e_contact'

urlpatterns = [
    url(r'^$', views.ContactView.as_view(), name='create'),
    url(r'^created/$', views.ContactCreated.as_view(), name='created'),
]
