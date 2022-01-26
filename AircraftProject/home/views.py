from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login , logout
from django.db import models
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import Profile
from django.urls import reverse
from .form import *
from django.db.models import Q
import json
import datetime
from datetime import date

datenow = timezone.now()

def home(request):
    if request.method == 'POST':
        username  = request.POST.get('username','')
        password = request.POST.get('password','')
    
        user = authenticate(request, username=username,password=password)

        if user is not None:
            login(request, user)
            first_name = user.first_name
            position = user.profile.get_position_display()
            user_id = user.id
            if position == 'Planner':
                return redirect("task", first_name=first_name,position=position,user_id=user_id)
            else:
                return redirect("mechanic", first_name=first_name,position=position,user_id=user_id)
        else:
            messages.success(request, 'Username or Password is invaild.')
            return render(request,'home.html')

    return render(request,'home.html')


def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()

@login_required
def task(request, first_name,position,user_id):
    form = TaskForm
    updateform = UpdateForm
    mechanic = User.objects.filter(profile__position='1')
    task_overdue_count = Task.objects.filter(Reviewed = False).exclude(DueDate__gte=datenow,DueDate__lt=date(2025,2,9)).count()
    task = Task.objects.all()
    cockpit = Task.objects.filter(Zone="Cockpit")
    cockpit_count = Task.objects.filter(Zone="Cockpit").count()
    cabin = Task.objects.filter(Zone="Cabin")
    cabin_count = Task.objects.filter(Zone="Cabin").count()
    wing = Task.objects.filter(Zone="Wing")
    wing_count = Task.objects.filter(Zone="Wing").count()
    landinggear = Task.objects.filter(Zone="Landing Gear")
    landinggear_count = Task.objects.filter(Zone="Landing Gear").count()
    fuselage = Task.objects.filter(Zone="Fuselage")
    fuselage_count = Task.objects.filter(Zone="Fuselage").count()
    engine = Task.objects.filter(Zone="Engine")
    engine_count = Task.objects.filter(Zone="Engine").count()
    empennage = Task.objects.filter(Zone="Empennage")
    empennage_count = Task.objects.filter(Zone="Empennage").count()
    avionic = Task.objects.filter(Zone="Avionic")
    avionic_count = Task.objects.filter(Zone="Avionic").count()
    task_count = Task.objects.count()
    wait_review = Task.objects.filter(Reviewed = None).exclude(Task_Performed__exact = '')
    wait_review_count = Task.objects.filter(Reviewed = None).exclude(Task_Performed__exact = '').count()
    if request.method == 'POST':
        if 'addtask' in request.POST:
            form = TaskForm(request.POST)
            if form.is_valid():
                newform = form.save(commit=False)
                newform.CreateBy = first_name
                newform.save()
                form = TaskForm
                return redirect(request.path_info)
        if 'update_form' in request.POST:
            form = TaskForm(request.POST)
            form_target = Task.objects.filter(id=request.POST.get("id"))
            tn = request.POST.get("Task_name")
            td = request.POST.get("Task_Detail")
            tp = request.POST.get("Task_Performed")
            an_raw = request.POST.get("Assign")
            an_list = an_raw.split(": ")
            an = an_list[1]
            dd = request.POST.get("DueDate")
            rw = request.POST.get("Reviewed")
            if rw == 'None':
                rw == 'False'
                return rw
            ub = first_name
            ud = timezone.now()
            if dd == '':
                form_target.update(Task_name=tn,Task_Detail=td,Task_Performed=tp,Assign=an,Update_Date=ud,Update_By=ub,Reviewed=rw)
                return redirect(request.path_info)  
            else:
                form_target.update(Task_name=tn,Task_Detail=td,Task_Performed=tp,Assign=an,Update_Date=ud,Update_By=ub,DueDate=dd,Reviewed=rw)
                return redirect(request.path_info) 
        if 'look' in request.POST:
            lk = request.POST.get("lookingfor")
            if lk.isdigit() == True:
                result = Task.objects.filter(Q(id__icontains=lk))
                if result == '<QuerySet []>':
                    result = 'Task Not Found.'
                    return render(request,"search.html",{"result":result})
                return render(request,"planner/search.html",{"result":result})
            else:
                result = Task.objects.filter(Q(Task_name__icontains=lk))
                if result == '<QuerySet []>':
                    result = None
                    return redirect("search",{"result":result})
                return render(request,"planner/search.html",{
                    "form":form,
                    "result":result,
                    "first_name":first_name,
                    "position":position,
                    "mechanic":mechanic,
                    "wait_review_count":wait_review_count,
                    "wait_review":wait_review,
                    "task_overdue_count":task_overdue_count,
                    "user_id":user_id,})    
        if 'delete_task'  in request.POST:
            delete = request.POST.get("id")
            delete_task = Task.objects.get(id = delete)
            delete_task.delete()
            return redirect(request.path_info) 
        if 'mechaniclist' in request.POST:
            return render(request,"planner/mechanic.html",{
                    "first_name":first_name,
                    "position":position,
                    "mechanic":mechanic,
                    "wait_review_count":wait_review_count,
                    "wait_review":wait_review,
                    "task":task,
                    "task_overdue_count":task_overdue_count,
                    "user_id":user_id,})
    return render(request,'planner/task.html',{
    "first_name":first_name,
    "position":position,
    "mechanic":mechanic,
    "form":form,
    "updateform":updateform,
    "cockpit":cockpit,
    "cabin":cabin,
    "wing":wing,
    "landinggear":landinggear,
    "fuselage":fuselage,
    "engine":engine,
    "empennage":empennage,
    "avionic":avionic,
    "task_count":task_count,
    "wait_review_count":wait_review_count,
    "wait_review":wait_review,
    "cockpit_count":cockpit_count,
    "cabin_count":cabin_count,
    "wing_count":wing_count,
    "landinggear_count":landinggear_count,
    "fuselage_count":fuselage_count,
    "engine_count":engine_count,
    "empennage_count":empennage_count,
    "avionic_count":avionic_count,
    "task_overdue_count":task_overdue_count,
    "user_id":user_id,
    })

