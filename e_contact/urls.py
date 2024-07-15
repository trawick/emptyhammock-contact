from django.urls import path

from . import views

app_name = 'e_contact'

urlpatterns = [
    path('', views.ContactView.as_view(), name='create'),
    path('created/', views.ContactCreated.as_view(), name='created'),
]
