from django.contrib import admin

from .models import SolarPanel, Battery, Inverter


class SolarPanelAdmin(admin.ModelAdmin):
    """Sortable and editable admin of objects for internal use
    Reused for panaels and inverters.
    """
    list_display = ('name', 'dollar_amount')

    def dollar_amount(self, obj):
        return obj.dollar_amount
    dollar_amount.short_description = 'Price'

class BatteryAdmin(admin.ModelAdmin):
    """Sortable and editable admin of objects for internal use
    Used for Battiers.
    """
    list_display = ('name', 'dollar_amount', 'voltage', 'amper_hours')

    def dollar_amount(self, obj):
        return obj.dollar_amount
    dollar_amount.short_description = 'Price'

admin.site.register(SolarPanel, SolarPanelAdmin)
admin.site.register(Battery, BatteryAdmin)
admin.site.register(Inverter, SolarPanelAdmin)
