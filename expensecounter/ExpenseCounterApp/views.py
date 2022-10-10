import datetime
from decimal import *

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import expense_item
from django.utils import timezone
# Create your views here.

debugLog = {}

appTitle = "Expense Counter" #app name displayed to the user

def index(request):
    template = loader.get_template('ExpenseCounterApp/index.html')
    
    two_weeks_ago_interval = datetime.timedelta(days=14)
    two_weeks_ago = timezone.now() - two_weeks_ago_interval
    date_range_start = format_date_for_html(two_weeks_ago)
    date_range_end = format_date_for_html(timezone.now())
    
    ordered_db = expense_item.objects.filter(purchase_time__range=[date_range_start, date_range_end])
    
    context = {'expense_items': ordered_db,
                'worked': "Default value",
                'app_title': appTitle,
                'date_range_start': date_range_start,
                'date_range_end': date_range_end,
                'breakdown_percents': get_percents(date_range_start, date_range_end)}
    
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
            context['breakdown_percents'] = get_percents(date_range_start, date_range_end)
            
            print("Start date:" + date_range_start)
            print("End date:" + date_range_end)
            context['worked'] = "Date range POST data was sent"
            
            percents = get_percents(date_range_start, date_range_end)
            
            return HttpResponse(template.render(context, request))
    
    context['worked'] = "No POST data was sent"
    return HttpResponse(template.render(context, request))
    
def deleteitem(request, dbkey):
        object = expense_item.objects.get(id=dbkey)
        logoutput("Deleting: " + object.name)
        object.delete()
        return redirect('/index')




                #Things that aren't views:


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


#Get a dict of the percentage breakdown of these categories:
#food_grocery, food_takeout, food_convenience, one_time_important, one_time_unimportant
#recurring_important, #recurring_unimportant
def get_percents(date_range_start, date_range_end):
    debug = False
    total_spend = get_total_spend(date_range_start, date_range_end, "all")
    breakdown = {'food_grocery': Decimal(0),
    'food_takeout': Decimal(0),
    'food_convenience': Decimal(0),
    'one_time_important': Decimal(0),
    'one_time_unimportant': Decimal(0),
    'recurring_important': Decimal(0),
    'recurring_unimportant': Decimal(0)}
    
    
    breakdown['food_grocery'] = (get_total_spend(date_range_start, date_range_end, "food_grocery") / total_spend) * 100
    breakdown['food_takeout'] = Decimal((get_total_spend(date_range_start, date_range_end, "food_takeout")) / Decimal(total_spend)) * Decimal(100)
    breakdown['food_convenience'] = (get_total_spend(date_range_start, date_range_end, "food_convenience") / total_spend) * 100
    breakdown['one_time_important'] = get_total_spend(date_range_start, date_range_end, "one_time_important") / total_spend * 100
    breakdown['one_time_unimportant'] = get_total_spend(date_range_start, date_range_end, "one_time_unimportant") / total_spend * 100
    breakdown['recurring_important'] = get_total_spend(date_range_start, date_range_end, "recurring_important") / total_spend * 100
    breakdown['recurring_unimportant'] = get_total_spend(date_range_start, date_range_end, "recurring_unimportant") / total_spend * 100
    
    if (debug): print("The breakdown: " + str(breakdown['food_grocery']) + " " + str(breakdown['food_takeout']) + " " + str(breakdown['food_convenience']) + " " + str(breakdown['one_time_important']) + " " + str(breakdown['one_time_unimportant']) + " " + str(breakdown['recurring_important']) + " " + str(breakdown['recurring_unimportant']))
    
    return breakdown
    
    
#Get total spending for a given date range. Acceptable categories are all the categories + "all"
def get_total_spend(date_range_start, date_range_end, category):
    debug = False
    
    total = Decimal(0)
    
    match category:
        case "all":
            filtered_db = expense_item.objects.filter(purchase_time__range=[date_range_start, date_range_end])
            if (debug): print("Values: " + str(filtered_db.count()))
            for item in filtered_db:
                if (debug): print(str(item.name))
                total += item.cost
            return total
        
        case "food_grocery":
            filtered_db = expense_item.objects.filter(purchase_time__range=[date_range_start, date_range_end], category="food_grocery")
            for item in filtered_db:
                if (debug): print(str(item.name))
                total += item.cost
            return total
                
        case "food_takeout":
            filtered_db = expense_item.objects.filter(purchase_time__range=[date_range_start, date_range_end], category="food_takeout")
            for item in filtered_db:
                if (debug): print(str(item.name))
                total += item.cost
            return total
                
        case "food_convenience":
            filtered_db = expense_item.objects.filter(purchase_time__range=[date_range_start, date_range_end], category="food_convenience")
            for item in filtered_db:
                if (debug): print(str(item.name))
                total += item.cost
            return total
                
        case "one_time_important":
            filtered_db = expense_item.objects.filter(purchase_time__range=[date_range_start, date_range_end], category="one_time_important")
            for item in filtered_db:
                if (debug): print(str(item.name))
                total += item.cost
            return total
                        
        case "one_time_unimportant":
            filtered_db = expense_item.objects.filter(purchase_time__range=[date_range_start, date_range_end], category="one_time_unimportant")
            for item in filtered_db:
                if (debug): print(str(item.name))
                total += item.cost
            return total
                
                        
        case "recurring_important":
            filtered_db = expense_item.objects.filter(purchase_time__range=[date_range_start, date_range_end], category="recurring_important")
            for item in filtered_db:
                if (debug): print(str(item.name))
                total += item.cost
            return total
                        
        case "recurring_unimportant":
            filtered_db = expense_item.objects.filter(purchase_time__range=[date_range_start, date_range_end], category="recurring_unimportant")
            for item in filtered_db:
                if (debug): print(str(item.name))
                total += item.cost
            return total
            
def logoutput(logstring):
    debugLog.update({len(debugLog) + 1: logstring})
    print(logstring)