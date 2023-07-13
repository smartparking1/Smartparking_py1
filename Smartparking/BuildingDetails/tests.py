from django.test import TestCase
from .models import BuildingDetails


class BuildingDetailsTestCase(TestCase):

    def test_create_building_details(self):
        building = BuildingDetails.objects.get(
            building_name='Building A',
            location='City X',
            status='Active',
            no_of_floors='10'
        )
        self.assertEqual(building.building_name, 'Building A')
        self.assertEqual(building.location, 'City X')
        self.assertEqual(building.status, 'Active')
        self.assertEqual(building.no_of_floors, '10')



    def setUp(self):
        self.building_name = 'Building A'
        self.location = 'City X'
        self.status = 'Active'
        self.no_of_floors = '10'

        self.building = BuildingDetails.objects.create(
            building_name=self.building_name,
            location=self.location,
            status=self.status,
            no_of_floors=self.no_of_floors
        )

    def test_update_building_details(self):
        new_building_name = 'Building B'
        new_location = 'City Y'
        new_status = 'Inactive'
        new_no_of_floors = '5'

        self.building.building_name = new_building_name
        self.building.location = new_location
        self.building.status = new_status
        self.building.no_of_floors = new_no_of_floors
        self.building.save()

        # Retrieve the updated building from the database
        updated_building = BuildingDetails.objects.get(pk=self.building.pk)

        # Assert the updated details
        self.assertEqual(updated_building.building_name, new_building_name)
        self.assertEqual(updated_building.location, new_location)
        self.assertEqual(updated_building.status, new_status)
        self.assertEqual(updated_building.no_of_floors, new_no_of_floors)



    


   


    # @classmethod
    # def setUpClass(cls):
    #     super().setUpClass()
    #     cls.building_name = 'Building A'
    #     cls.location = 'City X'
    #     cls.status = 'Active'
    #     cls.no_of_floors = '10'

    # def test_update_building_details(self):
    #     # Update the building details
    #     new_building_name = 'Building A'
    #     new_location = 'City X'
    #     new_status = 'Active'
    #     new_no_of_floors = '10'

    #     # Perform the update without creating an actual object
    #     building = BuildingDetails(
    #         building_name=self.building_name,
    #         location=self.location,
    #         status=self.status,
    #         no_of_floors=self.no_of_floors
    #     )
    #     building.building_name = new_building_name
    #     building.location = new_location
    #     building.status = new_status
    #     building.no_of_floors = new_no_of_floors

    #     # Assert the updated details
    #     self.assertEqual(building.building_name, new_building_name)
    #     self.assertEqual(building.location, new_location)
    #     self.assertEqual(building.status, new_status)
    #     self.assertEqual(building.no_of_floors, new_no_of_floors)

    #     # Check if any values were changed
    #     has_updated = (
    #         building.building_name != self.building_name or
    #         building.location != self.location or
    #         building.status != self.status or
    #         building.no_of_floors != self.no_of_floors
    #     )

    #     if not has_updated:
    #         self.fail("Update did not occur ---------------------------")



# def test_create_building_details(self):
    #     building_name = 'Building A'
    #     location = 'City X'
    #     status = 'Active'
    #     no_of_floors = '10'

    #     building = BuildingDetails(
    #         building_name=building_name,
    #         location=location,
    #         status=status,
    #         no_of_floors=no_of_floors
    #     )

    #     self.assertEqual(building.building_name, building_name)
    #     self.assertEqual(building.location, location)
    #     self.assertEqual(building.status, status)
    #     self.assertEqual(building.no_of_floors, no_of_floors)
    #     # self.assertEqual(building.images, '')