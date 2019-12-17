from durable.lang import *
from decimal import Decimal
from home.models import *
import math
from uuid import uuid4
from django_countries import countries
import logging

logger = logging.getLogger(__name__)
print(__name__)

THIN_FILM_TEMPERATURE = 50
MONO_CRYSTALLINE_TEMPERATURE = 35

ELECTRICITY_HOME_BOUNDARY = 500000

class Rules:
    response = {}

    def __init__(self):
        with ruleset("panels"):

            @when_all(m.max_temperature >= THIN_FILM_TEMPERATURE)
            def is_thin_film(c):
                kind = "thin-film"
                logger.info(f'Max temperature over {THIN_FILM_TEMPERATURE}. Inferencing "{kind}".')
                if "materials" in self.response:
                    self.response["materials"].append(kind)
                else:
                    self.response["materials"] = [
                        kind,
                    ]

            @when_all((m.max_temperature >= MONO_CRYSTALLINE_TEMPERATURE) & (m.max_temperature < THIN_FILM_TEMPERATURE))
            def is_mono_crystalline(c):
                kind = "mono-crystalline"
                logger.info(f'Max temperature over {MONO_CRYSTALLINE_TEMPERATURE}. Inferencing "{kind}".')
                if "materials" in self.response:
                    self.response["materials"].append(kind)
                else:
                    self.response["materials"] = [
                        kind,
                    ]

            @when_all(m.max_temperature < MONO_CRYSTALLINE_TEMPERATURE)
            def is_poly_crystalline(c):
                kind = "poly-crystalline"
                logger.info(f'Max temperature under {MONO_CRYSTALLINE_TEMPERATURE}. Inferencing "{kind}".')
                if "materials" in self.response:
                    self.response["materials"].append(kind)
                else:
                    self.response["materials"] = [kind]

            @when_all((+m.country))
            def calculate_ecost_and_lux(country):
                logger.info(f'Calulating lux and cpw for country {countries[country.m["country"]]}.')
                self.response["cpw"] = 0.20
                self.response["lux"] = 100
                country.assert_fact(
                    {
                        "uid": country.m.uid,
                        "cpw": 0.20,
                        "lux": 100,
                        "inclination": country.m.inclination,
                    }
                )

            @when_all((+m.lux) & (+m.inclination))
            def calculate_practical_lux(c):
                self.response["p_lux"] = c.m.lux - (c.m.lux * c.m.inclination)
                logger.info(f'Based on lux and inclination practical lux is {self.response["p_lux"]}.')

            @when_all(m.electricity < ELECTRICITY_HOME_BOUNDARY)
            def small_home_inverter(c):
                logger.info(f'Electricity requirement smaller than {ELECTRICITY_HOME_BOUNDARY}. Selecting "home" inverter.')
                self.response["inverter"] = "home"

            @when_all(m.electricity >= ELECTRICITY_HOME_BOUNDARY)
            def commercial_inverter(c):
                logger.info(f'Electricity requirement bigger than {ELECTRICITY_HOME_BOUNDARY}. Selecting "central" inverter.')
                self.response["inverter"] = "central"

            @when_all((m.electricity < ELECTRICITY_HOME_BOUNDARY) & (m.grid_type == "on-grid"))
            def user_on_grid(c):
                logger.info(f'Grid type is "on-grid". Setting battery requirement to False.')
                self.response["battery"] = False

            @when_all((m.electricity < ELECTRICITY_HOME_BOUNDARY) & (m.grid_type == "off-grid"))
            def user_on_grid(c):
                logger.info(f'Grid type is "off-grid". Setting battery requirement to True.')
                self.response["battery"] = True
                c.assert_fact({"has_battery": True})

            @when_all((m.has_battery == True) | (m.has_smart_monitoring == True))
            def power_conditioning_unit(c):
                logger.info(f'System has smart monitoring. Setting charge_controller requirement to True.')
                self.response["charge_controller"] = True
                c.assert_fact({"has_charge_controller": True})

            @when_all(+m.shape)
            def available_shapes(c):
                pass

        with ruleset("solution"):
            @when_all(+m.panel_pk & +m.panel_amount)
            def calculate_total_weight(c):
                panel = SolarPanel.objects.get(pk=c.m.panel_pk)
                self.response.update({"total_weight": panel.weight * c.m.panel_amount})
                logger.info(f'Calculated all panels total weight to: {self.response["total_weight"]}.')

            @when_all(+m.panel_pk & +m.panel_amount)
            def calculate_total_area(c):
                panel = SolarPanel.objects.get(pk=c.m.panel_pk)
                self.response.update({"total_area": panel.area * c.m.panel_amount})
                logger.info(f'Calculated all panels total area to: {self.response["total_area"]}.')

            @when_all(+m.total_price & +m.total_watts)
            def calculate_cost_per_watt(c):
                self.response['cost_per_watt'] = c.m.total_price / c.m.total_watts
                logger.info(f'Calculated cost per watt to: {self.response["cost_per_watt"]}.')

            @when_all(+m.total_price & +m.total_watts & +m.location_wattage & +m.panel_efficiency)
            def calculate_cost_per_hour(c):
                total_watt_twenty_years = (c.m.total_watts / 1000) * c.m.location_wattage \
                                          * 365 * 20 * c.m.panel_efficiency
                self.response['cost_per_hour'] = c.m.total_price / total_watt_twenty_years
                logger.info(f'Calculated cost per hour to: {self.response["cost_per_hour"]}.')

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
        assert_fact("panels", input_)
        self.response["electricity"] = input_["electricity"] * 1000
        self.response["max_budget"] = input_["max_budget"]
        return self.response

    def get_solution(self, input_):
        self.response = {}
        input_ = preformat_json(input_)

        panels_budget = 0.4 * input_["max_budget"]
        inverter_budget = input_["max_budget"] * 0.4
        battery_budget = input_["max_budget"] * 0.2
        logger.info(f'Price composition rule splitted budget to: panels - {panels_budget}, inverter - {inverter_budget}, battery - {battery_budget}.')
        response = get_choosen_panel(panels_budget, input_["electricity"])
        response = {
            **response,
            **get_chosen_inverter(inverter_budget, input_["electricity"]),
        }
        response = {
            **response,
            **get_chosen_battery(battery_budget, input_["electricity"]),
        }
        logger.info(f'Chosen solar panel componenent(s): {response["panel_amount"]} x {SolarPanel.objects.get(id=response["panel_pk"])}')
        logger.info(f'Chosen inverter component(s): {response["inverter_amount"]} x {Inverter.objects.get(id=response["inverter_pk"])}')
        logger.info(f'Chosen battery component(s): {response["battery_amount"]} x {Battery.objects.get(id=response["battery_pk"])}')
        response["uid"] = str(uuid4())
        assert_fact("solution", response)
        logger.info(f'Solution for the system found. Proceeding with presentation of final solution.')
        self.response.update(response)
        return self.response


