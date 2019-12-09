from django.views.generic import TemplateView, FormView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from .forms import *


class IndexView(TemplateView):
    template_name = 'home.html'


class UserFormView(SuccessMessageMixin, FormView):
    template_name = 'home.html'
    form_class = HomeUserForm
    success_url = '/huser/#get-advice'

    success_message = 'Submission Successful'

    def form_valid(self, form):
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

        return super().form_valid(form)


class CommercialFormView(SuccessMessageMixin, FormView):
    template_name = 'home.html'
    form_class = CommercialUserForm
    success_url = '/cuser/#get-advice'
    success_message = 'Submission Successful'

    def form_valid(self, form):
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
