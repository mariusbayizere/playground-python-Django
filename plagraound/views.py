from django import forms
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden

from django.http import JsonResponse
import json
from django.shortcuts import render, redirect
from .models import AnomalyLog, Conversation, IoTData
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import login
from .forms import CustomUserCreationForm


# def say_hello(request): 
#     return render(request, 'hello.html', { "name" : "Bayizere marius ", "Postion" : 'His is software Engineering SAND Teachinology'})

# iot/views.py
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import IoTData

class IoTDataListView(ListView):
    model = IoTData
    template_name = "iotdata_list.html"
    context_object_name = "iotdata_list"

class IoTDataDetailView(DetailView):
    model = IoTData
    template_name = "plagraound/iotdata_list.html"
    


# @login_re quired
# def create_iot_data(request):
#     if request.method == 'POST':
#         user = request.user
#         sensor_data = request.POST.get('sensor_data')
#         prediction = request.POST.get('prediction')
#         notes = request.POST.get('notes')
        
#         # Save the data to the database
#         IoTData.objects.create(
#             user=user,
#             sensor_data=sensor_data,
#             prediction=prediction,
#             notes=notes
#         )
#         return redirect('iotdata-list')  # Redirect after saving

#     return render(request, 'iotdata_detail.html')



def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in
            messages.success(request, "Account created successfully!")
            # return redirect('login')  
            return redirect('iot:login')
        else:
            messages.error(request, "Error in form submission.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})


@login_required
def create_iot_data(request):
    if request.method == 'POST':
        user = request.user

        if not user.is_authenticated:
            return HttpResponseForbidden("You must be logged in to create IoT data.")

        sensor_data = request.POST.get('sensor_data', '').strip()
        prediction = request.POST.get('prediction')
        notes = request.POST.get('notes')

        # Validate JSON data
        try:
            sensor_data_json = json.loads(sensor_data) if sensor_data else {}
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format for sensor_data'}, status=400)

        # Save the data to the database
        IoTData.objects.create(
            user=user,
            sensor_data=sensor_data_json,
            prediction=prediction,
            notes=notes
        )
        return render(request, 'iotdata_detail.html')

    return render(request, 'iotdata_detail.html')


class IoTDataForm(forms.ModelForm):
    sensor_data = forms.CharField(
        required=False, 
        widget=forms.Textarea, 
        help_text="Enter sensor data in JSON format"
    )

    class Meta:
        model = IoTData
        fields = ['sensor_data', 'prediction', 'notes']

# Update view
@login_required
def update_iot_data(request, id):
    iot_data = get_object_or_404(IoTData, id=id, user=request.user)

    if request.method == 'POST':
        form = IoTDataForm(request.POST, instance=iot_data)
        if form.is_valid():
            print("Form is valid!")  # Debug
            try:
                # Update fields
                sensor_data = form.cleaned_data['sensor_data']
                if sensor_data:
                    iot_data.sensor_data = json.loads(sensor_data) if isinstance(sensor_data, str) else sensor_data
                iot_data.prediction = form.cleaned_data['prediction']
                iot_data.notes = form.cleaned_data['notes']

                # Save updated instance
                print("IoTData before saving:", iot_data)
                iot_data.save()
                print("IoTData instance saved:", iot_data) 

                return render(request, 'iotdata_detail.html')
                
            except json.JSONDecodeError as e:
                print("JSONDecodeError:", e)  # Debug
                form.add_error('sensor_data', 'Invalid JSON format.')
        else:
            print("Form errors:", form.errors)  # Debug
    else:
        initial_data = {
            'sensor_data': json.dumps(iot_data.sensor_data, indent=2) if iot_data.sensor_data else '',
            'prediction': iot_data.prediction,
            'notes': iot_data.notes,
        }
        form = IoTDataForm(initial=initial_data)

    print("Rendering update page.")  # Debug
    return render(request, 'update_iot_data.html', {'form': form, 'iot_data': iot_data})
    



@login_required
def delete_iot_data(request, id):
    iot_data = get_object_or_404(IoTData, id=id, user=request.user)

    if request.method == 'POST':
        print(f"Deleting IoTData with id {id}")  # Debug
        iot_data.delete()
        print("IoTData deleted successfully.")  # Debug
        # return redirect('iot_list')
        return render(request, 'iotdata_detail.html')
        

    return render(request, 'delete_iot_data.html', {'iot_data': iot_data})



@login_required
def iot_data_list(request):
    iot_data_list = IoTData.objects.filter(user=request.user) 
    return render(request, 'iot_data_list.html', {'iot_data_list': iot_data_list})



# @login_required
# def create_anomaly_log(request):
#     if request.method == 'POST':
#         # Get form data
#         iot_data_id = request.POST.get('iot_data')
#         severity = request.POST.get('severity')
#         resolved = request.POST.get('resolved') == 'on'  # Checkbox value
#         resolution_conversation_id = request.POST.get('resolution_conversation')

#         # Validate IoTData foreign key
#         try:
#             iot_data = IoTData.objects.get(id=iot_data_id)
#         except IoTData.DoesNotExist:
#             return JsonResponse({'error': 'IoTData not found'}, status=400)

#         # Validate severity
#         if severity not in ['low', 'medium', 'high']:
#             return JsonResponse({'error': 'Invalid severity level'}, status=400)

#         # Validate resolution conversation foreign key (optional)
#         resolution_conversation = None
#         if resolution_conversation_id:
#             try:
#                 resolution_conversation = Conversation.objects.get(id=resolution_conversation_id)
#             except Conversation.DoesNotExist:
#                 return JsonResponse({'error': 'Resolution conversation not found'}, status=400)

#         # Create and save the anomaly log
#         AnomalyLog.objects.create(
#             iot_data=iot_data,
#             severity=severity,
#             resolved=resolved,
#             resolution_conversation=resolution_conversation
#         )
#         return JsonResponse({'success': 'Anomaly log created successfully'}, status=200)

#     # Render the form template
#     return render(request, 'create_anomaly_log.html')



@login_required
def create_anomaly_log(request):
    if request.method == 'POST':
        # Get form data
        iot_data_id = request.POST.get('iot_data')
        severity = request.POST.get('severity')
        resolved = request.POST.get('resolved') == 'on'  # Checkbox value
        resolution_conversation_id = request.POST.get('resolution_conversation')

        # Validate IoTData foreign key
        try:
            iot_data = IoTData.objects.get(id=iot_data_id)
        except IoTData.DoesNotExist:
            return render(request, 'create_anomaly_log.html', {'error': 'IoTData not found'})

        # Validate severity
        if severity not in ['low', 'medium', 'high']:
            return render(request, 'create_anomaly_log.html', {'error': 'Invalid severity level'})

        # Validate resolution conversation foreign key (optional)
        resolution_conversation = None
        if resolution_conversation_id:
            try:
                resolution_conversation = Conversation.objects.get(id=resolution_conversation_id)
            except Conversation.DoesNotExist:
                return render(request, 'create_anomaly_log.html', {'error': 'Resolution conversation not found'})

        AnomalyLog.objects.create(
            iot_data=iot_data,
            severity=severity,
            resolved=resolved,
            resolution_conversation=resolution_conversation
        )

        # Use messages to display success
        messages.success(request, 'Anomaly log created successfully')

        return redirect('iot:create_anomaly_log')  # Include namespace in the redirect

    # Render the form template
    return render(request, 'create_anomaly_log.html')



@login_required
def update_anomaly_log(request, id):
    anomaly_log = get_object_or_404(AnomalyLog, id=id)  # Retrieve the anomaly log or raise 404 if not found
    
    if request.method == 'POST':
        # Get updated data from the form
        iot_data_id = request.POST.get('iot_data')
        severity = request.POST.get('severity')
        resolved = request.POST.get('resolved') == 'on'  # Checkbox value
        resolution_conversation_id = request.POST.get('resolution_conversation')

        # Validate IoTData foreign key
        try:
            iot_data = IoTData.objects.get(id=iot_data_id)
        except IoTData.DoesNotExist:
            return render(request, 'update_anomaly_log.html', {'error': 'IoTData not found', 'anomaly_log': anomaly_log})

        # Validate severity
        if severity not in ['low', 'medium', 'high']:
            return render(request, 'update_anomaly_log.html', {'error': 'Invalid severity level', 'anomaly_log': anomaly_log})

        # Validate resolution conversation foreign key (optional)
        resolution_conversation = None
        if resolution_conversation_id:
            try:
                resolution_conversation = Conversation.objects.get(id=resolution_conversation_id)
            except Conversation.DoesNotExist:
                return render(request, 'update_anomaly_log.html', {'error': 'Resolution conversation not found', 'anomaly_log': anomaly_log})

        # Update the anomaly log
        anomaly_log.iot_data = iot_data
        anomaly_log.severity = severity
        anomaly_log.resolved = resolved
        anomaly_log.resolution_conversation = resolution_conversation
        anomaly_log.save()

        # Use messages to display success
        messages.success(request, 'Anomaly log updated successfully')

        return redirect('iot:update_anomaly_log', id=id)  # Redirect to the same page to show the success message

    # Render the form template with the current data
    return render(request, 'update_anomaly_log.html', {'anomaly_log': anomaly_log})