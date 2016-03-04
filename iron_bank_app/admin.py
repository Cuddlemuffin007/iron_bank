from django.contrib import admin

from iron_bank_app.models import Account, Transaction

admin.site.register([Account, Transaction])