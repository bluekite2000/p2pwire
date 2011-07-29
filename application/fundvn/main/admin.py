from django.contrib import admin
from models import ReverseTransaction,Transaction,Bank,MyBankAccount,Country,City,RecipientBankAccount
admin.site.register(Country)
admin.site.register(City)

admin.site.register(Bank)

admin.site.register(MyBankAccount)

admin.site.register(RecipientBankAccount)

admin.site.register(Transaction)
admin.site.register(ReverseTransaction)