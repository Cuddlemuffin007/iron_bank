from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView, DetailView, ListView
from datetime import date, timedelta

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
        account_object = form.save(commit=False)
        account_object.customer = self.request.user
        if account_object.initial_balance > 0:
            account_object.balance = account_object.initial_balance
        account_object.save()
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
    fields = ('amount', 'description', 'transaction_type', 'destination_account_id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        account = Account.objects.get(pk=self.kwargs['pk'])
        context['account'] = account
        return context

    def form_invalid(self, form):
        # form.add_error('amount', 'The amount must be a positive value')
        return redirect('overdraft_notice')

    def form_valid(self, form):
        transaction_object = form.save(commit=False)
        transaction_object.account = Account.objects.get(pk=self.kwargs['pk'])
        if transaction_object.amount <= 0:
            return super().form_invalid(form)

        if transaction_object.transaction_type == 'd':
            transaction_object.account.balance += transaction_object.amount

        elif transaction_object.transaction_type == 'w':
            if transaction_object.amount > transaction_object.account.balance:
                return self.form_invalid(form)
            else:
                transaction_object.account.balance -= transaction_object.amount

        elif transaction_object.transaction_type == 't':
            try:
                destination_account = Account.objects.get(pk=transaction_object.destination_account_id)
            except Exception:
                return super().form_invalid(form)

            if transaction_object.account == destination_account or transaction_object.account.balance <= 0:
                return super().form_invalid(form)
            else:
                transaction_object.account.balance -= transaction_object.amount
                destination_account.balance += transaction_object.amount
                Transaction.objects.create(account=destination_account, amount=transaction_object.amount,
                                           transaction_type='t', description='received transfer')
                destination_account.save()

        transaction_object.account.save()
        transaction_object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('account_detail_view', args=(self.kwargs['pk'],))


class TransactionListView(ListView):
    model = Transaction

    def get_queryset(self):
        account = Account.objects.get(pk=self.kwargs['pk'])
        start_date = date.today() - timedelta(days=30)
        return self.model.objects.filter(account=account,
                                         account__transaction__post_date__gte=start_date).order_by('-post_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['account'] = Account.objects.get(pk=self.kwargs['pk'])
        # for whatever reason object list was containing dupes of the same instances
        context['object_list'] = set(context['object_list'])

        return context


def overdraft_notice_view(request):
    return render(request, 'overdraft.html')
