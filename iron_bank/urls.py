"""iron_bank URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

from iron_bank_app.views import IndexView, SignUpView, AccountListView, AccountCreateView, \
    AccountDetailView, TransactionCreateView, overdraft_notice_view, TransactionListView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', IndexView.as_view(), name='index_view'),
    url(r'^login/$', auth_views.login, name='login_view'),
    url(r'^logout/$', auth_views.logout_then_login, name='logout_view'),
    url(r'^signup/$', SignUpView.as_view(), name='sign_up_view'),
    url(r'^account/create/$', login_required(AccountCreateView.as_view()), name='account_create_view'),
    url(r'^account/$', login_required(AccountListView.as_view()), name='account_list_view'),
    url(r'^account/(?P<pk>\d+)/details/$', login_required(AccountDetailView.as_view()), name='account_detail_view'),
    url(r'^account/(?P<pk>\d+)/create_transaction/$', login_required(TransactionCreateView.as_view()), name='create_transaction_view'),
    url(r'^account/(?P<pk>\d+)/transactions/$', login_required(TransactionListView.as_view()), name='transaction_list_view'),
    url(r'^uh_ohs/', overdraft_notice_view, name='overdraft_notice')
]
