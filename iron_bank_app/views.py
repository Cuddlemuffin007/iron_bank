from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, DetailView, ListView

from iron_bank_app.models import Account


class IndexView(TemplateView):
    template_name = 'index.html'


class SignUpView(CreateView):
    model = User
    form_class = UserCreationForm

    def get_success_url(self):
        return reverse('login_view')


class AccountCreateView(CreateView):
    model = Account
    fields = ('description',)

    def form_valid(self, form):
        object = form.save(commit=False)
        object.customer = self.request.user
        object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('account_list_view')


class AccountListView(ListView):
    model = Account
    template_name = 'iron_bank_app/user_account_list.html'

    def get_queryset(self):
        return Account.objects.filter(customer=self.request.user)


class AccountDetailView(DetailView):
    model = Account

    def get_queryset(self):
        return Account.objects.filter(customer=self.request.user)










