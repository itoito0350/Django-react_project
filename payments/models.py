
from django.db import models
from django.contrib.auth.models import User

# Modelo para almacenar las facturas
class Invoice(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(choices=STATUS_CHOICES, max_length=10, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Invoice {self.id} for {self.user.username}"

# Modelo para almacenar los pagos realizados para las facturas
class Payment(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=255)
    transaction_id = models.CharField(max_length=255)
    status = models.CharField(choices=[('SUCCESS', 'Success'), ('FAILED', 'Failed')], max_length=10, default='SUCCESS')

    def __str__(self):
        return f"Payment {self.id} for Invoice {self.invoice.id}"
# Modelo para almacenar los métodos de pago de los usuarios
class PaymentMethod(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    method = models.CharField(max_length=255)
    details = models.TextField()

    def __str__(self):
        return f"Payment Method {self.method} for {self.user.username}"

class Transaction(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    transaction_date = models.DateTimeField(auto_now_add=True)
    transaction_status = models.CharField(choices=[('COMPLETED', 'Completed'), ('PENDING', 'Pending')], max_length=10, default='PENDING')
    transaction_reference = models.CharField(max_length=255)

    def __str__(self):
        return f"Transaction {self.id} for Payment {self.payment.id}"
