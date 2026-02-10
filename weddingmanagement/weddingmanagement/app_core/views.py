from django.http import HttpResponse
from django.shortcuts import redirect, render

from app_core.models import Category, District, Eventtype, Location
from app_dashboard.models import Customer, Vendor
from app_customer.models import Payment

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
def dis(request):
    Dis=District.objects.all()
    return render(request,'districtview.html',{'dis':Dis})

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
    
def disdl(request,name):
    d = District.objects.get(id=name)
    d.delete()
    return HttpResponse("<script>alert('Delete Successfully');window.location='/app_core/distview/';</script>")

def disup(request,name):
    up = District.objects.get(id=name)
    if request.method=="POST":
        name = request.POST.get('name')
        if District.objects.filter(name =name).exists():
            return HttpResponse("<script>alert('Already Exist');window.location='';</script>")
        up.name=name
        up.save()
        return HttpResponse("<script>alert('Updated Successfully');window.location='/core/distview/';</script>")
    return render(request,"districtedit.html",{"disv":up})
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

def admin_payment_list(request):
    payments = (
        Payment.objects
        .select_related('booking', 'booking__customer')
        .prefetch_related(
            'booking__details__service__vendor',
            'booking__details__service__service',
            'booking__details__event'
        )
        .order_by('-payment_date')
    )

    return render(request, 'admin_paymentview.html', {'payments': payments})