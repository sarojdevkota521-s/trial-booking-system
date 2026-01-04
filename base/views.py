from urllib import request
from django.shortcuts import render,redirect
from .models import Vehicle,Package,Booking,TrialTime
from django.shortcuts import get_object_or_404
# Create your views here.
def home(request):
    c=Vehicle.objects.filter(catogery__name='car')
    b=Vehicle.objects.filter(catogery__name='bike')
    
    context={
        'car':c,
        'bike':b
    }
    return render(request, 'home.html',context)

def booking(request):
    
    
    # from home page (?vehicle=ID)
    selected_vehicle_id = request.GET.get('vehicle')
    selected_vehicle_name=request.GET.get('type')
    packages=Package.objects.filter(vehicle__name=selected_vehicle_name)
    vehicles= Vehicle.objects.filter(catogery__name=selected_vehicle_name)
    booked_time_ids = Booking.objects.values_list('time_id', flat=True)
    trial_times = TrialTime.objects.exclude(id__in=booked_time_ids)
    
     # if vehicle id is invalid, set to None
    if request.method == 'POST':
        fname = request.POST.get('fname')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        vehicle_id = request.POST.get('vehicle')
        package_id = request.POST.get('package')

        # 🔒 validation (prevents ValueError)
        if not (fname and phone and vehicle_id and package_id):
            return render(request, 'booking.html', {
                "packages": packages,
                'vehicle': vehicles,
                'selected_vehicle_id': selected_vehicle_id,
                'selected_vehicle_name': selected_vehicle_name,
                'trial_times': trial_times,
                'error': 'All fields are required'
            })

        selected_vehicle = get_object_or_404(Vehicle, id=vehicle_id)
        selected_package = get_object_or_404(Package, id=package_id)

        Booking.objects.create(
            customer_name=fname,
            phone_number=phone,
            message=message,
            vehicle=selected_vehicle,
            package=selected_package
        )

        return redirect('booking')  # or wherever you want

    return render(request, 'booking.html', {
        'packages': packages,
        'vehicle': vehicles,
        'selected_vehicle_id': selected_vehicle_id,
        'selected_vehicle_name': selected_vehicle_name
    })