@login_required
def mechaniclist(request,first_name,position,user_id):
    form = TaskForm
    mechanic = User.objects.filter(profile__position='1')
    mechanic_1 = User.objects.filter(profile__position='1').values_list('first_name', flat=True)
    wait_review = Task.objects.filter(Reviewed = None).exclude(Task_Performed__exact = '')
    datenow = timezone.now()
    task_overdue_count = Task.objects.filter(Reviewed = False).exclude(DueDate__gte=datenow,DueDate__lt=date(2025,2,9)).count()
    task = Task.objects.all()
    mytask = Task.objects.filter(Assign=first_name)
    my_task_count = Task.objects.filter(Assign=first_name).count
    my_task_reviewed_count = Task.objects.filter(Assign=first_name).filter(Reviewed=True).exclude(Task_Performed='').count
    mytask_wait_review_count = Task.objects.filter(Assign=first_name).filter(Reviewed=True).exclude(Task_Performed='').count
    mechanic_list = {}
    for mechanics in mechanic:
        task_count = Task.objects.filter(Assign = mechanics.first_name).count()
        mechanic_list[mechanics] = task_count 
    if position == 'Planner':
        if request.method == 'POST':
            if 'addtask' in request.POST:
                form = TaskForm(request.POST)
                if form.is_valid():
                    newform = form.save(commit=False)
                    newform.CreateBy = first_name
                    newform.save()
                    form = TaskForm
                    return redirect(request.path_info)
            if 'update_form' in request.POST:
                form = TaskForm(request.POST)
                form_target = Task.objects.filter(id=request.POST.get("id"))
                tn = request.POST.get("Task_name")
                td = request.POST.get("Task_Detail")
                tp = request.POST.get("Task_Performed")
                an_raw = request.POST.get("Assign")
                an_list = an_raw.split(": ")
                an = an_list[1]
                dd = request.POST.get("DueDate")
                rw = request.POST.get("Reviewed")
                if rw == 'None':
                    rw == 'False'
                    return rw
                ub = first_name
                ud = timezone.now()
                if dd == '':
                    form_target.update(Task_name=tn,Task_Detail=td,Task_Performed=tp,Assign=an,Update_Date=ud,Update_By=ub,Reviewed=rw)
                    return redirect(request.path_info)  
                else:
                    form_target.update(Task_name=tn,Task_Detail=td,Task_Performed=tp,Assign=an,Update_Date=ud,Update_By=ub,DueDate=dd,Reviewed=rw)
                    return redirect(request.path_info) 
        if 'look' in request.POST:
            lk = request.POST.get("lookingfor")
            if lk.isdigit() == True:
                result = Task.objects.filter(Q(id__icontains=lk))
                if result == '<QuerySet []>':
                    result = 'Task Not Found.'
                    return render(request,"planner/search.html",{"result":result,
                    "task_overdue_count":task_overdue_count,})
                return render(request,"planner/search.html",{"result":result,
                "task_overdue_count":task_overdue_count,})
            else:
                result = Task.objects.filter(Q(Task_name__icontains=lk))
                print('result from task :',result)
                if result == '<QuerySet []>':
                    result = None
                    return redirect("search",{"result":result})
                return render(request,"planner/search.html",{
                    "result":result,
                    "first_name":first_name,
                    "position":position,
                    "mechanic":mechanic,
                    "my_task_reviewed_count":my_task_reviewed_count,
                    "wait_review":wait_review,
                    "mechanic_list":mechanic_list,
                    "task_overdue_count":task_overdue_count,
                    "user_id":user_id,})
        if 'delete_task'  in request.POST:
                delete = request.POST.get("id")
                delete_task = Task.objects.get(id = delete)
                delete_task.delete()
                return redirect(request.path_info)            
        return render(request,"planner/mechaniclist.html",{
                        "form":form,
                        "first_name":first_name,
                        "position":position,
                        "mechanic":mechanic,
                        "my_task_reviewed_count":my_task_reviewed_count,
                        "wait_review":wait_review,
                        "task":task,
                        "mechanic_list":mechanic_list,
                        "task_overdue_count":task_overdue_count,
                        "user_id":user_id,})
    else:
        if request.method == 'POST':
            if 'update_form' in request.POST:
                form = TaskForm(request.POST)
                form_target = Task.objects.filter(id=request.POST.get("id"))
                tp = request.POST.get("Task_Performed")
                ub = first_name
                ud = timezone.now()
                form_target.update(Task_Performed=tp,Update_Date=ud,Update_By=ub)
                return redirect(request.path_info)  
        if 'look' in request.POST:
            lk = request.POST.get("lookingfor")
            if lk.isdigit() == True:
                result = Task.objects.filter(Q(id__icontains=lk))
                if result == '<QuerySet []>':
                    result = 'Task Not Found.'
                    return render(request,"mechanic/search.html",{"result":result,
                    "task_overdue_count":task_overdue_count,})
                return render(request,"mechanic/search.html",{"result":result,
                "task_overdue_count":task_overdue_count,})
            else:
                result = Task.objects.filter(Q(Task_name__icontains=lk))
                print('result from task :',result)
                if result == '<QuerySet []>':
                    result = None
                    return redirect("search",{"result":result})
                return render(request,"mechanic/search.html",{
                    "result":result,
                    "first_name":first_name,
                    "position":position,
                    "mechanic":mechanic,
                    "my_task_reviewed_count":my_task_reviewed_count,
                    "wait_review":wait_review,
                    "mechanic_list":mechanic_list,
                    "task_overdue_count":task_overdue_count,
                    "user_id":user_id,
                    "mytask":mytask,
                    "my_task_count":my_task_count,
                    "mytask_wait_review_count":mytask_wait_review_count,})         
        return render(request,"mechanic/mechaniclist.html",{
                        "form":form,
                        "first_name":first_name,
                        "position":position,
                        "mechanic":mechanic,
                        "my_task_reviewed_count":my_task_reviewed_count,
                        "wait_review":wait_review,
                        "task":task,
                        "mechanic_list":mechanic_list,
                        "task_overdue_count":task_overdue_count,
                        "user_id":user_id,
                        "mytask":mytask,
                        "my_task_count":my_task_count,
                        "mytask_wait_review_count":mytask_wait_review_count,})

