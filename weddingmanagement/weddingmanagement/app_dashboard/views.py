

from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate,login

from app_dashboard.models import Customer, Vendor, VendorService
from app_core.models import Category, Eventtype
from app_customer.models import Booking_details
from weddingmanagement.users.models import User
from django.core.mail import send_mail
from django.db.models import Count,Sum


# Create your views here.
def appdash(request):

    booking_data = (
        Booking_details.objects
        .values('service__service')
        .annotate(total_bookings=Count('booking_master', distinct=True))
        .order_by('-total_bookings')
    )

    booking_labels = []
    booking_counts = []

    for item in booking_data:
        if item['service__service']:
            booking_labels.append(item['service__service'])
            booking_counts.append(item['total_bookings'])

    total_bookings = sum(booking_counts)


    revenue_data = (
        Booking_details.objects
        .values('service__service')
        .annotate(total_revenue=Sum('service__amount'))
        .order_by('-total_revenue')
    )

    revenue_labels = []
    revenue_amounts = []

    for item in revenue_data:
        if item['service__service']:
            revenue_labels.append(item['service__service'])
            revenue_amounts.append(item['total_revenue'] or 0)

    total_revenue = sum(revenue_amounts)


    context = {
        'booking_labels': booking_labels,
        'booking_counts': booking_counts,
        'revenue_labels': revenue_labels,
        'revenue_amounts': revenue_amounts,
        'total_bookings': total_bookings,
        'total_revenue': total_revenue,
    }

    return render(request, "admin_dashboard.html", context)

def guestdash(request):
    return render(request, "guestdashboard.html")
def login_view(request):
    if request.method=='POST':        
        uname = request.POST.get('name')
        password=request.POST.get('password')        
        user=authenticate(request,username=uname,password=password)
        
        if user is not None:
            if user.role=="admin":
                login(request,user)
                return HttpResponse("<script>alert('Login succesfull');window.location='/admin/';</script>")
            elif user.role=="vendors":
                login(request,user)
                return HttpResponse("<script>alert('Login succesfull');window.location='/vendordash/';</script>")
            elif user.role=="client":
                login(request,user)
                return HttpResponse("<script>alert('Login succesfull');window.location='/customerdash/';</script>")
        else:
            return HttpResponse("<script>alert('incorrect password');window.location='/login/';</script>")
    return render(request, "login.html")

def reg_view(request):
    if request.method=='POST':        
        uname = request.POST.get('name')
        password=request.POST.get('password')  
        vservices=request.POST.getlist('categories')
        license=request.POST.get('license')
        phone=request.POST.get('phone')
        email=request.POST.get('email')
        name=request.POST.get('fname')
        loc=request.POST.get('location')    
        if User.objects.filter(username=uname).exists():
            return HttpResponse("<script>alert('Already Exist');window.location='/registration';</script>")
        u=User()
        u.name=name
        u.username=uname
        u.set_password(password)
        u.email=email
        u.role="vendors"
        u.save()
        send_mail(subject="Registration successfull",message=f"Welcome{name}",from_email=None,recipient_list=[email])

        c=Vendor()
        c.location=loc
        c.phno=phone
        c.licenseno=license
        c.user=u
        c.save()
        for sid in vservices:
            VendorService.objects.create(
                vendor=u,
                service_id=sid,
            )
        return HttpResponse("<script>alert('Register succesfull');window.location='/registration/';</script>")
    d=Category.objects.all()
    return render(request,'vendorreg.html',{'cat':d})

def vendor_dash(request):
    return render(request, "vendordashboard.html")

def staffdash(request):
    return render(request, "staffdashboard.html")

def customer_view(request):
    if request.method=='POST':        
        uname = request.POST.get('name')
        password=request.POST.get('password')  
        address=request.POST.get('address')
        phone=request.POST.get('contact')
        email=request.POST.get('email')
        name=request.POST.get('fname')
        loc=request.POST.get('location')
           
        if User.objects.filter(username=uname).exists():
            return HttpResponse("<script>alert('Already Exist');window.location='/customerreg';</script>")
        u=User()
        u.name=name
        u.username=uname
        u.set_password(password)
        u.email=email
        u.role="client"
        u.save()

        c=Customer()
        c.location=loc
        c.contact=phone
        c.address=address
        c.user=u
        c.save()
        return HttpResponse("<script>alert('Register succesfull');window.location='/customerreg/';</script>")
    return render(request, "customerreg.html")
def customer_dash(request):
    events = Eventtype.objects.all()
    categories = Category.objects.all()

    return render(request, "customerdashboard.html", {
        "events": events,
        "categories": categories
    }) 
    
def select_role(request):
    return render(request, "select_role.html")
       
def event_list(request):
    events = Eventtype.objects.all()  # Fetch all events
    return render(request, 'event_list.html', {'events': events}) 

def vendor_dashboard(request):
    categories = Category.objects.all()

    return render(request, 'vendor_dashboard.html', {
        'categories': categories
    })