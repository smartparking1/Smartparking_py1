from BuildingDetails.models import *
from .models import Prices
import datetime
from .models import *


def gettingpriceByslotId(slotid,vehicle_type):
    slots=SlotDetails.objects.filter(slot_id=slotid).first()
    buildingid=slots.floor.building.building_id
    price=Prices.objects.filter(building=buildingid)
    day= gettingDay()
    record=price.filter(vehicle_type=vehicle_type , day_type=day ).first().price
    return record



normal_day=['Monday','Tuesday','Wednesday','Thursday','Friday']
weekend_day=['Sunday','Saturday']

def gettingDay():
    current_date=datetime.date.today()
    day=current_date.strftime('%A')
    if(day  not in weekend_day):
        return 'normal'
    return 'weekend'


def checkingCar(carNo):
    vehiclelist=VehicleParking.objects.filter(vehicle_no=carNo)
    print(vehiclelist,'-------------------------')
    for vehicle in vehiclelist:
        if vehicle.checkout_time is None:
            print('okkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk')
            raise Exception('okk')