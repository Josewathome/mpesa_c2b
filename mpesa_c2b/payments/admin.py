from django.contrib import admin

# Register your models here.
from .models import C2BTransaction, B2CTransaction, Account, AccountType,STKTransaction
admin.site.register(C2BTransaction)
admin.site.register(B2CTransaction)
admin.site.register(Account)
admin.site.register(AccountType)
admin.site.register(STKTransaction)