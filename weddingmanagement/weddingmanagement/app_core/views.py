from decimal import Decimal
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from app_core.models import Auditorium, Category, District, Eventtype, Location
from app_dashboard.models import Customer, Vendor
from app_customer.models import Booking_details, Booking_master, Payment
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
@login_required(login_url='/login/')
@never_cache
# Create your views here.
def district(request):
    if request.method=="POST":
        distname=request.POST.get('name')
        if District.objects.filter(name=distname).exists():
            return HttpResponse("<script>alert('District already exists');window.location='/core/district';</script>")
        dist=District()
        dist.name=distname
        dist.save()
        return HttpResponse("<script>alert('Inserted Successfully');window.location='/core/district';</script>")
    else:
            return render(request,'district.html')
@login_required(login_url='/login/')
@never_cache
def dis(request):
    Dis=District.objects.all()
    return render(request,'districtview.html',{'dis':Dis})
@login_required(login_url='/login/')
@never_cache
def location(request):
    if request.method=="POST":
        locatname=request.POST.get('locname')
        distname=request.POST.get('distname')
        if Location.objects.filter(name=locatname,).exists():
            return HttpResponse("<script>alert('District already exists');window.location='/core/location';</script>")
        dist=Location()
        dist.name=locatname
        dist.district=District.objects.get(id=distname)
        dist.save()
        return HttpResponse("<script>alert('Inserted Successfully');window.location='/core/location';</script>")
    else:
        d=District.objects.all()
        return render(request,'location.html',{'dis':d})
def disdl(request, id):
    district = get_object_or_404(District, id=id)
    district.delete()
    return redirect('/app_core/distview/')
def disup(request, id):
    district = get_object_or_404(District, id=id)

    if request.method == "POST":
        new_name = request.POST.get('name')

        if District.objects.filter(name=new_name).exclude(id=id).exists():
            return HttpResponse(
                "<script>alert('Already Exist');window.history.back();</script>"
            )

        district.name = new_name
        district.save()
        return redirect('/app_core/distview/')

    return render(request, "districtedit.html", {"disv": district})
def locview(request):
    Loc=Location.objects.all()
    return render(request,'locationview.html',{'loc':Loc})
def locup(request, Id):
    loc=location.objects.get(id=Id)
    if request.method == 'POST':
        name = request.POST.get('name')
        dis = request.POST.get("district")
        loc = Location.objects.get(Locationid=id)
        loc.name = Location
        loc.district = District.objects.get(id=dis)
        loc.save()
        return locview(request)
    else:
        dist = District.objects.all()
        return render(request, "locationedit.html", {'loc': loc, 'dist': dist})
def locdl(request,name):
    d=Location.objects.get(id=name)
    d.delete()
    return HttpResponse("<script>alert('Delete Successfully');window.location='/core/locview/';</script>")
def category(request):
    if request.method=="POST":
        catname=request.POST.get('name')
        catdes=request.POST.get('des')
        if Category.objects.filter(name=catname).exists():
            return HttpResponse("<script>alert('Category already exists');window.location='/core/category';</script>")
        catobj=Category()
        catobj.name=catname
        catobj.description=catdes
        if len(request.FILES) !=0:
                catimg=request.FILES['image']
        else:
            catimg='image/default.jpg'
        catobj.image=catimg 
        catobj.save()
        return HttpResponse("<script>alert('Inserted Successfully');window.location='/core/category';</script>")
    else:
            return render(request,'category.html')
def cat(request):
    Cat=Category.objects.all()
    return render(request,'categoryview.html',{'cat':Cat})
def catedl(request,name):
    d =Category.objects.get(id =name)
    d.delete()
    return HttpResponse("<script>alert('Delete Successfully');window.location='/core/catev/';</script>")

def cateup(request,name):
    up = Category.objects.get(id=name)
    if request.method=="POST":
        cname = request.POST.get('name')
        description=request.POST.get('description')
        if Category.objects.filter(name=cname).exclude(id=name).exists():
            return HttpResponse("<script>alert('Already Exist');window.location='/core/catev/';</script>")
        up.name=cname
        up.description=description
        if len(request.FILES) !=0:
            img=request.FILES.get('img')
            up.image=img
        up.save()
        return HttpResponse("<script>alert('Updated Successfully');window.location='/core/catev/';</script>")
    return render(request,"categoryedit.html",{"catv":up})
def catev(request):
    Cat=Category.objects.all()
    return render(request,'catviewtable.html',{'cat':Cat})




def eventtype(request):
    if request.method=="POST":
        evntname=request.POST.get('name')
        evntdes=request.POST.get('des')
        if Eventtype.objects.filter(name=evntname).exists():
            return HttpResponse("<script>alert('Event already exists');window.location='/core/eventtype';</script>")
        evntobj=Eventtype()
        evntobj.name=evntname
        evntobj.description=evntdes
        if len(request.FILES) !=0:
                evntimg=request.FILES['image']
        else:
            evntimg='image/default.jpg'
        evntobj.image=evntimg 
        evntobj.save()
        return HttpResponse("<script>alert('Inserted Successfully');window.location='/core/eventtype';</script>")
    else:
            return render(request,'eventtype.html')
