from rest_framework.exceptions import ValidationError

def validate_sensor_data(data):
    """Validate incoming sensor data"""
    required_fields = ['temperature', 'humidity', 'device']
    
    # Check required fields
    for field in required_fields:
        if field not in data:
            raise ValidationError({
                'error': f'Missing required field: {field}',
                'required': required_fields
            })
    
    # Validate data types
    if not isinstance(data['temperature'], (int, float)):
        raise ValidationError({'error': 'Temperature must be a number'})
        
    if not isinstance(data['humidity'], (int, float)):
        raise ValidationError({'error': 'Humidity must be a number'})
        
    if not isinstance(data['device'], str):
        raise ValidationError({'error': 'Device must be a string'})