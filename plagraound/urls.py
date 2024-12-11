from django.urls import path
from django.contrib.auth.views import LoginView 
from .views import (
    IoTDataListView,
    IoTDataDetailView,
    create_anomaly_log,
    create_message,
    create_iot_data,
    create_conversation,
    signup,
    update_iot_data,
    iot_data_list,
    delete_iot_data,
    list_messages,
    list_anomaly_logs,
    delete_message,
    update_anomaly_log,
    update_message,
    delete_anomaly_log,
    delete_conversation,
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
    path('delete-anomaly-log/<int:id>/', delete_anomaly_log, name='delete_anomaly_log'),
    path('anomaly-logs/', list_anomaly_logs, name='list_anomaly_logs'),
    path('conversation/create/', create_conversation, name='create_conversation'),
    path('conversation/delete/<int:conversation_id>/', delete_conversation, name='delete_conversation'),
    path('message/create/', create_message, name='create_message'),
    path('message/update/<int:message_id>/', update_message, name='update_message'),
    path('message/delete/<int:message_id>/', delete_message, name='delete_message'),
    path('messages/', list_messages, name='list_messages'),
]

