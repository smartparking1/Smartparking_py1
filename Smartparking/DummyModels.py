# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class BuildingDetails(models.Model):
    building_id = models.AutoField(primary_key=True)
    building_name = models.CharField(max_length=45)
    location = models.CharField(max_length=45)
    status = models.CharField(max_length=45)
    no_of_floors = models.CharField(max_length=45)
    images = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'building_details'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('Employeedetails', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Employeedetails(models.Model):
    id = models.BigAutoField(primary_key=True)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()
    employee_name = models.CharField(max_length=45)
    role = models.CharField(max_length=45)
    mobile_number = models.CharField(max_length=45)
    email_id = models.CharField(unique=True, max_length=45)
    password = models.CharField(max_length=10000)
    location = models.CharField(max_length=45)
    image = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'employeedetails'


class FloorDetails(models.Model):
    floor_id = models.AutoField(primary_key=True)
    floor_no = models.CharField(max_length=45)
    no_of_slots = models.IntegerField()
    status = models.CharField(max_length=45)
    building = models.ForeignKey(BuildingDetails, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'floor_details'


class Prices(models.Model):
    building = models.ForeignKey(BuildingDetails, models.DO_NOTHING)
    day_type = models.CharField(max_length=45, blank=True, null=True)
    vehicle_type = models.CharField(max_length=45, blank=True, null=True)
    price = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'prices'


class SlotDetails(models.Model):
    slot_id = models.AutoField(primary_key=True)
    slot_name = models.CharField(max_length=45)
    status = models.CharField(max_length=45)
    floor = models.ForeignKey(FloorDetails, models.DO_NOTHING)
    slot_type = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'slot_details'


class VehicleParking(models.Model):
    vehicle_no = models.CharField(max_length=45)
    vehicle_type = models.CharField(max_length=45)
    checkin_time = models.DateTimeField()
    checkout_time = models.DateTimeField(blank=True, null=True)
    parking_amount = models.IntegerField(blank=True, null=True)
    fine_amount = models.IntegerField(blank=True, null=True)
    total_amount = models.IntegerField(blank=True, null=True)
    slot = models.ForeignKey(SlotDetails, models.DO_NOTHING)
    checkin_by = models.ForeignKey(Employeedetails, models.DO_NOTHING, db_column='checkin_by')
    checkout_by = models.ForeignKey(Employeedetails, models.DO_NOTHING, db_column='checkout_by', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vehicle_parking'
