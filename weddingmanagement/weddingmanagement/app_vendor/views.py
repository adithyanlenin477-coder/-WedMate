
from django.http import HttpResponse
from django.shortcuts import render

from app_vendor.models import  Staff

from app_dashboard.models import Vendor, VendorService
from app_core.models import Category
from app_customer.models import Booking_details, Gallery, Payment
from weddingmanagement.users.models import User

# Create your views here.
def staff_view(request):
    if request.method=='POST':        
        uname = request.POST.get('name')
        password=request.POST.get('password')  
        name=request.POST.get('name')
        phone=request.POST.get('phone')
        email=request.POST.get('email')
        gender=request.POST.get('gender')
        
        loc=request.POST.get('location')    
        if User.objects.filter(username=uname).exists():
            return HttpResponse("<script>alert('Already Exist');window.location='/vendor/staff';</script>")
        u=User()
        u.name=name
        u.username=uname
        u.password=password
        u.email=email
        u.role="staff"
        u.save()
        
        c=Staff()
        c.location=loc
        c.phno=phone
        c.gender=gender
        c.user=User.objects.get(username=uname)
        c.save()
        return HttpResponse("<script>alert('Register succesfull');window.location='/vendor/staff/';</script>")
    return render(request, "staffreg.html")

def staffv(request):
       Sta=Staff.objects.all()
       return render(request,'stafftable.html',{'sta':Sta})

def servicedetails(request):
    if request.method=="POST":
        service_ids = request.POST.getlist("service_id[]")
        amounts = request.POST.getlist("amount[]")
        images = request.FILES.getlist("image[]")


        for idx, sid in enumerate(service_ids):
            ven = VendorService.objects.get(id=sid)

            # amount
            if idx < len(amounts):
                ven.amount = amounts[idx]

            # image
            if idx < len(images):
                ven.image = images[idx]

            ven.save()
    service=VendorService.objects.filter(vendor=request.user)
    return render(request, "servicedetails.html",{"service":service})   

def gallery(request):
    services = VendorService.objects.filter(vendor=request.user)
    if request.method == "POST":
        service_id = request.POST.get('service_id')
        image = request.FILES['image']

        if request.user and service_id and image:
            Gallery.objects.create(
                vendor=request.user,
                service=Category.objects.get(id=service_id),
                image=image
            )
            return HttpResponse("<script>alert('Image Uploaded Successfully');" "window.location='/vendor/gallery';</script>")


    return render(request, 'galleryform.html', {
        'services': services
    })

def gallery_table(request):
    galleries = Gallery.objects.select_related('vendor', 'service').all()
    return render(request, 'gallerytable.html', {'galleries': galleries})

def vendor_payment_list(request):
    vendor = request.user

    # Fetch payments that include at least one service of this vendor
    payments = (
        Payment.objects
        .select_related('booking', 'booking__customer')  # Payment -> Booking -> Customer
        .prefetch_related(
            'booking__details__service__service',   # Booking_details -> VendorService -> Category
            'booking__details__event'               # Booking_details -> Eventtype
        )
        .filter(
            booking__details__service__vendor=vendor
        )
        .distinct()
        .order_by('-payment_date')
    )

    # Annotate each payment with only the vendor's services
    for payment in payments:
        payment.vendor_services = [
            bd for bd in payment.booking.details.all()  # Booking_details
            if bd.service.vendor == vendor
        ]

    return render(request, 'paymentview.html', {'payments': payments})
