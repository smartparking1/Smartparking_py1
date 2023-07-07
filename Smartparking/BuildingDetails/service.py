

from rest_framework.exceptions import AuthenticationFailed
import jwt
from .models import *
from employee_authentication.models import *



def checkingAuthenticationForEmployee(authorization_header):
            if not authorization_header:
                    raise AuthenticationFailed("Unauthenticated")
            try:
                token = authorization_header.split(' ')[1]
                payload = jwt.decode(token, 'secret', algorithms=['HS256'])
                print(payload)
                currentuser=payload.get('id')
                print(currentuser)
                current_employeeRole=EmployeeDetails.objects.get(email_id=currentuser).role
                print(current_employeeRole)
            except jwt.ExpiredSignatureError:
                 raise AuthenticationFailed("Authentication expired")
            return True


def checkingAuthenticationForAdmin(authorization_header):
            if not authorization_header:
                    raise AuthenticationFailed("Unauthenticated")
            try:
                token = authorization_header.split(' ')[1]
                payload = jwt.decode(token, 'secret', algorithms=['HS256'])
                print(payload)
                currentuser=payload.get('id')
                print(currentuser)
                current_employeeRole=EmployeeDetails.objects.get(email_id=currentuser).role
                print(current_employeeRole)
            except jwt.ExpiredSignatureError:
                 raise AuthenticationFailed("Authentication expired")
            except authorization_header is None:
                 raise AuthenticationFailed("Token not found")
            if current_employeeRole!='admin':
                raise AuthenticationFailed("You are unauthorized to perform this action.")
            return True
                    