@login_required
def waitreview(request,first_name,position,user_id):
    form = TaskForm
    mechanic = User.objects.filter(profile__position='1')
    wait_review = Task.objects.filter(Reviewed = None).exclude(Task_Performed__exact = '')
    wait_review_count = Task.objects.filter(Reviewed = None).exclude(Task_Performed__exact = '').count()
    datenow = timezone.now()
    task_overdue_count = Task.objects.filter(Reviewed = False).exclude(DueDate__gte=datenow,DueDate__lt=date(2025,2,9)).count()
    task = Task.objects.all()
    my_task_reviewed_count = Task.objects.filter(Assign=first_name).filter(Reviewed=True).exclude(Task_Performed='').count
    if request.method == 'POST':
        if 'addtask' in request.POST:
            form = TaskForm(request.POST)
            if form.is_valid():
                newform = form.save(commit=False)
                newform.CreateBy = first_name
                newform.save()
                form = TaskForm
                return redirect(request.path_info)
        if 'update_form' in request.POST:
            form = TaskForm(request.POST)
            form_target = Task.objects.filter(id=request.POST.get("id"))
            tn = request.POST.get("Task_name")
            td = request.POST.get("Task_Detail")
            tp = request.POST.get("Task_Performed")
            an_raw = request.POST.get("Assign")
            an_list = an_raw.split(": ")
            an = an_list[1]
            dd = request.POST.get("DueDate")
            rw = request.POST.get("Reviewed")
            if rw == 'None':
                rw == 'False'
                return rw
            ub = first_name
            ud = timezone.now()
            if dd == '':
                form_target.update(Task_name=tn,Task_Detail=td,Task_Performed=tp,Assign=an,Update_Date=ud,Update_By=ub,Reviewed=rw)
                return redirect(request.path_info)  
            else:
                form_target.update(Task_name=tn,Task_Detail=td,Task_Performed=tp,Assign=an,Update_Date=ud,Update_By=ub,DueDate=dd,Reviewed=rw)
                return redirect(request.path_info)  
        if 'look' in request.POST:
            lk = request.POST.get("lookingfor")
            if lk.isdigit() == True:
                result = Task.objects.filter(Q(id__icontains=lk))
                if result == '<QuerySet []>':
                    result = 'Task Not Found.'
                    return render(request,"planner/search.html",{"result":result,
                    "task_overdue_count":task_overdue_count,})
                return render(request,"planner/search.html",{"result":result,
                "task_overdue_count":task_overdue_count,})
            else:
                result = Task.objects.filter(Q(Task_name__icontains=lk))
                print('result from task :',result)
                if result == '<QuerySet []>':
                    result = None
                    return redirect("search",{"result":result})
                return render(request,"planner/search.html",{
                    "result":result,
                    "first_name":first_name,
                    "position":position,
                    "mechanic":mechanic,
                    "wait_review_count":wait_review_count,
                    "wait_review":wait_review,
                    "task_overdue_count":task_overdue_count,
                    "user_id":user_id,})     
        if 'delete_task'  in request.POST:
            delete = request.POST.get("id")
            delete_task = Task.objects.get(id = delete)
            delete_task.delete()
            return redirect(request.path_info)           
    return render(request,"planner/wait_review.html",{
                    "form":form,
                    "first_name":first_name,
                    "position":position,
                    "mechanic":mechanic,
                    "wait_review_count":wait_review_count,
                    "wait_review":wait_review,
                    "task":task,
                    "task_overdue_count":task_overdue_count,
                    "user_id":user_id,})

