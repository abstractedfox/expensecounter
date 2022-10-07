import datetime
from decimal import *

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
    date_range_start = format_date_for_html(two_weeks_ago)
    date_range_end = format_date_for_html(timezone.now())
    
    #date_range_start_formatted = str(date_range_start.year) + "-" + str(date_range_start.month) + "-" + str(date_range_start.day)
    #date_range_start_formatted = str(date_range_start.year) + "-" + str(date_range_start.month) + "-" + str(date_range_start.day)
    #date_range_start_formatted = format_date_for_html(date_range_start)
    #print("The: " + date_range_start_formatted)
    
    #ordered_db = expense_item.objects.order_by('name')
    #ordered_db = expense_item.objects.all()
    ordered_db = expense_item.objects.filter(purchase_time__range=[date_range_start, date_range_end])
    context = {'expense_items': ordered_db,
                'worked': "Default value",
                'app_title': appTitle,
                'date_range_start': date_range_start,
                'date_range_end': date_range_end,}
    
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
        #format_date_for_html isn't necessary here because the dates are being read from the form in the POST data, so they're already formatted correctly
            date_range_start = request.POST.get('startDate')
            date_range_end = request.POST.get('endDate')
            
            ordered_db = expense_item.objects.filter(purchase_time__range=[date_range_start, date_range_end])
            context['date_range_start'] = date_range_start
            context['date_range_end'] = date_range_end
            context['expense_items'] = ordered_db
            
            print("Start date:" + date_range_start)
            print("End date:" + date_range_end)
            context['worked'] = "Date range POST data was sent"
            
            get_percents(date_range_start, date_range_end)
            
            return HttpResponse(template.render(context, request))
    
    context['worked'] = "No POST data was sent"
    return HttpResponse(template.render(context, request))
    
    
#Use this to format dates before being sent to a template for use in a date input
#This prevents us from having to treat dates differently whether they're passed to a template as a
#python datetime or as already formatted for HTML (ie if they came from POST data & were then sent
#back to another template)
def format_date_for_html(date):
    month = str(date.month)
    if len(month) == 1:
        month = str(0) + month
    
    day = str(date.day)
    if len(day) == 1:
        day = str(0) + day
    
    date_formatted = str(date.year) + "-" + month + "-" + day
    return date_formatted


#Get an array of the percentage breakdown of these categories:
#food_grocery, food_takeout, food_convenience, one_time_important, one_time_unimportant
#recurring_important, #recurring_unimportant
def get_percents(date_range_start, date_range_end):
    date_filtered_db = expense_item.objects.filter(purchase_time__range=[date_range_start, date_range_end])
    total_spend = get_total_spend(date_range_start, date_range_end, expense_item)
    
    percentage_food_grocery = get_total_spend(date_range_start, date_range_end, date_filtered_db.filter(category="food_grocery")) / total_spend * 100
    #print (percentage_food_grocery)
    
#Get total spending for a given date range    
def get_total_spend(date_range_start, date_range_end, source_database):
    date_filtered_db = source_database.objects.filter(purchase_time__range=[date_range_start, date_range_end])
    total = Decimal(0)
    
    for item in date_filtered_db:
        print(str(item.name))
        total += item.cost
        
    return total