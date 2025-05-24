from django.db import models

class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'pending'),
        ('sucess', 'sucess'), 
        ('failed', 'failed'),
    ]

    name = models.CharField(max_length = 200)
    email = models.EmailField()
    amount = models.DecimalField(max_digits = 10, decimal_places = 2)
    reference = models.CharField(max_length = 20, unique = True,)
    status = models.CharField(max_length=20, choices = STATUS_CHOICES, default ='pending')
    CreatedAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email} - {self.amount} - {self.reference} - {self.status}"