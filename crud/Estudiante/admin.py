from django.contrib import admin
from Estudiante.models import Estudiante
from django.contrib.auth.models import Permission

# Register your models here.

admin.site.register(Estudiante)
admin.site.register(Permission)