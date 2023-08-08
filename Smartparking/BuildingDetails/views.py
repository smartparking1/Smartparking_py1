import datetime
from django.shortcuts import render
import json
from .models import *
from .serializers import *
import logging
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import *
from .service import *
from rest_framework.views import APIView
from .exception import *
from django.http import JsonResponse ,HttpResponse  
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view
from base64 import b64encode
from django.core.serializers import serialize



"""building Oparations """

#* adding BUilding 

@api_view(['POST'])
def addingBuilding(request):
    if request.method == 'POST':
        image = request.FILES['images'].read()
        print(request.FILES['images'],'----------------------')
        building=BuildingDetails()
        building.building_name=request.data['building_name']
        building.location=request.data['location']
        building.status=request.data['status']
        building.no_of_floors=request.data['no_of_floors']
        building.images=image
        building.save()
        return JsonResponse({'message': 'ok'})
    return JsonResponse({'message': 'Failed to upload image'})




#* Getting all buildings

class GettingAllBuildings(GenericAPIView,ListModelMixin):
        queryset = BuildingDetails.objects.all()
        serializer_class = BuildingSerializer
        def get(self,request) :
            authorization_header = request.headers.get('Authorization')
            if checkingAuthenticationForEmployee(authorization_header):
                building_details = BuildingDetails.objects.all()
                data = []
                for building in building_details:
                        image_data = building.images
                        encoded_image = b64encode(image_data).decode('utf-8')
                        data.append({
                        'building_id': building.building_id,
                        'building_name': building.building_name,
                        'location': building.location,
                        'status': building.status,
                        'no_of_floors': building.no_of_floors,
                        'image': encoded_image})
                return JsonResponse(data, safe=False)
            


class UpdateBuildingAndDeleteBuildingGettingParticularBuilding(GenericAPIView,DestroyModelMixin,RetrieveModelMixin,UpdateModelMixin) :
    queryset = BuildingDetails.objects.all()
    serializer_class = BuildingSerializer

    def put(self,request,**kwargs):
        authorization_header = request.headers.get('Authorization')
        if checkingAuthenticationForEmployee(authorization_header):
            logging.info("From Building Details PUT method")
            return self.update(request,**kwargs)
        

    def delete(self,request,**kwargs):
        authorization_header = request.headers.get('Authorization')
        if checkingAuthenticationForEmployee(authorization_header):
            logging.info("From Building Details DELETE method")
            return self.destroy(request,**kwargs)
    def get(self,request,**kwargs):
        authorization_header = request.headers.get('Authorization')
        if checkingAuthenticationForEmployee(authorization_header):
            logging.info("From Building Details GET method to get specific data")
            return self.retrieve(request,**kwargs)

class BuildingInactiveAndactive(APIView) :
    def put(self,request,id):
        building_details = BuildingDetails.objects.get(building_id=id)
        active = 'active'
        inactive = 'inactive'
        if building_details.status == active:
            building_details.status = inactive
            building_details.save()
        else :
            building_details.status = active
            building_details.save()
        floor_details = FloorDetails.objects.filter(building_id=building_details.building_id)
        serializer = FloorSerializer(floor_details, many=True)
        floors = serializer.data
        if building_details.status == inactive:
            floor_details.update(status=inactive)
            for floor in floors:
                if(floor['status'] == active):
                    slot_details = SlotDetails.objects.filter(floor_id=floor['floor_id'])
                    slot_details.update(status = inactive) 
        else :
            floor_details.update(status=active)
            for floor in floors:
                if(floor['status'] == inactive):
                    slot_details = SlotDetails.objects.filter(floor_id=floor['floor_id'])
                    slot_details.update(status = active) 
        return Response(status=status.HTTP_201_CREATED)





"""Floor Oparations """


