from django.db import models

from django.contrib.auth.models import AbstractUser


class EmployeeDetails(AbstractUser):
    employee_name = models.CharField(max_length=45)
    role = models.CharField(max_length=45)
    mobile_number = models.CharField(max_length=45)
    email_id = models.CharField(max_length=45,unique=True)
    password = models.CharField(max_length=45)
    location = models.CharField(max_length=45)

   
    USERNAME_FIELD='email_id'
    REQUIRED_FIELDS=[]
    class Meta:
        db_table="employeedetails"
        managed=False