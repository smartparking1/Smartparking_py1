from django.shortcuts import render
from .models import *
from .serializers import *
import logging
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import *
from .service import *
from rest_framework.views import APIView
from .exception import *
from django.http import JsonResponse    
from django.core.exceptions import ObjectDoesNotExist



class addingBuilding(GenericAPIView,CreateModelMixin,ListModelMixin) :
    queryset = BuildingDetails.objects.all()
    serializer_class = BuildingSerializer
    def post(self,request) :
        authorization_header = request.headers.get('Authorization')
        if checkingAuthenticationForAdmin(authorization_header):
            logging.error("From Building Details POST method")
            return self.create(request)
        else:
             raise AuthenticationFailed("somthing went wrong")
 


    
class GettingAllBuildings(GenericAPIView,ListModelMixin):
        queryset = BuildingDetails.objects.all()
        serializer_class = BuildingSerializer
        def get(self,request) :
            authorization_header = request.headers.get('Authorization')
            if checkingAuthenticationForEmployee(authorization_header):
                logging.info("From Building Details get method")
                logging.info("From Building Details GET method to retrive all objects")
                return self.list(request)
            


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





class addingFloorAndGetAllFloors(GenericAPIView,CreateModelMixin,ListModelMixin):
    queryset = FloorDetails.objects.all()
    serializer_class = FloorSerializer
    def post(self,request):
        building_name = request.data.get('building')
        location = request.data.get('location')
        building_data = BuildingDetails.objects.filter(building_name=building_name , location=location).first()
        listOfFloors = FloorDetails.objects.filter(building = building_data.building_id)
        count = 0 
        if len(listOfFloors) < int(building_data.no_of_floors) and building_data.building_id:
            for floor in listOfFloors:
                if floor.floor_no != request.data.get('floor_no'):
                    count+=1;
            if(count == len(listOfFloors)):
                request.data['building'] = building_data.building_id
                logging.info("From Floor Details POST method")
                floordata =  self.create(request)
                slot = InsertSlots()
                slot.post(floordata.data['floor_id'])
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

class UpdateFloor(GenericAPIView,UpdateModelMixin):
    queryset = FloorDetails.objects.all()
    serializer_class = FloorsDetailsSerializer
    def put(self,request,**kwargs):
        logging.info("From Floor Details PUT method")
        return self.update(request,**kwargs)




class DeleteFloorsAndGettingParticularfloor(GenericAPIView,DestroyModelMixin,RetrieveModelMixin,UpdateModelMixin):
    queryset = FloorDetails.objects.all()
    serializer_class = FloorSerializer
    
    def delete(self,request,**kwargs):
        logging.info("From Building Details DELETE method")
        return self.destroy(request,**kwargs)
    def get(self,request,**kwargs):
        logging.info("From Building Details GET method to retrive particular objects")
        return self.retrieve(request,**kwargs)
    
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


class InsertSlots(APIView):
    def post(self,id):
        logging.info("From Building Details POST method")
        floor_details = FloorDetails.objects.get(floor_id=id)
        logging.info("for loop starting")
        for i in range(1, floor_details.no_of_slots+1):
            slot = SlotDetails()
            slot.slot_name = floor_details.floor_no + '-S' + str(i)
            slot.status = 'active'
            slot.floor = floor_details
            slot.save()  # Save the slot object to the database
        logging.info("for loop ending")
        return Response(status=status.HTTP_201_CREATED)


class GettingAllSlots(GenericAPIView,ListModelMixin):
    queryset = SlotDetails.objects.all()
    serializer_class = SlotDetailsSerializer
    def get(self,request):
        return self.list(request)


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
    
    

                