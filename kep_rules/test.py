from durable.lang import *


# Called in home/views
def get_proposal(input):

    response = {}

    with ruleset('panels'):
        @when_all(m.max_temperature >= 50)
        def is_thin_film(c):
            if 'materials' in response:
                response['materials'].append('thin-film')
            else:
                response['materials'] = ['thin-film', ]

        @when_all(m.max_temperature >= 35)
        def is_mono_crystalline(c):
            if 'materials' in response:
                response['materials'].append('mono-crystalline')
            else:
                response['materials'] = ['mono-crystalline', ]

        @when_all(m.max_temperature < 35)
        def is_poly_crystalline(c):
            if response['materials']:
                response['materials'].append('poly-crystalline')
            else:
                response['materials'] = ['poly-crystalline']

        @when_all((+m.postcode) & (+m.country))
        def calculate_ecost_and_lux(c):
            response['cpw'] = 0.20
            response['lux'] = 100
            c.assert_fact({
                'uid': c.m.uid,
                'cpw': 0.20,
                'lux': 100,
                'inclination': c.m.inclination
            })

        @when_all((+m.lux) & (+m.inclination))
        def calculate_practical_lux(c):
            response['p_lux'] = c.m.lux - (c.m.lux * c.m.inclination)

        @when_all(m.electricity < 500000)
        def small_home_inverter(c):
            response['inverter'] = 'blahblah'

        @when_all( m.electricity >= 500000)
        def commercial_inverter(c):
            response['inverter'] = 'central'

        @when_all((m.electricity < 500000) & (m.grid_type == "on-grid"))
        def user_on_grid(c):
            response['battery'] = False

        @when_all((m.electricity < 500000) & (m.grid_type == "off-grid"))
        def user_on_grid(c):
            response['battery'] = True
            c.assert_fact({'has_battery': True})

        @when_all((m.has_battery == True) | (m.has_smart_monitoring == True))
        def power_conditioning_unit(c):
            response['charge_controller'] = True
            c.assert_fact({'has_charge_controller': True})

    print(input)
    assert_fact('panels', input)
    return response

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