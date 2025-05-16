from django.urls import path
from .views import linkedin_callback


urlpatterns = [
    path('callback/', linkedin_callback, name='linkedin_callback'),
]