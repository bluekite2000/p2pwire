from django.contrib import admin
from models import ReverseTransaction,Transaction,Bank,MyBankAccount,Country,RecipientBankAccount
admin.site.register(Country)

admin.site.register(Bank)

admin.site.register(MyBankAccount)

admin.site.register(RecipientBankAccount)

admin.site.register(Transaction)
admin.site.register(ReverseTransaction)