from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView, DetailView, ListView

from iron_bank_app.models import Account, Transaction


class LimitedAccessMixin:

    def get_queryset(self):
        return self.model.objects.filter(customer=self.request.user)


class IndexView(TemplateView):
    template_name = 'index.html'


class SignUpView(CreateView):
    model = User
    form_class = UserCreationForm

    def get_success_url(self):
        return reverse('login_view')


class AccountCreateView(CreateView):
    model = Account
    fields = ('nickname', 'initial_balance')

    def form_valid(self, form):
        object = form.save(commit=False)
        object.customer = self.request.user
        if object.initial_balance > 0:
            object.balance = object.initial_balance
        object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('account_list_view')


class AccountListView(LimitedAccessMixin, ListView):
    model = Account
    template_name = 'iron_bank_app/user_account_list.html'


class AccountDetailView(LimitedAccessMixin, DetailView):
    model = Account


class TransactionCreateView(CreateView):
    model = Transaction
    fields = ('amount', 'description', 'transaction_type')

    def form_invalid(self, form):
        # form.add_error('amount', 'The amount must be a positive value')
        return redirect('overdraft_notice')

    def form_valid(self, form):
        transaction_object = form.save(commit=False)
        transaction_object.account = Account.objects.get(pk=self.kwargs['pk'])
        if transaction_object.amount < 0:
            return super().form_invalid(form)

        if transaction_object.transaction_type == 'd':
            transaction_object.account.balance += transaction_object.amount
        elif transaction_object.transaction_type == 'w':
            if transaction_object.amount > transaction_object.account.balance:
                return self.form_invalid(form)
            else:
                transaction_object.account.balance -= transaction_object.amount

        transaction_object.account.save()
        transaction_object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('account_detail_view', args=(self.kwargs['pk'],))


class TransactionListView(ListView):
    model = Transaction

    def get_queryset(self):
        account = Account.objects.get(pk=self.kwargs['pk'])
        return self.model.objects.filter(account=account)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['account'] = Account.objects.get(pk=self.kwargs['pk'])
        return context


def overdraft_notice_view(request):
    return render(request, 'overdraft.html')
