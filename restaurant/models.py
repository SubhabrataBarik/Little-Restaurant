from django.db import models

class Booking(models.Model):
    first_name = models.CharField(max_length=200)
    reservation_date = models.DateField()
    reservation_slot = models.IntegerField()

    # def __str__(self):
    #     return self.first_name
