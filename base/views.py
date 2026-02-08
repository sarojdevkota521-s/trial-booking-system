from inspect import signature
from urllib import request
import uuid
from django.shortcuts import render,redirect
from .models import Vehicle,Package,Booking,TrialTime,Timeslot,ContactMessage,Trainer
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.views import View as view
from django.urls import reverse
from django.utils import timezone
from django.db.models import Exists, OuterRef
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count 
from django.utils.timezone import datetime
from datetime import timedelta
from django.db import IntegrityError
# Create your views here.

def home(request):
    # c=Vehicle.objects.filter(catogery__name='car')
    # b=Vehicle.objects.filter(catogery__name='bike')
    base_query = Vehicle.objects.annotate(
        available_slots_count=Count(
            'trialtime',
            filter=~Q(trialtime__bookings__is_active=True),
            distinct=True
        )
    )
    c = base_query.filter(catogery__name='car')
    b = base_query.filter(catogery__name='bike')
    v = base_query.all()
    context={
        'car':c,
        'bike':b,
        'vehicles':v

    }
    return render(request, 'home.html',context)
def about(request):
    
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
    vehicles = Vehicle.objects.all()
    time_slots = Timeslot.objects.all()
    trainers = Trainer.objects.all()

    # Get the date from the search bar, default to today
    date_query = request.GET.get('date')
    if date_query:
        selected_date = datetime.strptime(date_query, "%Y-%m-%d").date()
    else:
        selected_date = timezone.now().date()

    # CRITICAL LOGIC: Find bookings where the selected date is 
    # BETWEEN the start (booking_date) and the end (expiry_date)
    active_bookings = Booking.objects.filter(
        is_active=True,
        booking_date__lte=selected_date,  # Started on or before selected date
        expiry_date__gte=selected_date   # Ends on or after selected date
    )

    # Create a lookup set for (vehicle_id, timeslot_id)
    booked_pairs = set(
        active_bookings.values_list('vehicle_id', 'trial_time__time_id')
    )

    table_data = []
    for vehicle in vehicles:
        row = {
            'vehicle_name': vehicle.name,
            'slots': []
        }
        for slot in time_slots:
            # If the pair exists in our filtered range, mark as booked
            is_booked = (vehicle.id, slot.id) in booked_pairs
            row['slots'].append(is_booked)
        table_data.append(row)

    return render(request, 'detail.html', {
        'time_slots': time_slots,
        'table_data': table_data,
        'selected_date': selected_date.strftime("%Y-%m-%d"),
        'trainers': trainers
    })

def contact(request):
    if request.method == "POST":
        # Extract data from the form
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        email = request.POST.get('emailAddress')
        phone = request.POST.get('phoneNumber')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Save to database
        ContactMessage.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            subject=subject,
            message=message
        )
        
        messages.success(request, "Your message has been sent successfully!")
        return redirect('contact') 
    return render(request, 'contact.html')

from django.http import JsonResponse

def ajax_get_available_times(request):
    date_str = request.GET.get('date')
    vehicle_id = request.GET.get('vehicle_id')
    
    if not date_str or not vehicle_id:
        return JsonResponse({'slots': []})

    selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()

    # Find IDs of timeslots that are already booked for this specific date range
    booked_timeslot_ids = Booking.objects.filter(
        vehicle_id=vehicle_id,
        is_active=True,
        booking_date__lte=selected_date,
        expiry_date__gte=selected_date
    ).values_list('trial_time__time_id', flat=True)

    # Get available Timeslots for this vehicle
    # First, get all trial times for the vehicle
    available_trial_times = TrialTime.objects.filter(
        vehicle_id=vehicle_id
    ).exclude(time_id__in=booked_timeslot_ids)

    data = [{'id': t.time.id, 'time': t.time.time} for t in available_trial_times]
    return JsonResponse({'slots': data})

@login_required(login_url='login')
# def booking(request):

#     selected_vehicle_id = request.GET.get('vehicle')
#     selected_vehicle_name = request.GET.get('type')

#     packages = Package.objects.filter(vehicle__name=selected_vehicle_name)
#     vehicles = Vehicle.objects.filter(catogery__name=selected_vehicle_name)

#     active_booked_timeslot_ids = Booking.objects.filter(
#         is_active=True,
#         vehicle_id=selected_vehicle_id
#     ).values_list('trial_time__time_id', flat=True)

#     available_trial_times = Timeslot.objects.exclude(
#         id__in=active_booked_timeslot_ids
#     )
    
    

#     #  HANDLE POST AND RETURN
#     if request.method == 'POST':
#         fname = request.POST.get('fname')
#         phone = request.POST.get('phone')
#         date=request.POST.get('date')
#         message = request.POST.get('message')
#         time_id = request.POST.get('time')
#         vehicle_id = request.POST.get('vehicle')
#         package_id = request.POST.get('package')

#         if not all([fname, phone,date, time_id, vehicle_id, package_id]):
#             messages.error(request, "All fields are required")
#             return redirect(request.path)
        
