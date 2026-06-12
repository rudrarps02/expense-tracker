from django.db import models

CATEGORY_CHOICES = [
    ('food', 'Food'),
    ('transport', 'Transport'),
    ('shopping', 'Shopping'),
    ('bills', 'Bills'),
    ('health', 'Health'),
    ('other', 'Other'),
]

class Expense(models.Model):
    title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    date = models.DateField()

    class Meta:
                ordering = ['-date']

    def __str__(self):
                return f"{self.title} - {self.amount}"