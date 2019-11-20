from django.views.generic import TemplateView, FormView
from django.contrib.messages.views import SuccessMessageMixin
from .forms import CostForm


class IndexView(SuccessMessageMixin, FormView):
    template_name = 'home.html'
    form_class = CostForm
    success_url = '/'
    success_message = 'Submission Successful'

    def form_valid(self, form):
        # From here the form is validated and we can do rule chaining etc
        form.add_error(None, "Submission Failed")
        return self.form_invalid(form)
