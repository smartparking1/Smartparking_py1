from django.urls import path
from .views import *

urlpatterns = [
    path('addingbuilding/',addingBuilding.as_view(),name='addingBuilding'),
    path('GettingAllBuildings/',GettingAllBuildings.as_view(),name='GettingAllBuildings'),
    path('UpdateBuildingAndDeleteBuildingGettingParticularBuilding/<int:pk>/',UpdateBuildingAndDeleteBuildingGettingParticularBuilding.as_view(),name='UpdateBuildingAndDeleteBuildingGettingParticularBuilding'),
    path('addingFloorAndGetAllFloors/',addingFloorAndGetAllFloors.as_view(),name='insertfloorandgettingall'),
    path('UpdateFloor/<int:pk>/',UpdateFloor.as_view(),name='UpdateFloor'),
    path('DeleteFloorsAndGettingParticularfloor/<int:pk>/',DeleteFloorsAndGettingParticularfloor.as_view(),name='DeleteFloorsAndGettingParticularfloor'),
    path('insertslot/<int:id>/',InsertSlots.as_view(),name='insertslot'),
    path('buildinginactiveandactive/<int:id>/',BuildingInactiveAndactive.as_view(),name = 'buildinginactive'),
    path('SlotUpdate/<int:slot_id>/<str:slot_status>/',SlotUpdate.as_view(),name='SlotUpdate'),
    path('FloorActiveAndInactive/<int:id>/',FloorActiveAndInactive.as_view(),name='FloorActiveAndInactive'),
    path('gettingallslots/',GettingAllSlots.as_view(),name='gettingallslots')

]
