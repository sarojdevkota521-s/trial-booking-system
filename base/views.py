from inspect import signature
from urllib import request
import uuid
from django.shortcuts import render,redirect
from .models import Vehicle,Package,Booking,TrialTime,Timeslot
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.views import View as view
from django.urls import reverse
from django.utils import timezone
from django.db.models import Exists, OuterRef
from django.contrib.auth.decorators import login_required
# Create your views here.

def home(request):
    c=Vehicle.objects.filter(catogery__name='car')
    b=Vehicle.objects.filter(catogery__name='bike')
    
    
    context={
        'car':c,
        'bike':b
    }
    return render(request, 'home.html',context)
def about(request):
    booked_vehicles = Booking.objects.filter(is_active=True).count()
    booked_car= Booking.objects.filter(is_active=True, vehicle__catogery__name='car').count()
    booked_bike= Booking.objects.filter(is_active=True, vehicle__catogery__name='bike').count()
    available_vehicles = Vehicle.objects.count() 
    available_car = Vehicle.objects.filter(catogery__name='car').count()
    available_bike = Vehicle.objects.filter(catogery__name='bike').count() 
    context = {
       
        'available_vehicles': available_vehicles,
        'available_car': available_car,
        'available_bike': available_bike
    }

    return render(request, 'about.html', context)

def detail(request):
    # time_slots=Timeslot.objects.all()
    

    # context={
    #     'time_slots':time_slots,
    #     'availability':availability

    # }
#     vehicles = Vehicle.objects.all()
#     time_slots = Timeslot.objects.all()
   

#     bookings = Booking.objects.filter(is_active=True).values_list(
#     'vehicle_id', 'trial_time__time_id'
# )
#     ts=set()
#     for (v_id, t_id) in bookings:
#         ts.add((v_id, t_id))
   
    
     
#     at=TrialTime.objects.all().values_list(
#     'vehicle_id', 'time_id'
# )
   
#     context = {
#         'vehicles': vehicles,
#         'time_slots': time_slots,
#         "total":at,
       
#         'availability': ts
        
#     }

#     return render(request, 'detail.html',context)
    vehicles = Vehicle.objects.all()
    time_slots = Timeslot.objects.all()

    # Get active bookings as a set of (vehicle_id, time_id) for fast lookup
    booked_pairs = set(
        Booking.objects.filter(is_active=True).values_list('vehicle_id', 'trial_time__time_id')
    )

    # Build a "grid" of data
    table_data = []
    for vehicle in vehicles:
        row = {
            'vehicle_name': vehicle.name,
            'slots': []
        }
        for slot in time_slots:
            # Check if this specific vehicle and time slot is in our booked set
            is_booked = (vehicle.id, slot.id) in booked_pairs
            row['slots'].append(is_booked)
        table_data.append(row)

    context = {
        'time_slots': time_slots,
        'table_data': table_data,
    }
    return render(request, 'detail.html', context)

def contact(request):
    return render(request, 'contact.html')

# def booking(request):
#     # from home page (?vehicle=ID)
#     selected_vehicle_id = request.GET.get('vehicle')
#     selected_vehicle_name=request.GET.get('type')
#     packages=Package.objects.filter(vehicle__name=selected_vehicle_name)
#     vehicles= Vehicle.objects.filter(catogery__name=selected_vehicle_name)
    
#     # Available TrialTimes
#     active_booked_timeslot_ids = Booking.objects.filter(
#     is_active=True,
#     vehicle_id=selected_vehicle_id).values_list( 'trial_time__time_id', flat=True)

#     available_trial_times = Timeslot.objects.exclude(
#     id__in=active_booked_timeslot_ids)

#     
#     if request.method == 'POST':
#         fname = request.POST.get('fname')
#         phone = request.POST.get('phone')
#         message = request.POST.get('message')
#         time_id = request.POST.get('time')
        

#         vehicle_id = request.POST.get('vehicle')
#         package_id = request.POST.get('package')
        
#        
#         if not (fname and phone and vehicle_id and package_id):
#             messages.error(request, 'All fields are required')
#             return render(request, 'booking.html', {
#                 "packages": packages,
#                 'vehicle': vehicles,
#                 'selected_vehicle_id': selected_vehicle_id,
#                 'selected_vehicle_name': selected_vehicle_name,
#                 'available_trial_times': available_trial_times,
#                 'error': 'All fields are required'
#             })

#         selected_vehicle = get_object_or_404(Vehicle, id=vehicle_id)
#         selected_package = get_object_or_404(Package, id=package_id)

#         selected_trial_time = get_object_or_404(TrialTime, time_id=time_id, vehicle_id=selected_vehicle_id)

#         if Booking.objects.filter(
#         trial_time=selected_trial_time,
#         is_active=True).exists():
#             messages.error(request, 'Selected time slot is already booked.')
#             return render(request, 'booking.html', {
#         "packages": packages,
#         'vehicle': vehicles,
#         'available_trial_times': available_trial_times,
#         'selected_vehicle_id': selected_vehicle_id,
#         'selected_vehicle_name': selected_vehicle_name,
#     })
    
        
#     payment_uuid = str(uuid.uuid4())

