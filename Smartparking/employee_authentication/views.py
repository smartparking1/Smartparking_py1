from rest_framework.views import APIView
from .models import *
from rest_framework.response import Response
from .serializers import *
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import *
from rest_framework.exceptions import AuthenticationFailed
import jwt,datetime





#* this is the Employee Register method

class EmployeeRegister(GenericAPIView,CreateModelMixin):
    serializer_class=EmployeeSerializer
    queryset=EmployeeDetails.objects.all()
    def post(self,request):
        return self.create(request)
    

#* this is the Employeee Login Method and user will get JWT token heare 

class EmployeeLogin(APIView):

    def post(self,request):        
        email=request.data['email_id']
        password=request.data['password']
        employee=EmployeeDetails.objects.filter(email_id=email).first()

        if employee is None:
            raise AuthenticationFailed("Invalid User ")
        if not employee.check_password(password):
            raise AuthenticationFailed("Invalid Password")
        
        payload ={
            'id':employee.email_id,
            'role':employee.role,
            'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=20000),
            'iat':datetime.datetime.utcnow()
        }

        #* creating JWT token by using algorithm HS256
        tocken=jwt.encode(payload,'secret',algorithm='HS256')
        responce =Response()
        responce.data={
                'jwt':tocken
            }
        responce.set_cookie(key='jwt',value=tocken,httponly=True)
        print(responce)
        return responce
    

class GettingAllEmployeeList(APIView):
    def get(self,request):
        authorization_header = request.headers.get('Authorization')
        if not authorization_header:
            raise AuthenticationFailed("Unauthenticated")

        try:
            token = authorization_header.split(' ')[1]
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            print(payload)
            currentuser=payload.get('id')
            print(currentuser)
    
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Authentication expired")
        except :
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