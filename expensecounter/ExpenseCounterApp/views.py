from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import expense_item
from django.utils import timezone
# Create your views here.

def index(request):
    template = loader.get_template('ExpenseCounterApp/index.html')
    ordered_db = expense_item.objects.order_by('name')
    context = {'expense_items': ordered_db,
                'worked': "No POST data was sent"}
    
    if request.method == "POST":
        if request.POST.get('name'):
            newitem = expense_item()
            newitem.name = request.POST.get('name')
            newitem.description = request.POST.get('description')
            newitem.cost = request.POST.get('cost')
            newitem.purchase_time = request.POST.get('purchase_time')
            newitem.time_added = timezone.now()
            
            newitem.save()
            context['worked'] = "POST data was sent"
            
            return HttpResponse(template.render(context, request))
            
    
    return HttpResponse(template.render(context, request))