@login_required
def overdue(request,first_name,position,user_id):
    form = TaskForm
    mechanic = User.objects.filter(profile__position='1')
    wait_review = Task.objects.filter(Reviewed = None).exclude(Task_Performed__exact = '')
    wait_review_count = Task.objects.filter(Reviewed = None).exclude(Task_Performed__exact = '').count()
    datenow = timezone.now()
    task_overdue = Task.objects.filter(Reviewed = False).exclude(DueDate__gte=datenow,DueDate__lt=date(2025,2,9))
    task_overdue_count = Task.objects.filter(Reviewed = False).exclude(DueDate__gte=datenow,DueDate__lt=date(2025,2,9)).count()
    my_task = Task.objects.filter(Assign=first_name)
    my_task_count = Task.objects.filter(Assign=first_name).count
    my_task_reviewed_count = Task.objects.filter(Assign=first_name).filter(Reviewed=True).exclude(Task_Performed='').count
    mytask_wait_review_count = Task.objects.filter(Assign=first_name).filter(Reviewed=True).exclude(Task_Performed='').count
    if position == 'Planner':
        if request.method == 'POST':
            if 'addtask' in request.POST:
                form = TaskForm(request.POST)
                if form.is_valid():
                    newform = form.save(commit=False)
                    newform.CreateBy = first_name
                    newform.save()
                    form = TaskForm
                    return redirect(request.path_info)
            if 'update_form' in request.POST:
                form = TaskForm(request.POST)
                form_target = Task.objects.filter(id=request.POST.get("id"))
                tp = request.POST.get("Task_Performed")
                ub = first_name
                ud = timezone.now()
                form_target.update(Task_Performed=tp,Update_Date=ud,Update_By=ub)
                return redirect(request.path_info)  
            if 'look' in request.POST:
                lk = request.POST.get("lookingfor")
                if lk.isdigit() == True:
                    result = Task.objects.filter(Q(id__icontains=lk))
                    if result == '<QuerySet []>':
                        result = 'Task Not Found.'
                        return render(request,"planner/search.html",{"result":result,
                        "task_overdue_count":task_overdue_count,})
                    return render(request,"planner/search.html",{"result":result,
                    "task_overdue_count":task_overdue_count,})
                else:
                    result = Task.objects.filter(Q(Task_name__icontains=lk))
                    print('result from task :',result)
                    if result == '<QuerySet []>':
                        result = None
                        return redirect("search",{"result":result,
                        "task_overdue_count":task_overdue_count,})
                    return render(request,"planner/search.html",{
                        "result":result,
                        "first_name":first_name,
                        "position":position,
                        "mechanic":mechanic,
                        "wait_review_count":wait_review_count,
                        "wait_review":wait_review,
                        "task_overdue_count":task_overdue_count,
                        "user_id":user_id,})     
            if 'delete_task'  in request.POST:
                delete = request.POST.get("id")
                delete_task = Task.objects.get(id = delete)
                delete_task.delete()
                return redirect(request.path_info)           
        return render(request,"planner/overdue.html",{
                        "form":form,
                        "first_name":first_name,
                        "position":position,
                        "mechanic":mechanic,
                        "wait_review_count":wait_review_count,
                        "wait_review":wait_review,
                        "task_overdue":task_overdue,
                        "task_overdue_count":task_overdue_count,
                        "user_id":user_id,})
    else:
        if request.method == 'POST':
            if 'update_form' in request.POST:
                form = TaskForm(request.POST)
                form_target = Task.objects.filter(id=request.POST.get("id"))
                tp = request.POST.get("Task_Performed")
                ub = first_name
                ub_id = user_id
                ud = timezone.now()
                form_target.update(Task_Performed=tp,Update_Date=ud,Update_By=ub,Update_By_ID=ub_id)
                return redirect(request.path_info)   
            if 'look' in request.POST:
                lk = request.POST.get("lookingfor")
                if lk.isdigit() == True:
                    result = Task.objects.filter(Q(id__icontains=lk))
                    if result == '<QuerySet []>':
                        result = 'Task Not Found.'
                        return render(request,"mechanic/search.html",{"result":result,
                        "task_overdue_count":task_overdue_count,})
                    return render(request,"mechanic/search.html",{"result":result,
                    "task_overdue_count":task_overdue_count,})
                else:
                    result = Task.objects.filter(Q(Task_name__icontains=lk))
                    print('result from task :',result)
                    if result == '<QuerySet []>':
                        result = None
                        return redirect("search",{"result":result,
                        "task_overdue_count":task_overdue_count,})
                    return render(request,"mechanic/search.html",{
                        "result":result,
                        "first_name":first_name,
                        "position":position,
                        "mechanic":mechanic,
                        "wait_review_count":wait_review_count,
                        "wait_review":wait_review,
                        "task_overdue_count":task_overdue_count,
                        "user_id":user_id,
                        "my_task":my_task,
                        "my_task_count":my_task_count,
                        "my_task_reviewed_count":my_task_reviewed_count,
                        "mytask_wait_review_count":mytask_wait_review_count,})            
        return render(request,"mechanic/overdue.html",{
                        "form":form,
                        "first_name":first_name,
                        "position":position,
                        "mechanic":mechanic,
                        "wait_review_count":wait_review_count,
                        "wait_review":wait_review,
                        "task_overdue":task_overdue,
                        "task_overdue_count":task_overdue_count,
                        "my_task":my_task,
                        "my_task_count":my_task_count,
                        "user_id":user_id,
                        "my_task_reviewed_count":my_task_reviewed_count,
                        "mytask_wait_review_count":mytask_wait_review_count,})

