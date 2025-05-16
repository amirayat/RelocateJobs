from django.contrib import admin

from .models import Token, OAUTH


admin.site.register(Token)
admin.site.register(OAUTH)
