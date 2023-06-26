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
    path('GettingAllSlots/',GettingAllSlots.as_view(),name='GettingAllSlots'),

]
