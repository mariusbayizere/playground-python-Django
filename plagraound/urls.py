from django.urls import path
from django.contrib.auth.views import LoginView 
from .views import (
    IoTDataListView,
    IoTDataDetailView,
    create_anomaly_log,
    create_iot_data,
    signup,
    update_iot_data,
    iot_data_list,
    delete_iot_data,
    update_anomaly_log,
)
app_name = 'iot'

urlpatterns = [
    path('',  iot_data_list, name='iot_data_list'),
    path("<int:pk>/", IoTDataDetailView.as_view(), name="iotdata-detail"),
    path("create/", create_iot_data, name="iotdata-create"),
    path("update/<int:id>/", update_iot_data, name="update-iot-data"),
    path('delete/<int:id>/', delete_iot_data, name='delete_iot_data'),
    path('create-anomaly-log/', create_anomaly_log, name='create_anomaly_log'),
    path("signup/", signup, name="signup"),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('update-anomaly-log/<int:id>/', update_anomaly_log, name='update_anomaly_log'),
]

