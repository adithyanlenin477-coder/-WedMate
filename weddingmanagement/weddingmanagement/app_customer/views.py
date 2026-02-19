from datetime import timezone
from decimal import Decimal
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from app_core.models import Category, Eventtype
from app_dashboard.models import Customer, VendorService
from app_customer.models import Booking_details, Booking_master, Gallery, Payment
from weddingmanagement.users.models import User
from django.db.models import Sum
from django.utils import timezone


# Create your views here.
def serviceview(request):
    evnt = Eventtype.objects.all()
    return render(request, 'servicesview.html', {'evnt': evnt})

def categoryview(request, id):
    Cat = Category.objects.all()

    date = request.session.get('event_date')
    time = request.session.get('event_time')

    return render(request,'categoriesview.html',{
        'cat': Cat,
        "cid": id,
        "date": date,
        "time": time
    })



def pricedetails(request, service_id,cid):
    date = request.session.get('event_date')
    time = request.session.get('event_time')
    
    if request.method=="POST":
        
        serviceid=request.POST.get("service")
        event=request.POST.get("event")
        booking=Booking_details()
        booking.service=VendorService.objects.get(id=serviceid)
        booking.event=Eventtype.objects.get(id=event)
        booking.customer=request.user
        booking.save()
        return HttpResponse("<script>alert('added successfully');window.location='/customer/booking_details_view'</script>")

    booked_vendor_services = Booking_details.objects.filter(
        booking_master__event_date=date,
        booking_master__time=time
    ).values_list('service_id', flat=True)
    # Service / Category (Stage Decoration)
    service = Category.objects.get(id=service_id)

    # Fetch ALL prices for this service (any vendor)
    prices = VendorService.objects.filter(
        service_id=service_id
    ).exclude(
        id__in=booked_vendor_services
    ).select_related('service')

    context = {
        'service': service,
        'prices': prices,
        "cid":cid
    }
    return render(request, 'pricedetails.html', context)
def book_service(request):
    if request.method == "POST":

        booking_date = request.POST.get("service")
        event_date = request.POST.get("event_date")
        note = request.POST.get("note")
        time = request.POST.get("time")
        number_of_participants = request.POST.get("number_of_participants")
        venue = request.POST.get("venue")

        total = Booking_details.objects.filter(
            customer=request.user,
            booking_master__isnull=True
        ).aggregate(
            total_amount=Sum('service__amount')
        )['total_amount'] or Decimal('0.00')

        booking = Booking_master(
            booking_date=booking_date,
            event_date=event_date,
            customer=request.user,
            note=note,
            number_of_participants=number_of_participants,
            time=time,
            venue=venue,
            grandtotal=total   # ✅ correct value saved
        )
        booking.save()

        Booking_details.objects.filter(
            customer=request.user,
            booking_master__isnull=True
        ).update(booking_master=booking)
        

        return redirect("app_customer:payment_page", booking_id=booking.id,)

    total = Booking_details.objects.filter(
        customer=request.user,
        booking_master__isnull=True
    ).aggregate(
        total_amount=Sum('service__amount')
    )['total_amount'] or Decimal('0.00')
    date = request.session.get('event_date')
    time = request.session.get('event_time')
    return render(request, "booking.html", {"grandtotal": total,"date":date,"time":time})

def bookingdetails_view(request): 
    list=Booking_details.objects.filter(customer=request.user,booking_master__isnull=True)
    total=Booking_details.objects.filter(customer=request.user,booking_master__isnull=True).aggregate(total_amount=Sum('service__amount'))['total_amount'] or 0
    return render(request,"booking_details_view.html",{"list":list,"total":total})
def bookingdetail_delete(request, id):
    d=Booking_details.objects.get(id=id)
    d.delete()
    return HttpResponse(
        "<script>alert('Delete Successfully');window.location='/customer/booking_details_view';</script>"
    )

def booking(request):
    book = Booking_master.objects.filter(customer=request.user).order_by('-id')
    return render(request, 'bookingtable.html', {'book': book})  

def payment_page(request, booking_id):
    booking = get_object_or_404(Booking_master, id=booking_id)

    total = Decimal(booking.grandtotal)
    advance = (total * Decimal('40')) / Decimal('100')

    if request.method == "POST":
        # Create payment
        Payment.objects.create(
            booking=booking,
            amount=advance
        )

        # 🔥 CREATE BOOKING DETAILS (THIS WAS MISSING)
        service_ids = request.POST.getlist('service_id[]')

        for sid in service_ids:
            vendor_service = VendorService.objects.get(id=sid)

            Booking_details.objects.create(
                booking_master=booking,
                service=vendor_service,
                customer=booking.customer
            )

        return HttpResponse(
            "<script>alert('Payment successful');"
            "window.location='/customer/booking_details_view';</script>"
        )

    return render(request, "payment.html", {
        "booking": booking,
        "total": total,
        "advance": advance
    })
    
def event_datetime(request, id):
    event = get_object_or_404(Eventtype, id=id)

    if request.method == "POST":
        date = request.POST.get("date")
        time = request.POST.get("time")

        # Store in session
        request.session['event_id'] = id
        request.session['event_date'] = date
        request.session['event_time'] = time

        return redirect('app_customer:categoryv', id=id)

    return render(request, "event_datetime.html", {"event": event})    