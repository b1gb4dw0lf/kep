from django.contrib import admin

from .models import SolarPanel, Battery, Inverter


class SolarPanelAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')


admin.site.register(SolarPanel, SolarPanelAdmin)
admin.site.register(Battery, SolarPanelAdmin)
admin.site.register(Inverter, SolarPanelAdmin)