@login_required
def mechanic(request,first_name,position,user_id):
    mechanic = User.objects.filter(profile__position='1')
    task_overdue_count = Task.objects.filter(Reviewed = False).exclude(DueDate__gte=datenow,DueDate__lt=date(2025,2,9)).count()
    updateform = UpdateForm
    cockpit = Task.objects.filter(Zone="Cockpit")
    cockpit_count = Task.objects.filter(Zone="Cockpit").count()
    cabin = Task.objects.filter(Zone="Cabin")
    cabin_count = Task.objects.filter(Zone="Cabin").count()
    wing = Task.objects.filter(Zone="Wing")
    wing_count = Task.objects.filter(Zone="Wing").count()
    landinggear = Task.objects.filter(Zone="Landing Gear")
    landinggear_count = Task.objects.filter(Zone="Landing Gear").count()
    fuselage = Task.objects.filter(Zone="Fuselage")
    fuselage_count = Task.objects.filter(Zone="Fuselage").count()
    engine = Task.objects.filter(Zone="Engine")
    engine_count = Task.objects.filter(Zone="Engine").count()
    empennage = Task.objects.filter(Zone="Empennage")
    empennage_count = Task.objects.filter(Zone="Empennage").count()
    avionic = Task.objects.filter(Zone="Avionic")
    avionic_count = Task.objects.filter(Zone="Avionic").count()
    mytask = Task.objects.filter(Assign=first_name)
    my_task_count = Task.objects.filter(Assign=first_name).count
    my_task_reviewed_count = Task.objects.filter(Assign=first_name).filter(Reviewed=True).exclude(Task_Performed='').count
    mytask_wait_review_count = Task.objects.filter(Assign=first_name).filter(Reviewed=True).exclude(Task_Performed='').count
    if 'look' in request.POST:
            lk = request.POST.get("lookingfor")
            if lk.isdigit() == True:
                result = Task.objects.filter(Q(id__icontains=lk))
                if result == '<QuerySet []>':
                    result = 'Task Not Found.'
                    return render(request,"search.html",{"result":result})
                return render(request,"mechanic/search.html",{
                    "result":result,
                    "first_name":first_name,
                    "position":position,
                    "mechanic":mechanic,
                    "task_overdue_count":task_overdue_count,
                    "my_task_count":my_task_count,
                    "user_id":user_id,})
            else:
                result = Task.objects.filter(Q(Task_name__icontains=lk))
                if result == '<QuerySet []>':
                    result = None
                    return redirect("search",{"result":result})
                return render(request,"mechanic/search.html",{
                    "result":result,
                    "first_name":first_name,
                    "position":position,
                    "mechanic":mechanic,
                    "task_overdue_count":task_overdue_count,
                    "my_task_count":my_task_count,
                    "user_id":user_id,
                    "my_task_reviewed_count":my_task_reviewed_count,
                    "mytask_wait_review_count":mytask_wait_review_count,})    
    if 'update_form' in request.POST:
        form = TaskForm(request.POST)
        print(request.POST)
        form_target = Task.objects.filter(id=request.POST.get("id"))
        tp = request.POST.get("Task_Performed")
        ub = first_name
        ub_id = user_id
        ud = timezone.now()
        form_target.update(Task_Performed=tp,Update_Date=ud,Update_By=ub,Update_By_ID=ub_id)
        return redirect(request.path_info)  
    return render(request,'mechanic/mechanic.html',{
        'first_name':first_name,
        'position':position,
        'task_overdue_count':task_overdue_count,
        "mechanic":mechanic,
        "updateform":updateform,
        "cockpit":cockpit,
        "cabin":cabin,
        "wing":wing,
        "landinggear":landinggear,
        "fuselage":fuselage,
        "engine":engine,
        "empennage":empennage,
        "avionic":avionic,
        "cockpit_count":cockpit_count,
        "cabin_count":cabin_count,
        "wing_count":wing_count,
        "landinggear_count":landinggear_count,
        "fuselage_count":fuselage_count,
        "engine_count":engine_count,
        "empennage_count":empennage_count,
        "avionic_count":avionic_count,
        "mytask":mytask,
        "my_task_count":my_task_count,
        "user_id":user_id,
        "my_task_reviewed_count":my_task_reviewed_count,
        "mytask_wait_review_count":mytask_wait_review_count,
    })

