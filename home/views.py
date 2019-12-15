from django.views.generic import TemplateView, FormView
from django.contrib.messages.views import SuccessMessageMixin
from kep_rules.test import Rules
from .forms import *
from uuid import uuid4
from .models import SolarPanel, Battery, Inverter
from django.shortcuts import redirect, reverse
from urllib.parse import urlencode, parse_qs


rule_engine = Rules()


class IndexView(TemplateView):
    """Base home page of the application
    
    :param TemplateView: django engine template view
    """
    template_name = 'home.html'


class UserFormView(SuccessMessageMixin, FormView):
    """View for handling collection of user requirements
    
    :param SuccessMessageMixin: mixin for interaction with the user providing feedbacks
    on the form
    :param FormView: django base view for views containing forms
    """
    template_name = 'home.html'
    form_class = HomeUserForm

    success_message = 'Submission Successful'

    def form_valid(self, form):
        """check if the form data is valid so that it can be further processed by the
        knowledge system
        
        :param form: data coming from the form in raw format
        """
        # From here the form is validated and we can do rule chaining etc
        min_budget = form.cleaned_data['min_budget']
        max_budget = form.cleaned_data['max_budget']
        electricity = form.cleaned_data['electricity']

        if not min_budget and not max_budget and not electricity:
            form.add_error(None, "Submission Failed: You have to supply more info")
            return self.form_invalid(form)

        if min_budget and max_budget:
            if min_budget > max_budget:
                form.add_error(None, "Submission Failed: Minimum budget cannot be higher than maximum budget.")
                return self.form_invalid(form)
            elif min_budget == max_budget:
                form.add_error(None, "Submission Failed: Minimum budget cannot be equal to maximum budget.")
                return self.form_invalid(form)

        if min_budget:
            form.cleaned_data['min_budget'] = int(form.cleaned_data['min_budget'])
        if max_budget:
            form.cleaned_data['max_budget'] = int(form.cleaned_data['max_budget'])
        if form.cleaned_data['min_temperature']:
            form.cleaned_data['min_temperature'] = int(form.cleaned_data['min_temperature'])
        if form.cleaned_data['max_temperature']:
            form.cleaned_data['max_temperature'] = int(form.cleaned_data['max_temperature'])

        if form.cleaned_data['grid_type']:
            types = ['on-grid', 'off-grid']
            form.cleaned_data['grid_type'] = types[int(form.cleaned_data['grid_type'])]

        user_id = uuid4()

        rule_req = {'uid': str(user_id)}
        rule_req.update(form.cleaned_data)
        retres = rule_engine.get_proposal(rule_req)
        retres['materials'] = ",".join(retres['materials'])

        return redirect(reverse('solution_view') + "?" + urlencode(retres) + "#solution")


class CommercialFormView(SuccessMessageMixin, FormView):
    """form for the commercial investor. Similar to UserFormView
    
    :param SuccessMessageMixin: mixin for interaction with the user providing feedbacks
    on the form
    :param FormView: django base view for views containing forms
    """
    template_name = 'home.html'
    form_class = CommercialUserForm
    success_url = '/cuser/#get-advice'
    success_message = 'Submission Successful'

    def form_valid(self, form):
        """check if the form data is valid so that it can be further processed by the
        knowledge system
        
        :param form: data coming from the form in raw format
        """
        # From here the form is validated and we can do rule chaining etc
        min_budget = form.cleaned_data['min_budget']
        max_budget = form.cleaned_data['max_budget']
        min_temperature = form.cleaned_data['min_temperature']
        max_temperature = form.cleaned_data['max_temperature']
        price_per_watt = form.cleaned_data['price_per_watt']
        land_area = form.cleaned_data['land_area']
        electricity = form.cleaned_data['electricity']
        materials = form.cleaned_data['materials']

        if not min_budget and not max_budget and not min_temperature and not max_temperature and \
           not price_per_watt and not land_area and not electricity and not materials:

            form.add_error(None, "Submission Failed: You have to supply more info")
            return self.form_invalid(form)

        if min_budget and max_budget:
            if min_budget > max_budget:
                form.add_error(None, "Submission Failed: Minimum budget cannot be higher than maximum budget.")
                return self.form_invalid(form)
            elif min_budget == max_budget:
                form.add_error(None, "Submission Failed: Minimum budget cannot be equal to maximum budget.")
                return self.form_invalid(form)

        return super().form_valid(form)


class ProjectProposal(TemplateView):
    template_name = 'home.html'

    def dispatch(self, request, *args, **kwargs):
        self.params = parse_qs(request.GET.urlencode())
        return super(ProjectProposal, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProjectProposal, self).get_context_data(**kwargs)
        params = self.params

        total_price = 0
        total_watt = 0
        total_weight = 0
        total_area = 0

        for key in params:
            if key != 'materials':
                params[key] = "".join(params[key])

        panel = SolarPanel.objects.filter(
            material__in=params['materials'],
            watts__lte=float(params['electricity'])
        ).order_by('-price').first()

        battery = Battery.objects.all().order_by('-amper_hours').first()

        inverter = Inverter.objects.filter(
            watts__lte=float(params['electricity'])
        ).order_by('-price').first()

        total_price += 10 * panel.price
        total_area += 10 * panel.area
        total_watt += 10 * panel.watts
        total_weight += 10 * panel.weight
        context.update({'panel': panel})

        total_price += 2 * battery.price
        context.update({'battery': battery})

        total_price += inverter.price
        context.update({'inverter': inverter})

        total_watt_twenty_years = (panel.watts/1000) * 4.2 * 365 * 20 * 0.80
        cost_per_hour = total_price / total_watt_twenty_years

        context.update({
            'total_price': total_price,
            'total_watt': total_watt,
            'total_weight': total_weight,
            'total_area': total_area,
            'cost_per_watt': "{:0.2f}".format(total_price / total_watt),
            'cost_per_hour': "{:0.2f}".format(cost_per_hour)
        })

        return context


