from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from app_core.models import Category, Eventtype
from app_dashboard.models import VendorService
from app_customer.models import Gallery
from weddingmanagement.users.models import User


# Create your views here.
def serviceview(request):
    Evnt=Eventtype.objects.all()
    return render(request,'servicesview.html',{'evnt':Evnt})

def categoryview(request):
    Cat=Category.objects.all()
    return render(request,'categoriesview.html',{'cat':Cat})


def pricedetails(request, service_id):

    # Service / Category (Stage Decoration)
    service = Category.objects.get(id=service_id)

    # Fetch ALL prices for this service (any vendor)
    prices = VendorService.objects.filter(
        service_id=service_id
    ).select_related('service')

    context = {
        'service': service,
        'prices': prices
    }
    return render(request, 'pricedetails.html', context)



    


    