@login_required
def mytask(request,first_name,position,user_id):
    mechanic = User.objects.filter(profile__position='1')
    task_overdue_count = Task.objects.filter(Reviewed = False).exclude(DueDate__gte=datenow,DueDate__lt=date(2025,2,9)).count()
    updateform = UpdateForm
    cockpit = Task.objects.filter(Zone="Cockpit")
    cockpit_count = Task.objects.filter(Zone="Cockpit").count()
    cabin = Task.objects.filter(Zone="Cabin")
    cabin_count = Task.objects.filter(Zone="Cabin").count()
    wing = Task.objects.filter(Zone="Wing")
    wing_count = Task.objects.filter(Zone="Wing").count()
    landinggear = Task.objects.filter(Zone="Landing Gear")
    landinggear_count = Task.objects.filter(Zone="Landing Gear").count()
    fuselage = Task.objects.filter(Zone="Fuselage")
    fuselage_count = Task.objects.filter(Zone="Fuselage").count()
    engine = Task.objects.filter(Zone="Engine")
    engine_count = Task.objects.filter(Zone="Engine").count()
    empennage = Task.objects.filter(Zone="Empennage")
    empennage_count = Task.objects.filter(Zone="Empennage").count()
    avionic = Task.objects.filter(Zone="Avionic")
    avionic_count = Task.objects.filter(Zone="Avionic").count()
    mytask = Task.objects.filter(Assign=first_name)
    my_task_count = Task.objects.filter(Assign=first_name).count
    my_task_reviewed_count = Task.objects.filter(Assign=first_name).filter(Reviewed=True).exclude(Task_Performed='').count
    my_task_wait = Task.objects.filter(Assign=first_name).exclude(Task_Performed='').exclude(Reviewed=True).count
    mytask_wait_review_count = Task.objects.filter(Assign=first_name).filter(Reviewed=True).exclude(Task_Performed='').count
    if 'look' in request.POST:
            lk = request.POST.get("lookingfor")
            if lk.isdigit() == True:
                result = Task.objects.filter(Q(id__icontains=lk))
                if result == '<QuerySet []>':
                    result = 'Task Not Found.'
                    return render(request,"search.html",{"result":result})
                return render(request,"mechanic/search.html",{"result":result})
            else:
                result = Task.objects.filter(Q(Task_name__icontains=lk))
                if result == '<QuerySet []>':
                    result = None
                    return redirect("search",{"result":result})
                return render(request,"mechanic/search.html",{
                    "result":result,
                    "first_name":first_name,
                    "position":position,
                    "mechanic":mechanic,
                    "task_overdue_count":task_overdue_count,
                    "my_task_count":my_task_count,
                    "mytask":mytask,
                    "user_id":user_id,
                    "my_task_reviewed_count":my_task_reviewed_count,
                    "mytask_wait_review_count":mytask_wait_review_count,})    
    if 'update_form' in request.POST:
        form = TaskForm(request.POST)
        form_target = Task.objects.filter(id=request.POST.get("id"))
        print(request.POST)
        tp = request.POST.get("Task_Performed")
        ub = first_name
        ub_id = user_id
        ud = timezone.now()
        form_target.update(Task_Performed=tp,Update_Date=ud,Update_By=ub,Update_By_ID=ub_id)
        return redirect(request.path_info)  
    return render(request,'mechanic/mytask.html',{
        'first_name':first_name,
        'position':position,
        'task_overdue_count':task_overdue_count,
        "mechanic":mechanic,
        "updateform":updateform,
        "cockpit":cockpit,
        "cabin":cabin,
        "wing":wing,
        "landinggear":landinggear,
        "fuselage":fuselage,
        "engine":engine,
        "empennage":empennage,
        "avionic":avionic,
        "cockpit_count":cockpit_count,
        "cabin_count":cabin_count,
        "wing_count":wing_count,
        "landinggear_count":landinggear_count,
        "fuselage_count":fuselage_count,
        "engine_count":engine_count,
        "empennage_count":empennage_count,
        "avionic_count":avionic_count,
        "mytask":mytask,
        "my_task_count":my_task_count,
        "user_id":user_id,
        "my_task_reviewed_count":my_task_reviewed_count,
        "my_task_wait":my_task_wait,
        "mytask_wait_review_count":mytask_wait_review_count,
    })

