from rest_framework.response import Response
from rest_framework import status

class FixedResponseMixin:
    def get_fixed_response(self, message, data, status_code, error=None):
        
        if status_code in [200, 201]:
      
            response_data = {
                'status': status_code,
                'message': message if message else 'None' ,
                'data': data if data else [] 
            }
            return Response(response_data, status=status_code)
            
        else:
            response_data = {
                'status': status_code,
                'message': message,
                'error': error if error else None
            }
            return Response(response_data, status=status_code)

