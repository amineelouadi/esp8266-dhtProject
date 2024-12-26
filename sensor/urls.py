from django.urls import path
from django.views.generic import TemplateView
from .views import SensorDataView

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='dashboard'),
    path('sensor-data/', SensorDataView.as_view(), name='sensor-data'),
]