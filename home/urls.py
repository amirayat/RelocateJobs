from django.urls import path

from .views import index, privacy_policy, faq, terms, about_us, permission_denied


urlpatterns = [
    path('', index, name='index'),
    path('privacypolicy/', privacy_policy, name='privacypolicy'),
    path('faq/', faq, name='faq'),
    path('terms/', terms, name='terms'),
    path('about/', about_us, name='about_us'),
    path('permission_denied/', permission_denied, name='permission_denied'),
]
