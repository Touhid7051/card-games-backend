from django.db import models
from django.contrib.auth.models import User

class XonTokenBalance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    xon_balance = models.DecimalField(max_digits=10, decimal_places=2)
