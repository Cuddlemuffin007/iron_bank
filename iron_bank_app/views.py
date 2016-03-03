from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, DetailView


class IndexView(TemplateView):
    template_name = 'index.html'


class SignUpView(CreateView):
    model = User
    form_class = UserCreationForm

    def get_success_url(self):
        return reverse('login_view')


class AccountDetailView(TemplateView):
    template_name = 'iron_bank_app/account_details.html'