@login_required
def mytask_reviewed(request,first_name,position,user_id):
    mechanic = User.objects.filter(profile__position='1')
    task_overdue_count = Task.objects.filter(Reviewed = False).exclude(DueDate__gte=datenow,DueDate__lt=date(2025,2,9)).count()
    updateform = UpdateForm
    cockpit = Task.objects.filter(Zone="Cockpit")
    cockpit_count = Task.objects.filter(Zone="Cockpit").count()
    cabin = Task.objects.filter(Zone="Cabin")
    cabin_count = Task.objects.filter(Zone="Cabin").count()
    wing = Task.objects.filter(Zone="Wing")
    wing_count = Task.objects.filter(Zone="Wing").count()
    landinggear = Task.objects.filter(Zone="Landing Gear")
    landinggear_count = Task.objects.filter(Zone="Landing Gear").count()
    fuselage = Task.objects.filter(Zone="Fuselage")
    fuselage_count = Task.objects.filter(Zone="Fuselage").count()
    engine = Task.objects.filter(Zone="Engine")
    engine_count = Task.objects.filter(Zone="Engine").count()
    empennage = Task.objects.filter(Zone="Empennage")
    empennage_count = Task.objects.filter(Zone="Empennage").count()
    avionic = Task.objects.filter(Zone="Avionic")
    avionic_count = Task.objects.filter(Zone="Avionic").count()
    my_task_reviewed = Task.objects.filter(Assign=first_name,Reviewed=True).exclude(Task_Performed='')
    my_task_reviewed_count = Task.objects.filter(Assign=first_name).filter(Reviewed=True).exclude(Task_Performed='').count
    my_task_count = Task.objects.filter(Assign=first_name).count
    mytask_wait_review_count = Task.objects.filter(Assign=first_name).filter(Reviewed=True).exclude(Task_Performed='').count
    if 'look' in request.POST:
            lk = request.POST.get("lookingfor")
            if lk.isdigit() == True:
                result = Task.objects.filter(Q(id__icontains=lk))
                if result == '<QuerySet []>':
                    result = 'Task Not Found.'
                    return render(request,"search.html",{"result":result})
                return render(request,"mechanic/search.html",{"result":result})
            else:
                result = Task.objects.filter(Q(Task_name__icontains=lk))
                if result == '<QuerySet []>':
                    result = None
                    return redirect("search",{"result":result})
                return render(request,"mechanic/search.html",{
                    "result":result,
                    "first_name":first_name,
                    "position":position,
                    "mechanic":mechanic,
                    "task_overdue_count":task_overdue_count,
                    "my_task_count":my_task_count,
                    "user_id":user_id,
                    "mytask_wait_review_count":mytask_wait_review_count,})    
    if 'update_form' in request.POST:
        form = TaskForm(request.POST)
        form_target = Task.objects.filter(id=request.POST.get("id"))
        print(request.POST)
        tp = request.POST.get("Task_Performed")
        ub = first_name
        ub_id = user_id
        ud = timezone.now()
        form_target.update(Task_Performed=tp,Update_Date=ud,Update_By=ub,Update_By_ID=ub_id)
        return redirect(request.path_info)  
    return render(request,'mechanic/mytask_reviewed.html',{
        'first_name':first_name,
        'position':position,
        'task_overdue_count':task_overdue_count,
        "mechanic":mechanic,
        "updateform":updateform,
        "cockpit":cockpit,
        "cabin":cabin,
        "wing":wing,
        "landinggear":landinggear,
        "fuselage":fuselage,
        "engine":engine,
        "empennage":empennage,
        "avionic":avionic,
        "cockpit_count":cockpit_count,
        "cabin_count":cabin_count,
        "wing_count":wing_count,
        "landinggear_count":landinggear_count,
        "fuselage_count":fuselage_count,
        "engine_count":engine_count,
        "empennage_count":empennage_count,
        "avionic_count":avionic_count,
        "my_task_reviewed":my_task_reviewed,
        "my_task_reviewed_count":my_task_reviewed_count,
        "my_task_count":my_task_count,
        "user_id":user_id,
        "mytask_wait_review_count":mytask_wait_review_count,
    })

