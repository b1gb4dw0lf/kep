from django.contrib import admin

from .models import SolarPanel, Battery, Inverter


class SolarPanelAdmin(admin.ModelAdmin):
    """Sortable and editable admin of objects for internal use
    Reused for Battiers and inverters.
    """
    list_display = ('name', 'dollar_amount')

    def dollar_amount(self, obj):
        return obj.dollar_amount
    dollar_amount.short_description = 'Price'


admin.site.register(SolarPanel, SolarPanelAdmin)
admin.site.register(Battery, SolarPanelAdmin)
admin.site.register(Inverter, SolarPanelAdmin)
