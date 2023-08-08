from django.test import TestCase
from datetime import datetime

import BuildingDetails
from .models import VehicleParking, SlotDetails, EmployeeDetails, FloorDetails

class VehicleParkingTestCase(TestCase):
    def setUp(self):
        building = BuildingDetails.objects.create(
            building_name='Building A',
            location='City X',
            status='Active',
            no_of_floors=10
        )
        floor = FloorDetails.objects.create(floor_no='1', no_of_slots=10, status='Active', building=building)
        slot = SlotDetails.objects.create(slot_number='A1', floor=floor)
        employee = EmployeeDetails.objects.create(employee_name='john', password='123456', email='employee@gmail.com')
        checkin_time = datetime.now()
        vehicle = VehicleParking.objects.create(
            vehicle_no='TSD1234',
            vehicle_type='FourWheeler',
            checkin_time=checkin_time,
            slot=slot,
            checkin_by=employee
        )

    def test_vehicle_parking_fields(self):
        vehicle = VehicleParking.objects.get(vehicle_no='TSD1234')
        self.assertEqual(vehicle.vehicle_no, 'TSD1234')
        self.assertEqual(vehicle.vehicle_type, 'FourWheeler')
        self.assertEqual(vehicle.checkin_time.date(), datetime.now().date())
        self.assertIsNone(vehicle.checkout_time)
        self.assertIsNone(vehicle.parking_amount)
        self.assertIsNone(vehicle.fine_amount)
        self.assertIsNone(vehicle.total_amount)
        self.assertEqual(vehicle.slot.slot_number, 'A1')
        self.assertEqual(vehicle.checkin_by.employee_name, 'john')
        self.assertIsNone(vehicle.checkout_by)

    def test_set_checkout_time(self):
        vehicle = VehicleParking.objects.get(vehicle_no='TSD1234')
        checkout_time = datetime.now()
        vehicle.checkout_time = checkout_time
        vehicle.save()
        updated_vehicle = VehicleParking.objects.get(vehicle_no='TSD1234')
        self.assertEqual(updated_vehicle.checkout_time.date(), datetime.now().date())

        # Assert the time part only, as microseconds might not match exactly
        self.assertEqual(updated_vehicle.checkout_time.time(), checkout_time.time())

        # Assert that other fields remain unchanged
        self.assertEqual(updated_vehicle.vehicle_no, 'TSD1234')
        self.assertEqual(updated_vehicle.vehicle_type, 'FourWheeler')
        self.assertEqual(updated_vehicle.checkin_time.date(), datetime.now().date())
        self.assertIsNone(updated_vehicle.parking_amount)
        self.assertIsNone(updated_vehicle.fine_amount)
        self.assertIsNone(updated_vehicle.total_amount)
        self.assertEqual(updated_vehicle.slot.slot_number, 'A1')
        self.assertEqual(updated_vehicle.checkin_by.employee_name, 'john')
        self.assertIsNone(updated_vehicle.checkout_by)