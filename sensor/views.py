from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from .validators import validate_sensor_data
from .utils import process_sensor_data

class SensorDataView(APIView):
    # Variable de classe pour stocker la dernière lecture
    last_reading = {
        'temperature': None,
        'humidity': None,
        'device': None
    }

    def post(self, request):
        try:
            validate_sensor_data(request.data)
            response_data = process_sensor_data(request.data)
            
            # Stocker les données reçues dans le format correct
            SensorDataView.last_reading = {
                'temperature': float(request.data['temperature']),  # Assurez-vous que c'est un nombre
                'humidity': float(request.data['humidity']),       # Assurez-vous que c'est un nombre
                'device': request.data['device']
            }
            
            print(f"Received data from device {request.data['device']}:")
            print(f"Temperature: {request.data['temperature']}°C")
            print(f"Humidity: {request.data['humidity']}%")
            
            return Response(SensorDataView.last_reading, status=status.HTTP_200_OK)  # Renvoyer les mêmes données
            
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'error': 'Internal server error',
                'detail': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        print("GET request - Returning:", SensorDataView.last_reading)  # Debug log
        return Response(SensorDataView.last_reading)