from django.shortcuts import render
from .models import *
from .serializers import *
import logging
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import *
from .service import *
from rest_framework.views import APIView


# Create your views here.
class addingBuilding(GenericAPIView,CreateModelMixin,ListModelMixin) :
    queryset = BuildingDetails.objects.all()
    serializer_class = BuildingSerializer
    def post(self,request) :
        authorization_header = request.headers.get('Authorization')
        if checkingAuthentication(authorization_header):
            logging.info("From Building Details POST method")
            return self.create(request)
        else:
             raise AuthenticationFailed("somthing went wrong")
 


    
class GettingAllBuildings(GenericAPIView,ListModelMixin):
        queryset = BuildingDetails.objects.all()
        serializer_class = BuildingSerializer
        def get(self,request) :
            authorization_header = request.headers.get('Authorization')
            if checkingAuthentication(authorization_header):
                logging.info("From Building Details get method")
                logging.info("From Building Details GET method to retrive all objects")
                return self.list(request)
            



class UpdateBuildingAndDeleteBuildingGettingParticularBuilding(GenericAPIView,DestroyModelMixin,RetrieveModelMixin,UpdateModelMixin) :
    queryset = BuildingDetails.objects.all()
    serializer_class = BuildingSerializer
    def put(self,request,**kwargs):
        logging.info("From Building Details PUT method")
        return self.update(request,**kwargs)
    def delete(self,request,**kwargs):
        logging.info("From Building Details DELETE method")
        return self.destroy(request,**kwargs)
    def get(self,request,**kwargs):
        logging.info("From Building Details GET method to get specific data")
        return self.retrieve(request,**kwargs)





class addingFloorAndGetAllFloors(GenericAPIView,CreateModelMixin,ListModelMixin):
    queryset = FloorDetails.objects.all()
    serializer_class = FloorSerializer
    def post(self,request):
        logging.info("From Floor Details POST method")
        return self.create(request)
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






class InsertSlots(APIView):
    def post(self, request, id):
        logging.info("From Building Details POST method")
        floor_details = FloorDetails.objects.get(floor_id=id)
        logging.info("for loop starting")
        for i in range(1, floor_details.no_of_slots+1):
            slot = SlotDetails()
            slot.slot_name = floor_details.floor_no + 's' + str(i)
            slot.status = 'active'
            slot.floor = floor_details
            slot.save()  # Save the slot object to the database
        logging.info("for loop ending")
        return Response(status=status.HTTP_201_CREATED)
    
class GettingAllSlots(GenericAPIView,CreateModelMixin,ListModelMixin):
    queryset = SlotDetails.objects.all()
    serializer_class = SlotSerializer
    def get(self,request):
        logging.info("From Floor Details GET method to retrive all objects")
        return self.list(request)


