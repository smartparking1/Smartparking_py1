from BuildingDetails.models import  SlotDetails
from .models import Prices
import datetime
from .models import *


def gettingpriceByslotId(slotid,vehicle_type,day):
    slots=SlotDetails.objects.filter(slot_id=slotid).first()
    buildingid=slots.floor.building.building_id
    price=Prices.objects.filter(building=buildingid)
    day= gettingDay(day)
    record=price.filter(vehicle_type=vehicle_type , day_type=day ).first().price
    print(record,'------------------------price of the vehicle----------------------')
    return int(record)



normal_day=['Monday','Tuesday','Wednesday','Thursday','Friday']
weekend_day=['Sunday','Saturday']

def gettingDay(day):
    current_date=day
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
        
def calulatingamout(days_detals,slotid,vehicletype):
    total_amout=0

    for day,hours in days_detals.items():
        print(day,'================',hours)
        total_amout+=hours*gettingpriceByslotId(slotid.slot_id,vehicletype,day)
        print(total_amout)
    print(total_amout,'000000000000000009999999999999999999934567----------')
    return total_amout
        



