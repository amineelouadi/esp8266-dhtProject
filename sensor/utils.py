def calculate_temperature_status(temperature):
    """Calculate temperature status based on thresholds"""
    if temperature > 30:
        return 'high'
    elif temperature < 10:
        return 'low'
    return 'normal'

def calculate_humidity_status(humidity):
    """Calculate humidity status based on thresholds"""
    if humidity > 70:
        return 'high'
    elif humidity < 30:
        return 'low'
    return 'normal'

def celsius_to_fahrenheit(celsius):
    """Convert Celsius to Fahrenheit"""
    return (celsius * 9/5) + 32

def process_sensor_data(data):
    """Process and enrich sensor data"""
    temperature = data['temperature']
    humidity = data['humidity']
    
    return {
        'success': True,
        'data': {
            'device': data['device'],
            'temperature': temperature,
            'humidity': humidity,
            'temperature_fahrenheit': celsius_to_fahrenheit(temperature),
            'temperature_status': calculate_temperature_status(temperature),
            'humidity_status': calculate_humidity_status(humidity),
            'status': 'normal'
        }
    }