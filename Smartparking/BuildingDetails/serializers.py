from .models import *
from rest_framework import serializers


class BuildingSerializer(serializers.ModelSerializer) :
    class Meta :
        model = BuildingDetails
        fields = '__all__'

class FloorSerializer(serializers.ModelSerializer) :
    # building = BuildingSerializer()
    class Meta :
        model = FloorDetails
        fields = '__all__'
    
    # def create(self, validated_data):
    #     building_data = validated_data.pop('building')
    #     building = BuildingDetails.objects.filter(**building_data).first()
    #     floor = FloorDetails.objects.create(building=building,**validated_data)
    #     return floor
    
class FloorsDetailsSerializer(serializers.ModelSerializer):
    # building = BuildingSerializer(read_only=True)

    class Meta:
        model = FloorDetails
        fields = '__all__'

    
    # def create(self, validated_data):
    #     building_data = validated_data.pop('building')
    #     building_id = building_data.get('building_id')
    #     building, _ = BuildingDetails.objects.get_or_create(building_id=building_id, defaults=building_data)
    #     validated_data['building'] = building
    #     floor = FloorDetails.objects.create(**validated_data)
    #     return floor

class SlotSerializer(serializers.ModelSerializer):
    floor = FloorSerializer()
    class Meta:
        model = SlotDetails
        fields = '__all__'
    
    def create(self, validated_data):
        floor_data = validated_data.pop('floor')
        building_data = floor_data.pop('building')
        building = BuildingDetails.objects.create(**building_data)
        floor = FloorDetails.objects.create(building=building,**floor_data)
        slot = SlotDetails.objects.create(floor=floor,**floor_data)
        return slot
    
class SlotDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SlotDetails
        fields = '_all_'

    def update(self, instance, validated_data):
        # Update the fields of SlotDetails instance
        instance.status = validated_data.get('status', instance.status)
       
        # Save the updated SlotDetails instance
        instance.save()
        return instance