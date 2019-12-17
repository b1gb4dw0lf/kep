from durable.lang import *
from decimal import Decimal
from home.models import *
import math
from uuid import uuid4


class Rules:
    response = {}

    def __init__(self):
        with ruleset("panels"):

            @when_all(m.max_temperature >= 50)
            def is_thin_film(c):
                if "materials" in self.response:
                    self.response["materials"].append("thin-film")
                else:
                    self.response["materials"] = [
                        "thin-film",
                    ]

            @when_all(m.max_temperature >= 35)
            def is_mono_crystalline(c):
                if "materials" in self.response:
                    self.response["materials"].append("mono-crystalline")
                else:
                    self.response["materials"] = [
                        "mono-crystalline",
                    ]

            @when_all(m.max_temperature < 35)
            def is_poly_crystalline(c):
                if self.response["materials"]:
                    self.response["materials"].append("poly-crystalline")
                else:
                    self.response["materials"] = ["poly-crystalline"]

            @when_all((+m.country))
            def calculate_ecost_and_lux(c):
                self.response["cpw"] = 0.20
                self.response["lux"] = 100
                c.assert_fact(
                    {
                        "uid": c.m.uid,
                        "cpw": 0.20,
                        "lux": 100,
                        "inclination": c.m.inclination,
                    }
                )

            @when_all((+m.lux) & (+m.inclination))
            def calculate_practical_lux(c):
                self.response["p_lux"] = c.m.lux - (c.m.lux * c.m.inclination)

            @when_all(m.electricity < 500000)
            def small_home_inverter(c):
                self.response["inverter"] = "home"

            @when_all(m.electricity >= 500000)
            def commercial_inverter(c):
                self.response["inverter"] = "central"

            @when_all((m.electricity < 500000) & (m.grid_type == "on-grid"))
            def user_on_grid(c):
                self.response["battery"] = False

            @when_all((m.electricity < 500000) & (m.grid_type == "off-grid"))
            def user_on_grid(c):
                self.response["battery"] = True
                c.assert_fact({"has_battery": True})

            @when_all((m.has_battery == True) | (m.has_smart_monitoring == True))
            def power_conditioning_unit(c):
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

            @when_all(+m.panel_pk & +m.panel_amount)
            def calculate_total_area(c):
                panel = SolarPanel.objects.get(pk=c.m.panel_pk)
                self.response.update({"total_weight": panel.area * c.m.panel_amount})

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
        self.response["electricity"] = input_["electricity"]
        self.response["max_budget"] = input_["max_budget"]
        return self.response

    def get_solution(self, input_):
        self.response = {}
        input_ = preformat_json(input_)
        panels_budget = 0.4 * input_["max_budget"]
        response = get_choosen_panel(panels_budget, input_["electricity"])
        inverter_budget = input_["max_budget"] * 0.4
        response = {
            **response,
            **get_chosen_inverter(inverter_budget, input_["electricity"]),
        }
        battery_budget = input_["max_budget"] * 0.2
        response = {
            **response,
            **get_chosen_battery(battery_budget, input_["electricity"]),
        }
        response["uid"] = str(uuid4())
        assert_fact("solution", response)
        self.response.update(response)
        print(response)
        return self.response


def get_choosen_panel(max_budget, electricity):
    panel = None
    total_price = 0
    total_watts = 0
    total_panels = 0

    previously_best_panel = None
    for p in SolarPanel.objects.all().order_by("watts"):
        if p.watts < electricity:
            previously_best_panel = p
        else:
            break

    # need to compose of multiple panels
    total_panels = 0
    if not previously_best_panel:
        p = SolarPanel.objects.order_by("-watts").first()
        panel_amount = math.ceil(electricity / p.watts)
        total_watts = panel_amount * panel_watts
        panel = p
        total_area = panel.area * amount
    else:
        p = previously_best_panel
        panel_amount = 1
        total_watts = p.watts
        panel = p
        total_area = panel.area

    return {
        "panel_pk": panel.pk,
        "total_watts": total_watts,
        "total_area": total_area,
        "panel_amount": panel_amount,
    }


def get_chosen_inverter(max_budget, electricity):
    inverter = None
    inverter_price = 0
    inverter_watts = 0
    inverter_amount = 0

    previously_best_inverter = None
    for i in Inverter.objects.all().order_by("watts"):
        if i.watts < electricity:
            previously_best_inverter = i
        else:
            break

    # need to compose of multiple inverters
    total_inverters = 0
    if not previously_best_inverter:
        i = Inverter.objects.order_by("-watts").first()
        inverter_amount = math.ceil(electricity / i.watts)
        total_watts = inverter_amount * inverter_watts
        inverter = i
        total_price = inverter_amount * i.price
    else:
        i = previously_best_inverter
        inverter_amount = 1
        total_price = i.price
        total_watts = i.watts
        inverter = i

    return {
        "inverter_pk": inverter.pk,
        "inverter_price": inverter_price,
        "inverter_amount": inverter_amount,
    }


def get_chosen_battery(max_budget, amper_hours):
    battery = None
    battery_price = 0
    battery_watts = 0
    battery_amount = 0

    previously_best_battery = None
    for b in Battery.objects.all().order_by("amper_hours"):
        if b.amper_hours < amper_hours:
            previously_best_battery = b
        else:
            break

    # need to compose of multiple batterys
    total_batterys = 0
    if not previously_best_battery:
        # get the battery with largest possible capacity
        b = Battery.objects.order_by("-amper_hours").first()
        battery_amount = math.ceil(amper_hours / b.amper_hours)
    else:
        b = previously_best_battery
        battery_amount = 1

    battery = b
    total_price = b.price * battery_amount
    total_watts = b.amper_hours * battery_amount

    return {
        "battery_pk": battery.pk,
        "battery_price": battery_price,
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
