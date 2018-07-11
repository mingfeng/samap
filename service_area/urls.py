from django.urls import path

from . import views

app_name = 'service_area'
urlpatterns = [
    path(r'service-area/', views.service_area, name='service-area'),
]
