import datetime

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import expense_item
from django.utils import timezone
# Create your views here.

appTitle = "Expense Counter" #app name displayed to the user

def index(request):
    template = loader.get_template('ExpenseCounterApp/index.html')
    
    two_weeks_ago_interval = datetime.timedelta(days=14)
    two_weeks_ago = timezone.now() - two_weeks_ago_interval
    date_range_start = two_weeks_ago
    date_range_end = timezone.now()
    
    #ordered_db = expense_item.objects.order_by('name')
    #ordered_db = expense_item.objects.all()
    ordered_db = expense_item.objects.filter(purchase_time__range=[date_range_start, date_range_end])
    context = {'expense_items': ordered_db,
                'worked': "No POST data was sent",
                'app_title': appTitle,
                'date_range_start': date_range_start,
                'date_range_end': date_range_end}
    
    if request.method == "POST":
        if request.POST.get('name'):
            newitem = expense_item()
            newitem.category = request.POST.get('categoryDropDown')
            newitem.name = request.POST.get('name')
            newitem.description = request.POST.get('description')
            newitem.cost = request.POST.get('cost')
            newitem.purchase_time = request.POST.get('purchase_time')
            newitem.time_added = timezone.now()
            
            newitem.save()
            context['worked'] = "POST data was sent"
            
            return HttpResponse(template.render(context, request))
            
        if request.POST.get('startDate'):
            context['date_range_start'] = request.POST.get('startDate')
            context['date_range_end'] = request.POST.get('endDate')
            context['worked'] = "Date range POST data was sent"
            return HttpResponse(template.render(context, request))
    
    return HttpResponse(template.render(context, request))