from django.test import TestCase
from home.models import Battery

# Create your tests here.

class TestCreationOfBatteries(TestCase):
    """test correct handling of connection to database with Django
    and model instantiation
    
    :param TestCase: base Django testing engine
    """
    def setUp(self):
        """function which will be executed before each testCase
        """

        self.test_name = 'Test battery'
        Battery.objects.create(name=self.test_name)

    def test_correct_connection(self):
        self.assertEqual(Battery.objects.all().count(), 1)
        self.assertEqual(Battery.objects.first().name, self.test_name)
