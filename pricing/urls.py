from django.urls import path

from .views import pricing, subscribe


urlpatterns = [
    path('', pricing, name='pricing'),
    path('subscribe/', subscribe, name='subscribe'),
]
