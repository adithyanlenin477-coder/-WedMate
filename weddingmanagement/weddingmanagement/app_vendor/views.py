
from decimal import Decimal
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

    payments = (
        Payment.objects
        .select_related('booking', 'booking__customer')
        .prefetch_related('booking__details__service')
        .order_by('-payment_date')
    )

    vendor_rows = []

    total_service_amount = Decimal('0.00')
    total_advance = Decimal('0.00')
    total_admin_share = Decimal('0.00')
    total_vendor_net = Decimal('0.00')

    for payment in payments:

        # Get only this vendor's booked services
        vendor_services = payment.booking.details.filter(
            service__vendor=vendor
        )

        if not vendor_services.exists():
            continue

        # 40% advance paid
        advance_amount = payment.amount

        # Admin takes 20% of advance
        admin_share = (advance_amount * Decimal('0.20')).quantize(Decimal('0.01'))

        # Vendor gets remaining
        vendor_net = (advance_amount - admin_share).quantize(Decimal('0.01'))

        total_advance += advance_amount
        total_admin_share += admin_share
        total_vendor_net += vendor_net

        # Calculate full service price total
        service_total = Decimal('0.00')

        for detail in vendor_services:
            if detail.service.amount:
                service_total += detail.service.amount

        total_service_amount += service_total

        vendor_rows.append({
            'payment': payment,
            'services': vendor_services,
            'service_total': service_total,
            'advance_amount': advance_amount,
            'admin_share': admin_share,
            'vendor_net': vendor_net,
        })

    return render(request, 'paymentview.html', {
        'vendor_rows': vendor_rows,
        'total_service_amount': total_service_amount.quantize(Decimal('0.01')),
        'total_advance': total_advance.quantize(Decimal('0.01')),
        'total_admin_share': total_admin_share.quantize(Decimal('0.01')),
        'total_vendor_net': total_vendor_net.quantize(Decimal('0.01')),
    })