#         booking_date = datetime.strptime(date, "%Y-%m-%d").date()
#         today = timezone.now().date()
       
        
#         if booking_date < today:
#             messages.error(request, "Can't book a past date")
#             return redirect('home')
#         is_overlapping = Booking.objects.filter(
#     vehicle_id=vehicle_id,
#     is_active=True,
#     booking_date__lte=booking_date,
#     expiry_date__gte=booking_date,
#     trial_time__time_id=time_id # Checks if the specific slot is taken within a duration
# ).exists()

#         if is_overlapping:
#             messages.error(request, "This vehicle is already booked for the selected duration.")
#             return redirect(request.path)

#         selected_vehicle = get_object_or_404(Vehicle, id=vehicle_id)
#         selected_package = get_object_or_404(Package, id=package_id)
#         selected_trial_time = get_object_or_404(
#             TrialTime,
#             time_id=time_id,
#             vehicle_id=selected_vehicle_id
#         )
#         x=timedelta(days=selected_package.duration_days)
#         exp=booking_date+x
        

#         payment_uuid = str(uuid.uuid4())
#         duplicate_exists = Booking.objects.filter(
#     vehicle_id=vehicle_id,
#     trial_time=selected_trial_time, # Use the object you fetched
#     booking_date=booking_date,
#     is_active=True
# ).exists()

#         if duplicate_exists:
#             messages.error(request, "This specific time slot has just been booked. Please choose another.")
#             return redirect(request.path)

#         try:
#             Booking.objects.create(...)
#         except IntegrityError:
#             messages.error(request, "A system error occurred. Please try again.")
#             return redirect(request.path)


#         Booking.objects.create(
#             user=request.user,
#             customer_name=fname,
#             phone_number=phone,
#             booking_date=date,
#             trial_time=selected_trial_time,
#             message=message,
#             vehicle=selected_vehicle,
#             package=selected_package,
#             expiry_date=exp,
#             payment_uuid=payment_uuid,
#             payment_status=False

#         )

#         return redirect(
#             reverse('esewa') + f'?p={selected_package.id}&uuid={payment_uuid}'
#         )

   
#     return render(request, 'booking.html', {
#         'packages': packages,
#         'vehicle': vehicles,
#         'available_trial_times': available_trial_times,
#         'selected_vehicle_id': selected_vehicle_id,
#         'selected_vehicle_name': selected_vehicle_name
#     })
def booking(request):
    # GET parameters for initial load
    selected_vehicle_id = request.GET.get('vehicle')
    selected_vehicle_name = request.GET.get('type')
    
    # Base querysets
    packages = Package.objects.filter(vehicle__name=selected_vehicle_name)
    vehicles = Vehicle.objects.filter(catogery__name=selected_vehicle_name)

    # Note: On initial GET load, we don't know the date yet, 
    # so we show all times for the vehicle until the user picks a date (handled by AJAX).
    available_trial_times = Timeslot.objects.all()

    if request.method == 'POST':
        fname = request.POST.get('fname')
        phone = request.POST.get('phone')
        date_str = request.POST.get('date')
        message = request.POST.get('message')
        time_id = request.POST.get('time')  # This is the ID of the Timeslot
        vehicle_id = request.POST.get('vehicle')
        package_id = request.POST.get('package')

        if not all([fname, phone, date_str, time_id, vehicle_id, package_id]):
            messages.error(request, "All fields are required")
            return redirect(request.path)

        booking_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        
        if booking_date < timezone.now().date():
            messages.error(request, "Can't book a past date")
            return redirect(request.path)

        # 1. Fetch related objects
        selected_vehicle = get_object_or_404(Vehicle, id=vehicle_id)
        selected_package = get_object_or_404(Package, id=package_id)
        selected_trial_time = get_object_or_404(TrialTime, time_id=time_id, vehicle_id=vehicle_id)

        # 2. Calculate Expiry
        expiry_date = booking_date + timedelta(days=selected_package.duration_days)

        # 3. OVERLAP LOGIC: Check if this vehicle is busy during the requested date
        # This checks if ANY existing active booking's range covers our requested booking_date
        is_overlapping = Booking.objects.filter(
            vehicle=selected_vehicle,
            is_active=True,
            trial_time=selected_trial_time,
            booking_date__lte=booking_date,
            expiry_date__gte=booking_date
        ).exists()

        if is_overlapping:
            messages.error(request, "This vehicle is already booked for this duration/time.")
            return redirect(request.path)

        # 4. Create the Booking
        try:
            payment_uuid = str(uuid.uuid4())
            expiry_date = booking_date + timedelta(days=selected_package.duration_days)
        
            Booking.objects.create(
            user=request.user,
            customer_name=fname,
            phone_number=phone,
            booking_date=booking_date,
            expiry_date=expiry_date,
            trial_time=selected_trial_time,
            vehicle=selected_vehicle,
            package=selected_package,
            payment_uuid=payment_uuid,
            is_active=True # Mark active so the next check sees it
        )
            return redirect(reverse('esewa') + f'?p={selected_package.id}&uuid={payment_uuid}')

        except IntegrityError:
            messages.error(request, "A booking already exists for this exact date and time.")
            return redirect(request.path)

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
