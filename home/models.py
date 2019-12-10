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
    width = models.IntegerField(help_text='Width of the panel in mm')
    height = models.IntegerField(help_text='Height of the panel in mm')
    thickness = models.IntegerField(help_text='Thickness of the panel in mm')
    area = models.IntegerField(editable=False)
    weight = models.IntegerField(help_text='Weight of the panel in grams')
    price = models.DecimalField(max_digits=15, decimal_places=2,
                                help_text='Price of the panel in "dollars.cents"')

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
