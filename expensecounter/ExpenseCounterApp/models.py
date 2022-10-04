from django.db import models

# Create your models here.

class expense_item(models.Model):
    category = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=400)
    cost = models.DecimalField(max_digits=9, decimal_places=2)
    purchase_time = models.DateTimeField('time purchased')
    time_added = models.DateTimeField('time added') #when this was added to this database
    def toString():
        finishedString = category
        finishedString += ", "
        finishedString += name
        finishedString += ", "
        finishedString += cost
        
    def __str__(self):
        return toString()