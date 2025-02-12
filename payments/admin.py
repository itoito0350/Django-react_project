from django.contrib import admin
from .models import Invoice, Payment, PaymentMethod, Transaction

admin.site.register(Invoice)
admin.site.register(Payment)
admin.site.register(PaymentMethod)
admin.site.register(Transaction)