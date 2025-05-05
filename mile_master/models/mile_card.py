from django.db import models
from django.contrib import admin

class MileCard(models.Model):
    distance = models.IntegerField() 
    card_name = models.CharField(max_length=100)  
    
    def __str__(self):
        return f"{self.card_name} - {self.distance} km"
    
@admin.register(MileCard)
class MileCardAdmin(admin.ModelAdmin):
    list_display = ('card_name', 'distance')