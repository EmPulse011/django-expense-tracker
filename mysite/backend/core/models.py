from django.db import models
from django.utils import timezone

class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('food', 'Food'),
        ('transport', 'Transport'),
        ('data', 'Data/Airtime'),
        ('other', 'Other'),
    ]
    title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    date = models.DateField(default=timezone.localdate)

    def __str__(self):
        return self.title


class Budget(models.Model):
    month = models.CharField(max_length=20, unique=True)
    limit = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.month} - {self.limit}"