from durable.lang import *
from decimal import Decimal


class Rules():
    response = {}

    def __init__(self):
        with ruleset('panels'):
            @when_all(m.max_temperature >= 50)
            def is_thin_film(c):
                if 'materials' in self.response:
                    self.response['materials'].append('thin-film')
                else:
                    self.response['materials'] = ['thin-film', ]

            @when_all(m.max_temperature >= 35)
            def is_mono_crystalline(c):
                if 'materials' in self.response:
                    self.response['materials'].append('mono-crystalline')
                else:
                    self.response['materials'] = ['mono-crystalline', ]

            @when_all(m.max_temperature < 35)
            def is_poly_crystalline(c):
                if self.response['materials']:
                    self.response['materials'].append('poly-crystalline')
                else:
                    self.response['materials'] = ['poly-crystalline']

            @when_all((+m.country))
            def calculate_ecost_and_lux(c):
                self.response['cpw'] = 0.20
                self.response['lux'] = 100
                c.assert_fact({
                    'uid': c.m.uid,
                    'cpw': 0.20,
                    'lux': 100,
                    'inclination': c.m.inclination
                })

            @when_all((+m.lux) & (+m.inclination))
            def calculate_practical_lux(c):
                self.response['p_lux'] = c.m.lux - (c.m.lux * c.m.inclination)

            @when_all(m.electricity < 500000)
            def small_home_inverter(c):
                self.response['inverter'] = 'home'

            @when_all(m.electricity >= 500000)
            def commercial_inverter(c):
                self.response['inverter'] = 'central'

            @when_all((m.electricity < 500000) & (m.grid_type == "on-grid"))
            def user_on_grid(c):
                self.response['battery'] = False

            @when_all((m.electricity < 500000) & (m.grid_type == "off-grid"))
            def user_on_grid(c):
                self.response['battery'] = True
                c.assert_fact({'has_battery': True})

            @when_all((m.has_battery == True) | (m.has_smart_monitoring == True))
            def power_conditioning_unit(c):
                self.response['charge_controller'] = True
                c.assert_fact({'has_charge_controller': True})

            @when_all(+m.shape)
            def available_shapes(c):
                pass

    # Called in home/views
    def get_proposal(self, input_):
        """rules inference engine based on durable rules engine

        Arguments:
            input_ {dict} -- [input data to be used for inference]

        Returns:
            response -- dictionary with different properties of the output system
        """
        self.response = {}
        input_ = preformat_json(input_)
        assert_fact('panels', input_)
        self.response['electricity'] = input_['electricity']
        return self.response


def preformat_json(input_):
    """
    transforms decimal to float so they are JSON serializable
    """
    for k, v in input_.items():
        if isinstance(v, Decimal):
            input_[k] = float(v)
    return input_


'''
user_id = uuid4()
get_proposal({
    'uid': str(user_id),
    'max_temperature': 60,
    'electricity': 2000,
    'location': 'Ams',
    'inclination':0.3,
    'grid_type': 'off-grid'
})
'''
