from django.db import models

class SolarPanel(models.Model):
    name = models.CharField(max_length=255)
    shape = models.CharField(choices=[
        ('rectangular', 'Rectangular'),
        ('square', 'Square'),
        ('triangle', 'Triangle')
    ], max_length=255)
    watt = models.IntegerField(help_text='Amount of electricity it produces in Watts')
    material = models.CharField(choices=[
        ('mono-crystalline', 'Mono-Crystalline'),
        ('poly-crystalline', 'Poly-crystalline'),
        ('thin-film', 'Thin-Film')
    ], max_length=255)
    width = models.IntegerField(help_text='Width of the panel in cm')
    height = models.IntegerField(help_text='Height of the panel in cm')
    thickness = models.IntegerField(help_text='Thickness of the panel in cm')
    area = models.IntegerField(editable=False)
    weight = models.IntegerField(help_text='Weight of the panel in grams')
    price = models.DecimalField(max_digits=15, decimal_places=2,
                                help_text='Price of the panel in "dollars.cents"')
    image_url = models.URLField(max_length=500, blank=True, null=True)

    @property
    def area(self):
        if self.shape == 'rectangular' or self.shape == 'square':
            return self.height * self.width
        else:
            # Assume it is a perpendicular triangle
            return (self.height * self.width) / 2

    @property
    def dollar_amount(self):
        return '$' + str(self.price)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Solar Panel'
        verbose_name_plural = 'Solar Panels'


class Battery(models.Model):
    name = models.CharField(max_length=255)
    voltage = models.IntegerField(help_text='Voltage')
    amper_hours = models.IntegerField(help_text='Amper Hours')
    price = models.DecimalField(max_digits=15, decimal_places=2,
                                help_text='Price of the battery in "dollars.cents"')

    kind = models.CharField(max_length=255)
    image_url = models.URLField(max_length=500, blank=True, null=True)

    @property
    def dollar_amount(self):
        return '$' + str(self.price)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Battery'
        verbose_name_plural = 'Batteries'


class Inverter(models.Model):
    name = models.CharField(max_length=255)
    input_voltage = models.IntegerField(help_text='Input voltage')
    output_voltage = models.IntegerField(help_text='Output voltage')
    watts = models.IntegerField(help_text='Watts')
    price = models.DecimalField(max_digits=15, decimal_places=2,
                                help_text='Price in "dollars.cents"')

    kind = models.CharField(max_length=255)

    image_url = models.URLField(max_length=500, blank=True, null=True)

    @property
    def dollar_amount(self):
        return '$' + str(self.price)

    def __str__(self):
        return self.name