def evnt(request):
    Evnt=Eventtype.objects.all()
    return render(request,'eventview.html',{'evnt':Evnt})
def evntdl(request,name):
    d =Eventtype.objects.get(id =name)
    d.delete()
    return HttpResponse("<script>alert('Delete Successfully');window.location='/core/evntv/';</script>")

def evntup(request,name):
    up = Eventtype.objects.get(id=name)
    if request.method=="POST":
        evntname = request.POST.get('name')
        description=request.POST.get('description')
        if Eventtype.objects.filter(name=evntname).exclude(id=name).exists():
            return HttpResponse("<script>alert('Already Exist');window.location='/core/evntv/';</script>")
        up.name=evntname
        up.description=description
        if len(request.FILES) !=0:
            img=request.FILES.get('img')
            up.image=img
        up.save()
        return HttpResponse("<script>alert('Updated Successfully');window.location='/core/evntv/';</script>")
    return render(request,"eventedit.html",{"evtv":up})
def evntv(request):
    Evnt=Eventtype.objects.all()
    return render(request,'evntviewtable.html',{'evnt':Evnt})

def vendorview(request):
    Ver=Vendor.objects.all()
    return render(request,'vendorview.html',{'ver':Ver})
    
def custv(request):
       Cust=Customer.objects.all()
       return render(request,'customertable.html',{'cust':Cust})    
def get_locations(request):
    district_id = request.GET.get('district_id')
    locations = Location.objects.filter(district=district_id).values('id', 'name')
    return JsonResponse(list(locations), safe=False)
def auditorium(request):
    if request.method=="POST":
        name=request.POST.get('name')
        hours=request.POST.get('hours')
        amount=request.POST.get('amount')
        location=request.POST.get('location')
        
        if Auditorium.objects.filter(name=name).exists():
            return HttpResponse("<script>alert('Auditorium details already exists');window.location='/core/auditorium';</script>")
        evntobj=Auditorium()
        evntobj.name=name
        evntobj.hours=hours
        evntobj.amount=amount
        evntobj.location=Location.objects.get(id=location)

        if len(request.FILES) !=0:
                evntimg=request.FILES['image']
        else:
            evntimg='image/default.jpg'
        evntobj.image=evntimg 
        evntobj.save()
        return HttpResponse("<script>alert('Inserted Successfully');window.location='/core/auditorium';</script>")
    else:
        district=District.objects.all()
        return render(request,'auditorium.html',{"district":district})
def auditoriumview(request):
    Evnt=Auditorium.objects.all()
    return render(request,'auditoriumview.html',{'data':Evnt})
def auditoriumdl(request,id):
    d =Auditorium.objects.get(id =id)
    d.delete()
    return HttpResponse("<script>alert('Delete Successfully');window.location='/core/auditoriumview/';</script>")

def auditoriumup(request,id):
    up = Auditorium.objects.get(id=id)
    if request.method=="POST":
        evntname = request.POST.get('name')
        hours=request.POST.get('hours')
        amount=request.POST.get('amount')
        if Auditorium.objects.filter(name=evntname).exclude(id=id).exists():
            return HttpResponse("<script>alert('Already Exist');window.location='/core/auditoriumview/';</script>")
        up.name=evntname
        up.hours=hours
        up.amount=amount
        if len(request.FILES) !=0:
            img=request.FILES.get('img')
            up.image=img
        up.location=Location.objects.get(id=request.POST.get("location"))
        up.save()
        return HttpResponse("<script>alert('Updated Successfully');window.location='/core/auditoriumview/';</script>")
    district=District.objects.all()
    location=Location.objects.get(id=up.location.id)
    return render(request,"auditoriumedit.html",{"data":up,"district":district,"location":location})

def admin_payment_list(request):

    payments = (
        Payment.objects
        .select_related('booking', 'booking__customer')
        .prefetch_related('booking__details__service')
        .order_by('-payment_date')
    )

    rows = []
    total_admin_earning = Decimal('0.00')

    for payment in payments:

        # Admin gets 20% of advance (40%)
        admin_commission = payment.amount * Decimal('0.20')

        total_admin_earning += admin_commission

        rows.append({
            'payment': payment,
            'admin_commission': admin_commission
        })

    return render(request, 'admin_paymentview.html', {
        'rows': rows,
        'total_admin_earning': total_admin_earning
    })

def admin_booking_report(request):

    service_data = (
        Booking_details.objects
        .values('service__service__name')   
        .annotate(total_bookings=Count('booking_master', distinct=True))
        .order_by('-total_bookings')
    )

    labels = []
    data = []

    for item in service_data:
        if item['service__service__name']:
            labels.append(item['service__service__name'])
            data.append(item['total_bookings'])

    context = {
        'labels': labels,
        'data': data,
    }

    return render(request, 'booking_report.html', context)

def auditorium_booking_pie_chart(request):
    auditorium_data = (
        Booking_master.objects.values('auditorium__name')
        .annotate(booking_count=Count('id'))
        .order_by('-booking_count')
    )

    labels = [item['auditorium__name'] for item in auditorium_data if item['auditorium__name']]
    data = [item['booking_count'] for item in auditorium_data if item['auditorium__name']]

    context = {
        'labels': labels,
        'data': data,
    }

    return render(request, 'auditorium_report.html', context)