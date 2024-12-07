from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
    Custom user model with added phone number field
    """
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        """
        Returns a string representation of the user
        """
        return self.username

    class Meta:
        db_table = "User"


class IoTData(models.Model):
    """
    Model for IoT sensor data
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="iot_data")
    timestamp = models.DateTimeField(auto_now_add=True)
    sensor_data = models.JSONField()
    prediction = models.CharField(max_length=20, choices=[
        ('normal', 'Normal'),
        ('anomaly', 'Anomaly'),
    ])
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        """
        Returns a string representation of the IoT data
        """
        return f"IoTData at {self.timestamp} - Prediction: {self.prediction}"

    class Meta:
        db_table = "IoTData" 


class AnomalyLog(models.Model):
    """
    Model for anomaly detection logs
    """
    iot_data = models.ForeignKey(IoTData, on_delete=models.CASCADE, related_name="anomalies")
    detected_at = models.DateTimeField(auto_now_add=True)
    severity = models.CharField(max_length=20, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ])
    resolved = models.BooleanField(default=False)
    resolution_conversation = models.ForeignKey("Conversation", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        """
        Returns a string representation of the anomaly log
        """
        return f"Anomaly at {self.detected_at} - Severity: {self.severity}"

    class Meta:
        db_table = "AnomalyLog"


class Conversation(models.Model):
    """
    Model for chat conversations
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="conversations")
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        """
        Returns a string representation of the conversation
        """
        return f"Conversation {self.id} with {self.user.username}"

    class Meta:
        db_table = "Conversation"


class Message(models.Model):
    """
    Model for chat messages
    """
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    sender = models.CharField(max_length=10, choices=[
        ('user', 'User'),
        ('chatbot', 'Chatbot'),
    ])
    message_content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Returns a string representation of the message
        """
        return f"Message by {self.sender} at {self.sent_at}"

    class Meta:
        db_table = "Message"
