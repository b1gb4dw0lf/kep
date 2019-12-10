from django.contrib import admin

from .models import SolarPanel


class SolarPanelAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')


admin.site.register(SolarPanel, SolarPanelAdmin)