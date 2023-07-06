from .models import *
from rest_framework import serializers
from django.core.files.images import get_image_dimensions
from django.utils.encoding import smart_str
from django.conf import settings
import logging

# class BuildingSerializer(serializers.ModelSerializer) :
#     class Meta :
#         model = BuildingDetails
#         fields = '__all__'

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
        fields = '__all__'

    def update(self, instance, validated_data):
        # Update the fields of SlotDetails instance
        instance.status = validated_data.get('status', instance.status)
       
        # Save the updated SlotDetails instance
        instance.save()
        return instance
    


#* building serilizers

class BuildingSerializer(serializers.ModelSerializer):
    images = serializers.ImageField(write_only=True)
    image_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = BuildingDetails
        fields = ['building_id', 'building_name', 'location', 'status', 'images', 'no_of_floors', 'image_url']

    def validate_images(self, value):
        if value:
            w, h = get_image_dimensions(value)
            if w > 3000 or h > 3000:
                raise serializers.ValidationError("The image dimensions should not exceed 3000 pixels.")
        return value

    def get_image_url(self, obj):
        logging.error("+++++++++++++++++++")
        logging.error(obj)
        if obj.images:
            image_path = smart_str(obj.images)
            return self.context['request'].build_absolute_uri(settings.MEDIA_URL + image_path)
        return None

    def create(self, validated_data):
        image = validated_data.pop('images', None)
        building = BuildingDetails.objects.create(**validated_data)

        if image:
            building.images = image
            building.save()

        return building