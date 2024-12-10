# from django.urls import path
# from . import views

# urlpatterns = [
#     path('hello/', views.say_hello)
# ]



# iot/urls.py
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
    IoTDataDeleteView,
)
app_name = 'iot'

urlpatterns = [
    # path("", IoTDataListView.as_view(), name="iotdata-list"),
    path('',  iot_data_list, name='iot_data_list'),
    path("<int:pk>/", IoTDataDetailView.as_view(), name="iotdata-detail"),
    # path("create/", IoTDataCreateView.as_view(), name="iotdata-create"),
    path("create/", create_iot_data, name="iotdata-create"),
    path('create-anomaly-log/', create_anomaly_log, name='create_anomaly_log'),
    path("update/<int:id>/", update_iot_data, name="update-iot-data"),
    # path('delete/<int:id>/', delete_iot_data, npath('create-anomaly-log/', create_anomaly_log, name='create_anomaly_log'),ame='delete_iot_data'), 
    path('delete/<int:id>/', delete_iot_data, name='delete_iot_data'),
    path('create-anomaly-log/', create_anomaly_log, name='create_anomaly_log'),
    path("signup/", signup, name="signup"),
        path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    # path("<int:pk>/update/", IoTDataUpdateView.as_view(), name="iotdata-update"),
    path("<int:pk>/delete/", IoTDataDeleteView.as_view(), name="iotdata-delete"),
]