def get_choosen_panel(max_budget, electricity):
    panel = None
    total_price = 0
    total_watts = 0
    total_panels = 0

    logger.info(f'Selecting solar panel using cheapest price criterium.')
    for p in SolarPanel.objects.all():
        panel_amount = round(electricity / p.watts)
        panel_watts = panel_amount * p.watts
        panels_price = panel_amount * p.price

        if (total_price == 0 and (panels_price < max_budget)) or (panels_price < total_price) \
                and panel_watts >= electricity:
            panel = p
            total_price = panels_price
            total_watts = panel_watts
            total_panels = panel_amount

    # fallback
    if not panel:
        logger.info(f'Solar panel optimal solution not found. Using fallback.')
        panel = p
        total_price = panels_price
        total_watts = panel_watts
        total_panels = panel_amount

    return {
        'panel_pk': panel.pk,
        'total_price': total_price,
        'total_watts': total_watts,
        'panel_amount': total_panels
    }


def get_chosen_inverter(max_budget, electricity):
    inverter = None
    total_inverters = 0

    logger.info(f'Selecting inverter using electricity fit criterium.')
    previously_best_inverter = None
    for i in Inverter.objects.all().order_by("watts"):
        if i.watts < electricity:
            previously_best_inverter = i
        else:
            break

    # need to compose of multiple inverters
    if not previously_best_inverter:
        i = Inverter.objects.order_by("-watts").first()
        total_inverters = math.ceil(electricity / i.watts)
        inverter = i
        total_price = total_inverters * i.price
    else:
        i = previously_best_inverter
        total_inverters = 1
        total_price = i.price
        inverter = i

    return {
        "inverter_pk": inverter.pk,
        "inverter_price": inverter.price,
        "total_inverter_price": total_price,
        "inverter_amount": total_inverters,
    }


def get_chosen_battery(max_budget, electricity):
    battery = None
    best_watts = 0
    previously_best_battery = None
    battery_amount = 0

    logger.info(f'Selecting battery using electricity storage fit criterium.')
    for b in Battery.objects.all().order_by("amper_hours"):
        battery_watts = b.amper_hours * b.voltage
        if best_watts < battery_watts < electricity:
            best_watts = battery_watts
            previously_best_battery = b
        else:
            break

    # need to compose of multiple batterys
    if not previously_best_battery:
        # get the battery with largest possible capacity
        b = Battery.objects.order_by("-amper_hours").first()
        battery_watts = b.amper_hours * b.voltage
        battery_amount = max([math.ceil(electricity / battery_watts), 1])
        battery = b
    else:
        b = previously_best_battery
        battery = b
        battery_amount = 1

    total_price = battery.price * battery_amount

    return {
        "battery_pk": battery.pk,
        "battery_price": battery.price,
        "total_battery_price": total_price,
        "battery_amount": battery_amount,
    }


def preformat_json(input_):
    """
    transforms decimal to float so they are JSON serializable
    """
    for k, v in input_.items():
        if isinstance(v, Decimal):
            input_[k] = float(v)
    return input_


"""
user_id = uuid4()
get_proposal({
    'uid': str(user_id),
    'max_temperature': 60,
    'electricity': 2000,
    'location': 'Ams',
    'inclination':0.3,
    'grid_type': 'off-grid'
})
"""
