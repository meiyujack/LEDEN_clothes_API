from django.contrib import admin
from .models import Material, Color, Size, Status, Type

admin.site.register(Material)
admin.site.register(Color)
admin.site.register(Size)
admin.site.register(Status)
admin.site.register(Type)
