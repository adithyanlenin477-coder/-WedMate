from datetime import timezone
from decimal import Decimal
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required

from app_core.models import Auditorium, Category, Eventtype
from app_dashboard.models import Customer, Vendor, VendorService
from app_customer.models import Booking_details, Booking_master, Gallery, Payment
from weddingmanagement.users.models import User
from django.db.models import Sum
from django.utils import timezone
from datetime import datetime, timedelta


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



def pricedetails(request, service_id, cid):

    date = request.session.get('event_date')
    time = request.session.get('event_time')

    if request.method == "POST":

        serviceid = request.POST.get("service")
        event = request.POST.get("event")

        booking = Booking_details()
        booking.service_id = serviceid
        booking.event_id = event
        booking.customer = request.user
        booking.save()

        return HttpResponse(
            "<script>alert('Added successfully');window.location='/customer/booking_details_view'</script>"
        )

    booked_vendor_services = []

    if date and time:
        booked_vendor_services = Booking_details.objects.filter(
            booking_master__event_date=date,
            booking_master__time=time,
            booking_master__isnull=False
        ).values_list('service_id', flat=True)

    service = Category.objects.get(id=service_id)

    prices = VendorService.objects.filter(
        service_id=service_id
    ).exclude(
        id__in=booked_vendor_services
    ).select_related('service')

    context = {
        'service': service,
        'prices': prices,
        "cid": cid
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
        auditorium = request.POST.get("auditorium")


        total = Booking_details.objects.filter(
            customer=request.user,
            booking_master__isnull=True
        ).aggregate(
            total_amount=Sum('service__amount')
        )['total_amount'] or Decimal('0.00')

        booking = Booking_master()
        booking.booking_date=booking_date
        booking.event_date=event_date
        booking.customer=request.user
        booking.note=note
        booking.number_of_participants=number_of_participants
        booking.time=time
        booking.grandtotal=total
        
        if auditorium:   # ✅ If auditorium selected
            booking.auditorium = Auditorium.objects.get(id=auditorium)
            booking.venue = None
            booking.booking_type=request.POST.get("booking_type")
        else:               # ✅ If normal venue
            booking.venue = venue
            booking.auditorium = None
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
    available_auditoriums = []

    if date and time:
        event_date = datetime.strptime(date, "%Y-%m-%d").date()
        start_time = datetime.strptime(time, "%H:%M").time()

        auditoriums = Auditorium.objects.all()

        for auditorium in auditoriums:

            duration = timedelta(hours=auditorium.hours)

            start_datetime = datetime.combine(event_date, start_time)
            end_datetime = start_datetime + duration

            # Existing bookings for same date & auditorium
            bookings = Booking_master.objects.filter(
                event_date=event_date,
                auditorium=auditorium
            )

            conflict = False

            for booking in bookings:
                existing_start = datetime.combine(event_date, booking.time)
                existing_end = existing_start + timedelta(hours=auditorium.hours)

                # 🔥 Overlap condition
                if start_datetime < existing_end and end_datetime > existing_start:
                    conflict = True
                    break

            if not conflict:
                available_auditoriums.append(auditorium)

    return render(request, "booking.html", {
        "grandtotal": total,
        "date": date,
        "time": time,
        "auditorium": available_auditoriums
    })



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

    # auditorium hourly rate
    hourly_rate = booking.auditorium.amount  

    # calculate hours
    if booking.booking_type == "full_day":
        hours = 8
    elif booking.booking_type == "half_day":
        hours = 4
    else:
        hours = 1

    # auditorium amount
    auditorium_total = Decimal(hourly_rate) * Decimal(hours)

    # service amount (grandtotal from booking)
    service_total = Decimal(booking.grandtotal)

    # final total
    total = service_total + auditorium_total

    # 40% advance
    advance = (total * Decimal('40')) / Decimal('100')

    if request.method == "POST":

        # save payment
        Payment.objects.create(
            booking=booking,
            amount=advance
        )

        # save booking details
        service_ids = request.POST.getlist('service_id[]')

        for sid in service_ids:
            vendor_service = VendorService.objects.get(id=sid)

            Booking_details.objects.create(
                booking_master=booking,
                service=vendor_service,
                customer=booking.customer
            )

        # redirect to my bookings page
        return redirect('app_customer:my_bookings')

    return render(request, "payment.html", {
        "booking": booking,
        "auditorium_total": auditorium_total,
        "service_total": service_total,
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


@login_required
def my_bookings(request):
    bookings = Booking_master.objects.filter(customer=request.user)
    return render(request, 'my_bookings.html', {'bookings': bookings})


@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(
        Booking_master,
        id=booking_id,
        customer=request.user
    )

    if request.method == "POST":
        booking.delete()
        return redirect('app_customer:my_bookings')

    return redirect('app_customer:my_bookings')