#     Booking.objects.create(
#     customer_name=fname,
#     phone_number=phone,
#     trial_time=selected_trial_time,
#     message=message,
#     vehicle=selected_vehicle,
#     package=selected_package,
#     payment_uuid=payment_uuid,
#     payment_status=False
# )
   

#     return redirect(
#     reverse('esewa') + f'?p={selected_package.id}&uuid={payment_uuid}'
# )
@login_required(login_url='login')
def booking(request):

    selected_vehicle_id = request.GET.get('vehicle')
    selected_vehicle_name = request.GET.get('type')

    packages = Package.objects.filter(vehicle__name=selected_vehicle_name)
    vehicles = Vehicle.objects.filter(catogery__name=selected_vehicle_name)

    active_booked_timeslot_ids = Booking.objects.filter(
        is_active=True,
        vehicle_id=selected_vehicle_id
    ).values_list('trial_time__time_id', flat=True)

    available_trial_times = Timeslot.objects.exclude(
        id__in=active_booked_timeslot_ids
    )

    

    #  HANDLE POST AND RETURN
    if request.method == 'POST':
        fname = request.POST.get('fname')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        time_id = request.POST.get('time')
        vehicle_id = request.POST.get('vehicle')
        package_id = request.POST.get('package')

        if not all([fname, phone, time_id, vehicle_id, package_id]):
            messages.error(request, "All fields are required")
            return redirect(request.path)

        selected_vehicle = get_object_or_404(Vehicle, id=vehicle_id)
        selected_package = get_object_or_404(Package, id=package_id)
        selected_trial_time = get_object_or_404(
            TrialTime,
            time_id=time_id,
            vehicle_id=selected_vehicle_id
        )


        payment_uuid = str(uuid.uuid4())

        Booking.objects.create(
            user=request.user,
            customer_name=fname,
            phone_number=phone,
            trial_time=selected_trial_time,
            message=message,
            vehicle=selected_vehicle,
            package=selected_package,
            payment_uuid=payment_uuid,
            payment_status=False
        )

        return redirect(
            reverse('esewa') + f'?p={selected_package.id}&uuid={payment_uuid}'
        )

   
    return render(request, 'booking.html', {
        'packages': packages,
        'vehicle': vehicles,
        'available_trial_times': available_trial_times,
        'selected_vehicle_id': selected_vehicle_id,
        'selected_vehicle_name': selected_vehicle_name
    })
   
import uuid
import hashlib
import hmac
import base64
from django.views import View
from django.http import HttpResponse

from django.views import View
from django.shortcuts import render
from django.http import HttpResponse
import uuid, hmac, hashlib, base64
from .models import Package

class EsewaView(View):
    def get(self, request, *args, **kwargs):

        package_id = request.GET.get('p')
        if not package_id:
            return HttpResponse("Missing package id", status=400)

        package = Package.objects.get(id=package_id)

        price = format(package.price, '.2f') 
        total_amount = price 
        transaction_uuid = request.GET.get('uuid')
        if not transaction_uuid:
            return HttpResponse("Missing transaction UUID", status=400)
        product_code = "EPAYTEST"
        signed_field_names = "total_amount,transaction_uuid,product_code"

        message = price + transaction_uuid + product_code

        secret_key = "8gBm/:&EnhH.1/q"

        signature = base64.b64encode(
            hmac.new(
                secret_key.encode(),
                message.encode(),
                hashlib.sha256
            ).digest()
        ).decode()
        signing_string = (
    f"total_amount={total_amount},"
    f"transaction_uuid={transaction_uuid},"
    f"product_code={product_code}"
)

        secret_key = "8gBm/:&EnhH.1/q"

        signature = base64.b64encode(
        hmac.new(
            secret_key.encode("utf-8"),
            signing_string.encode("utf-8"),
            hashlib.sha256
        ).digest()
    ).decode("utf-8")
        context = {
            "price": price,
            "total_amount": price,
            "transaction_uuid": transaction_uuid,
            "product_code": product_code,
            "signed_field_names": signed_field_names,
            "signature": signature,
        }
        
        return render(request, "esewa.html", context)
    
import json

def esewa_success(request):
    data = request.GET.get('data')

    if not data:
        return HttpResponse("No data", status=400)

    decoded = base64.b64decode(data).decode()
    payment_data = json.loads(decoded)

    if payment_data.get("status") == "COMPLETE":
        transaction_uuid = payment_data.get("transaction_uuid")

        booking = Booking.objects.filter(
            payment_uuid=transaction_uuid
        ).first()

        if booking:
            booking.payment_status = True
            booking.is_active = True
            booking.save()

        messages.success(request, "Payment successful & booking confirmed")
        return redirect('home')

    messages.error(request, "Payment failed")
    return redirect('booking')
