from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from .models import *
from rest_framework.response import Response
from .serializers import *
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import *
from rest_framework.exceptions import AuthenticationFailed
import jwt,datetime
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from .service_of_empoyee import checkingAuthenticationForAdmin
from django.http import JsonResponse    



#* this is the Employee Register method
image=None
class EmployeeRegister(GenericAPIView,CreateModelMixin):
    serializer_class=EmployeeSerializer
    queryset=EmployeeDetails.objects.all()

    @csrf_exempt
    def post(self,request):
        print(request.data)
        image = request.FILES['image'].read()
        request.data['image']=image
        print(request.data,'7777777777777777777777777777777777777777777777')
        return self.create(request)
    

#* this is the Employeee Login Method and user will get JWT token heare 

class EmployeeLogin(APIView):
    def post(self,request):        
        email=request.data['email_id']
        password=request.data['password']
        employee=EmployeeDetails.objects.filter(email_id=email)
        serializer=EmployeeSerializer(data=employee,many=True)
        serializer.is_valid()
        x=serializer.data


        if employee is None or len(employee)==0:
            raise AuthenticationFailed("Invalid User ")
        employee=employee[0]
        if not employee.check_password(password):
            raise AuthenticationFailed("Invalid Password")

        payload ={
            'id':employee.email_id,
            'role':employee.role,
            'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=600),
            'iat':datetime.datetime.utcnow()
        }

        #* creating JWT token by using algorithm HS256

        tocken=jwt.encode(payload,'secret',algorithm='HS256')
        responce =Response()
        responce.data={
                'jwt':tocken,
                'user':x[0]
                }
        responce.set_cookie(key='jwt',value=tocken,httponly=True)
        return responce
    

class GettingAllEmployeeList(APIView):
    def get(self,request):
        authorization_header = request.headers.get('Authorization')
        if not authorization_header:
            raise AuthenticationFailed("Unauthenticated ok this new")
        try:
            token = authorization_header.split(' ')[1]
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            print(payload)
            currentuser=payload.get('id')
           
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Authentication expired")
        except authorization_header is None :
            raise AuthenticationFailed("Token not found")
        
        employeesList = EmployeeDetails.objects.all()
        serializer = EmployeeSerializer(employeesList, many=True)
        return Response(serializer.data)
    

        
class EmployeeLogout(APIView):
    def post(self,request):
        respone=Response()
        respone.delete_cookie('jwt')
        respone.data ={
            'massage':"succesfully log outed"
        }
        return respone


class EmployeeRoleUpadate(APIView):
    def post(self,request):
        authorization_header = request.headers.get('Authorization')
        try:
            if checkingAuthenticationForAdmin(authorization_header):
                email=request.data['email']
                employee=EmployeeDetails.objects.get(email_id=email)
                print(employee.employee_name)
                if employee.role=='admin':
                    employee.role='employee'
                    employee.save()
                elif employee.role=='employee':
                    employee.role='admin'
                    employee.save()
        except ObjectDoesNotExist as e:
            return JsonResponse({'error': str(e)}, status=400)
        return Response('ok')




class DeletingEmployees(GenericAPIView,DestroyModelMixin):
    queryset=EmployeeDetails.objects.all()
    serializer_class=EmployeeDetails

    def delete(self, request, **kwargs):
        authorization_header = request.headers.get('Authorization')
        try:
            if checkingAuthenticationForAdmin(authorization_header):
                return self.destroy(request,**kwargs)
        except ObjectDoesNotExist as e:
            return JsonResponse({'error': str(e)}, status=400)
        return Response('ok')



