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
        max_budget = form.cleaned_data['max_budget']
        electricity = form.cleaned_data['electricity'] * 1000

        if not max_budget and not electricity:
            form.add_error(None, "Submission Failed: You have to supply more info")
            return self.form_invalid(form)

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
        print(retres)
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
        max_budget = form.cleaned_data['max_budget']
        min_temperature = form.cleaned_data['min_temperature']
        max_temperature = form.cleaned_data['max_temperature']
        price_per_watt = form.cleaned_data['price_per_watt']
        land_area = form.cleaned_data['land_area']
        electricity = form.cleaned_data['electricity']
        materials = form.cleaned_data['materials']

        if not max_budget and not min_temperature and not max_temperature and \
           not price_per_watt and not land_area and not electricity and not materials:

            form.add_error(None, "Submission Failed: You have to supply more info")
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

        total_area = 0

        for key in params:
            if key != 'materials':
                params[key] = "".join(params[key])

        params['electricity'] = float(params['electricity'])
        params['max_budget'] = int(params['max_budget'])

        solution_response = rule_engine.get_solution(params)

        print("Here goes!")
        print(solution_response)

        battery = Battery.objects.all().order_by('-amper_hours').first()

        inverter = Inverter.objects.filter(
            watts__lte=params['electricity']
        ).order_by('-price').first()

        panel_pk = solution_response['panel_pk']

        if not panel_pk:
            redirect(reverse('index'))

        panel = SolarPanel.objects.get(pk=panel_pk)
        context.update({'panel': panel})

        total_price = solution_response['total_price']
        total_price += 2 * battery.price
        total_price += inverter.price

        context.update({'battery': battery})
        context.update({'inverter': inverter})

        context.update({
            'total_price': solution_response['total_price'],
            'total_watt': solution_response['total_watts'],
            'total_panels': solution_response['panel_amount'],
            'total_weight': solution_response['total_weight'],
            'total_area': solution_response['total_area'],
            'cost_per_watt': "{:0.2f}".format(solution_response['cost_per_watt']),
            #'cost_per_hour': "{:0.2f}".format(cost_per_hour)
        })

        return context
