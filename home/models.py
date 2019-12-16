from django.db import models


class SolarGridComponent(models.Model):
    """Base class for different solar grid system components.
    As all components share similar variables, such as name and price, this base class avoids duplication through inheritance.
    Notice the abstract=True in Meta which means that no table will be created for this model, and it
    is to be used only through inheritance.
    
    :param models: [extension of the Django models engine which establishes the relation with the database]
    """
    name = models.CharField(max_length=255)
    price = models.FloatField(help_text='Price of the panel in "dollars.cents"')
    image_url = models.URLField(max_length=500, blank=True, null=True)

    @property
    def dollar_amount(self):
        """[transforms price into a string representing the formatted price]
        
        :return: [string representing the formatted price]
        :rtype: [type]
        """
        return '$' + str(self.price)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class SolarPanel(SolarGridComponent):
    """[main component of the solar grid system]
    :param SolarGridComponent: [the base solar grid components class]
    """
    shape = models.CharField(choices=[
        ('rectangular', 'Rectangular'),
        ('square', 'Square'),
        ('triangle', 'Triangle')
    ], max_length=255)
    watts = models.IntegerField(help_text='Amount of electricity it produces in Watts')
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

    @property
    def area(self):
        """[calculate the area on the model which has a shape, height and width]
        
        :return: area of the solar panel
        :rtype: [float]
        """
        if self.shape == 'rectangular' or self.shape == 'square':
            return self.height * self.width
        else:
            # Assume it is a perpendicular triangle
            return (self.height * self.width) / 2

    class Meta:
        verbose_name = 'Solar Panel'
        verbose_name_plural = 'Solar Panels'


class Battery(SolarGridComponent):
    """[battery for the solar grid system; essential in off-grid solutions]
    
    :param SolarGridComponent: [the base solar grid components class]
    """
    voltage = models.IntegerField(help_text='Voltage')
    amper_hours = models.IntegerField(help_text='Amper Hours')
    kind = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Battery'
        verbose_name_plural = 'Batteries'


class Inverter(SolarGridComponent):
    """[inverter for the solar grid system (required component)]
    
    :param SolarGridComponent: [the base solar grid components class]
    """
    input_voltage = models.IntegerField(help_text='Input voltage')
    output_voltage = models.IntegerField(help_text='Output voltage')
    watts = models.IntegerField(help_text='Watts')
    kind = models.CharField(max_length=255)