#* adding floors and getting all floors 
class addingFloorAndGetAllFloors(GenericAPIView,CreateModelMixin,ListModelMixin):
    
    queryset = FloorDetails.objects.all()
    serializer_class = FloorSerializer
    def post(self,request):
        building_name = request.data.get('building')
        location = request.data.get('location')
        building_data=BuildingDetails.objects.filter(building_name=building_name , location=location).first()
        listOfFloors = FloorDetails.objects.filter(building = building_data.building_id)
        count = 0 
        if len(listOfFloors) < int(building_data.no_of_floors) and building_data.building_id:
            for floor in listOfFloors:
                if floor.floor_no != request.data.get('floor_no'):
                    count+=1;
            if(count == len(listOfFloors)):
                request.data['building'] = building_data.building_id
                type_of_slots=request.data.get('floor_slots')
                total_slots=int(type_of_slots.get('four_wheeler'))+int(type_of_slots.get('two_wheeler'))
                request.data['no_of_slots']=total_slots
                logging.info("From Floor Details POST method")
                floordata =  self.create(request)
                slot = InsertSlots()
                slot.post(floordata.data['floor_id'],type_of_slots)
                return floordata
            return Response("saved sucessfully",status=status.HTTP_200_OK)
           
        else :
            try:
                raise FloorRequirementSatisfiedException("All Floors alredy added in ur Buildng😊😊")
            except FloorRequirementSatisfiedException as e:
                return JsonResponse({'error': str(e)}, status=400)
        
    def get(self,request) :
        logging.info("From Floor Details GET method to retrive all objects")

        return self.list(request)


#* Upadating the Floors 
class UpdateFloor(GenericAPIView,UpdateModelMixin):
    queryset = FloorDetails.objects.all()
    serializer_class = FloorsDetailsSerializer
    def put(self,request,**kwargs):
        logging.info("From Floor Details PUT method")
        return self.update(request,**kwargs)



#* Deleting the Floors and getting Floor by id
class DeleteFloorsAndGettingParticularfloor(GenericAPIView,DestroyModelMixin,RetrieveModelMixin,UpdateModelMixin):
    queryset = FloorDetails.objects.all()
    serializer_class = FloorSerializer
    
    def delete(self,request,**kwargs):
        logging.info("From Building Details DELETE method")
        return self.destroy(request,**kwargs)
    def get(self,request,**kwargs):
        logging.info("From Building Details GET method to retrive particular objects")
        return self.retrieve(request,**kwargs)
    

 #* changing the floor status    
class FloorActiveAndInactive(APIView):
    def put(self, request, id):
        floor = FloorDetails.objects.get(floor_id = id)
        if floor.status == 'active':
            floor.status = 'inactive'
            floor.save()
        else :
            floor.status = 'active'
            floor.save()
        logging.info("From Building Details POST method")
        slots = SlotDetails.objects.all()
        
        logging.info("for loop starting")
        for slot in slots:
            if slot.floor_id == id:
                if(floor.status == "inactive"):
                    slot.status = "inactive"
                    slot.save()
                else:
                  slot.status = "active"
                  slot.save()
        logging.info("for loop ending")
        return Response(status=status.HTTP_201_CREATED)
    
    

 #* Updating the Slot status   
class SlotUpdate(APIView) :
    queryset = SlotDetails.objects.all()
    serializer_class = SlotDetailsSerializer
    def put(self,request,slot_id,slot_status):
        try:
            slot = SlotDetails.objects.get(slot_id = slot_id)

            slot.status = slot_status
            slot.save()
            return Response("Updated Sucessfully",status=status.HTTP_201_CREATED)
        except ObjectDoesNotExist as e:
            return JsonResponse({'error': str(e)}, status=400)

#* Inserting the slots 

class InsertSlots(APIView):
    def post(self,id,type_of_slots):
        logging.info("From Building Details POST method")
        floor_details = FloorDetails.objects.get(floor_id=id)
        logging.info("for loop starting")
        print(type_of_slots,'-------------------------------------')
        two_wheeler=int(type_of_slots['two_wheeler'])
        four_wheeler=int(type_of_slots['four_wheeler'])
        for i in range(1,two_wheeler+1):
            slot = SlotDetails()
            slot.slot_name = floor_details.floor_no + '-S' + str(i)
            slot.status = 'active'
            slot.floor = floor_details
            slot.slot_type='two_wheeler'
            slot.save()
            logging.info("for loop ending")
        for i in range(1,four_wheeler+1):
            slot = SlotDetails()
            slot.slot_name = floor_details.floor_no + '-S' + str(two_wheeler+i)
            slot.status = 'active'
            slot.floor = floor_details
            slot.slot_type='four_wheeler'
            slot.save() 
        return Response(status=status.HTTP_201_CREATED)



#* getting the all slots 
class GettingAllSlots(GenericAPIView,ListModelMixin):
    queryset = SlotDetails.objects.all()
    serializer_class = SlotDetailsSerializer
    def get(self,request):
        return self.list(request)

