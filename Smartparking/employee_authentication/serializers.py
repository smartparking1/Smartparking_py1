from rest_framework import serializers
from .models import *

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model=EmployeeDetails
        fields = ['id','email_id','password','employee_name','role','mobile_number','location']
        extra_kwargs={
            'password':{'write_only':True}
        }

    def create(self, validated_data):
        password=validated_data.pop('password',None)
        instance=self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
        


   