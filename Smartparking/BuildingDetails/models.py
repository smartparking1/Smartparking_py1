from django.db import models


class BuildingDetails(models.Model):
    building_id = models.AutoField(primary_key=True)
    building_name = models.CharField(max_length=45)
    location = models.CharField(max_length=45)
    status = models.CharField(max_length=45)
    no_of_floors = models.CharField(max_length=45)
    images = models.BinaryField()


    class Meta:
        managed = False
        db_table = 'building_details'

class FloorDetails(models.Model):
    floor_id = models.AutoField(primary_key=True)
    floor_no = models.CharField(max_length=45)
    no_of_slots = models.IntegerField()
    status = models.CharField(max_length=45)
    building = models.ForeignKey(BuildingDetails, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'floor_details'

class SlotDetails(models.Model):
    slot_id = models.AutoField(primary_key=True)
    slot_name = models.CharField(max_length=45)
    status = models.CharField(max_length=45)
    floor = models.ForeignKey(FloorDetails, models.DO_NOTHING)
    slot_type = models.CharField(max_length=45, blank=True, null=True)


    class Meta:
        managed = False
        db_table = 'slot_details'



