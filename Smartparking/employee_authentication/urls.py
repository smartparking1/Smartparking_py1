from django.urls import path
from .views import *

urlpatterns = [
    path('EmployeeRegister/',EmployeeRegister.as_view(),name='EmployeeRegister'),
    path('EmployeeLogin/',EmployeeLogin.as_view(),name='EmployeeLogin'),
    path('GettingAllEmployeeList/',GettingAllEmployeeList.as_view(),name='GettingAllEmployeeList'),
    path('EmployeeLogout/',EmployeeLogout.as_view(),name='EmployeeLogout'),

]
