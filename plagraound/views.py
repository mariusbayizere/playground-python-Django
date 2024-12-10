from django import forms
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden

from django.http import JsonResponse
import json
from django.shortcuts import render, redirect
from .models import IoTData
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
    iot_data_list = IoTData.objects.filter(user=request.user)  # Ensure only the user's data is displayed
    return render(request, 'iot_data_list.html', {'iot_data_list': iot_data_list})

# @login_required
# def update_iot_data(request, id):
#     iot_data = get_object_or_404(IoTData, id=id, user=request.user)

#     if request.method == 'POST':
#         sensor_data = request.POST.get('sensor_data', '').strip()
#         prediction = request.POST.get('prediction')
#         notes = request.POST.get('notes')

#         # Validate JSON data
#         try:
#             sensor_data_json = json.loads(sensor_data) if sensor_data else {}
#         except json.JSONDecodeError:
#             return JsonResponse({'error': 'Invalid JSON format for sensor_data'}, status=400)

#         # Update the data
#         iot_data.sensor_data = sensor_data_json
#         iot_data.prediction = prediction
#         iot_data.notes = notes
#         iot_data.save()

#         return render(request, 'iotdata_detail.html', {'iot_data': iot_data})

#     return render(request, 'update_iot_data.html', {'iot_data': iot_data})


class IoTDataDeleteView(DeleteView):
    model = IoTData
    template_name = "iotdata_confirm_delete.html"
    success_url = reverse_lazy("iotdata-list")
