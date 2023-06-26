from django.db import models
from BuildingDetails.models import *
from employee_authentication.models import *
# Create your models here.


class VehicleParking(models.Model):
    id = models.AutoField(primary_key=True)
    vehicle_no = models.CharField(max_length=45)
    vehicle_type = models.CharField(max_length=45)
    checkin_time = models.DateTimeField()
    checkout_time = models.DateTimeField(blank=True, null=True)
    parking_amount = models.IntegerField(blank=True, null=True)
    fine_amount = models.IntegerField(blank=True, null=True)
    total_amount = models.IntegerField(blank=True, null=True)
    slot = models.ForeignKey(SlotDetails, models.DO_NOTHING,related_name='related_name')
    checkin_by = models.ForeignKey(EmployeeDetails, models.DO_NOTHING, db_column='checkin_by', related_name='checkins')
    checkout_by = models.ForeignKey(EmployeeDetails, models.DO_NOTHING, db_column='checkout_by', blank=True, null=True,related_name='checkouts')

    class Meta:
        managed = False
        db_table = 'vehicle_parking'