@login_required
def mytask_wait_review(request,first_name,position,user_id):
    mechanic = User.objects.filter(profile__position='1')
    task_overdue_count = Task.objects.filter(Reviewed = False).exclude(DueDate__gte=datenow,DueDate__lt=date(2025,2,9)).count()
    updateform = UpdateForm
    cockpit = Task.objects.filter(Zone="Cockpit")
    cockpit_count = Task.objects.filter(Zone="Cockpit").count()
    cabin = Task.objects.filter(Zone="Cabin")
    cabin_count = Task.objects.filter(Zone="Cabin").count()
    wing = Task.objects.filter(Zone="Wing")
    wing_count = Task.objects.filter(Zone="Wing").count()
    landinggear = Task.objects.filter(Zone="Landing Gear")
    landinggear_count = Task.objects.filter(Zone="Landing Gear").count()
    fuselage = Task.objects.filter(Zone="Fuselage")
    fuselage_count = Task.objects.filter(Zone="Fuselage").count()
    engine = Task.objects.filter(Zone="Engine")
    engine_count = Task.objects.filter(Zone="Engine").count()
    empennage = Task.objects.filter(Zone="Empennage")
    empennage_count = Task.objects.filter(Zone="Empennage").count()
    avionic = Task.objects.filter(Zone="Avionic")
    avionic_count = Task.objects.filter(Zone="Avionic").count()
    my_task_count = Task.objects.filter(Assign=first_name).count
    mytask_wait_review_count = Task.objects.filter(Assign=first_name).filter(Reviewed=True).exclude(Task_Performed='').count
    wait_review = Task.objects.filter(Assign=first_name).exclude(Task_Performed='').exclude(Reviewed=True)
    my_task_reviewed_count = Task.objects.filter(Assign=first_name).filter(Reviewed=True).exclude(Task_Performed='').count
    if 'look' in request.POST:
            lk = request.POST.get("lookingfor")
            if lk.isdigit() == True:
                result = Task.objects.filter(Q(id__icontains=lk))
                if result == '<QuerySet []>':
                    result = 'Task Not Found.'
                    return render(request,"search.html",{"result":result})
                return render(request,"mechanic/search.html",{"result":result})
            else:
                result = Task.objects.filter(Q(Task_name__icontains=lk))
                if result == '<QuerySet []>':
                    result = None
                    return redirect("search",{"result":result})
                return render(request,"mechanic/search.html",{
                    "result":result,
                    "first_name":first_name,
                    "position":position,
                    "mechanic":mechanic,
                    "task_overdue_count":task_overdue_count,
                    "my_task_count":my_task_count,
                    "user_id":user_id,
                    "mytask_wait_review_count":mytask_wait_review_count,
                    "wait_review":wait_review,
                    "my_task_reviewed_count":my_task_reviewed_count,})    
    if 'update_form' in request.POST:
        form = TaskForm(request.POST)
        form_target = Task.objects.filter(id=request.POST.get("id"))
        print(request.POST)
        tp = request.POST.get("Task_Performed")
        ub = first_name
        ub_id = user_id
        ud = timezone.now()
        form_target.update(Task_Performed=tp,Update_Date=ud,Update_By=ub,Update_By_ID=ub_id)
        return redirect(request.path_info)  
    return render(request,'mechanic/mytask_wait_review.html',{
        'first_name':first_name,
        'position':position,
        'task_overdue_count':task_overdue_count,
        "mechanic":mechanic,
        "updateform":updateform,
        "cockpit":cockpit,
        "cabin":cabin,
        "wing":wing,
        "landinggear":landinggear,
        "fuselage":fuselage,
        "engine":engine,
        "empennage":empennage,
        "avionic":avionic,
        "cockpit_count":cockpit_count,
        "cabin_count":cabin_count,
        "wing_count":wing_count,
        "landinggear_count":landinggear_count,
        "fuselage_count":fuselage_count,
        "engine_count":engine_count,
        "empennage_count":empennage_count,
        "avionic_count":avionic_count,
        "my_task_count":my_task_count,
        "user_id":user_id,
        "mytask_wait_review_count":mytask_wait_review_count,
        "wait_review":wait_review,
        "my_task_reviewed_count":my_task_reviewed_count,
    })


@login_required
def search(request,result,first_name,position,user_id):
    form = TaskForm
    my_task_reviewed_count = Task.objects.filter(Assign=first_name).filter(Reviewed=True).exclude(Task_Performed='').count
    return render(request,'search.html',{
        "result":result,
        "first_name":first_name,
        "position":position,
        "form":form,
        "user_id":user_id,
        "my_task_reviewed_count":my_task_reviewed_count})


def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('home')    