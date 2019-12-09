from django.views.generic import TemplateView, FormView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from .forms import *


class IndexView(TemplateView):
    template_name = 'home.html'


class UserFormView(SuccessMessageMixin, FormView):
    template_name = 'home.html'
    form_class = HomeUserForm
    success_url = '/'

    success_message = 'Submission Successful'

    def form_valid(self, form):
        # From here the form is validated and we can do rule chaining etc
        min_budget = form.cleaned_data['min_budget']
        max_budget = form.cleaned_data['max_budget']

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
    success_url = '/'
    success_message = 'Submission Successful'

    def form_valid(self, form):
        # From here the form is validated and we can do rule chaining etc
        min_budget = form.cleaned_data['min_budget']
        max_budget = form.cleaned_data['max_budget']

        if min_budget > max_budget:
            form.add_error(None, "Submission Failed: Minimum budget cannot be higher than maximum budget.")
            return self.form_invalid(form)
        elif min_budget == max_budget:
            form.add_error(None, "Submission Failed: Minimum budget cannot be equal to maximum budget.")
            return self.form_invalid(form)

        return super().form_valid(form)
