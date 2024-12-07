# from django.contrib import admin
from django.contrib import admin
from .models import IoTData, AnomalyLog, Conversation, Message

admin.site.register(IoTData)
admin.site.register(AnomalyLog)
admin.site.register(Conversation)
admin.site.register(Message)

# Register your models here.
