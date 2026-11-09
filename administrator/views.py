from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from Chatbot import models
from datetime import datetime, timedelta
# Create your views here.
def admindb(request):
    return render(request,'admin_dashboard/admin.html')

def logout(request):
    return redirect('login')

def change_pwd(request):
    return render(request,'admin_dashboard/change_pwd.html')
def change(request):
    current_pwd=request.POST['currentPassword']
    new_pwd=request.POST['newPassword']
    confirm_pwd=request.POST['confirmPassword']
    username=request.session.get('semail',None)
    if new_pwd==confirm_pwd:
        obj_login=models.Login.objects.get(username=username)
        if obj_login.password==current_pwd:
            obj_login.password=new_pwd
            obj_login.save()
            messages.success(request, 'password changed  successfully')
            return redirect('admindb')
        else:
            messages.success(request,'Invalid Current Password')
            return redirect('change_pwd')
    else:
        messages.success(request,'new and confirm password are not same')
        return redirect('change_pwd')

def enquiry(request):
    enquiries = models.Enquiry.objects.all()
    context={
        'enquiries':enquiries
        }
    return render(request,'admin_dashboard/enquiry.html',context)

def pending_response(request):
    if request.method == 'POST':
        from_date = request.POST.get('startDate')
        to_date = request.POST.get('endDate')

        if from_date and to_date:
            # Filter based on dates
            responses = models.PendingResponse.objects.filter(date__gte=from_date, date__lte=to_date)
        else:
            # No dates provided, return all responses
            responses = models.PendingResponse.objects.all()
    else:
        # GET request, return all responses
        responses = models.PendingResponse.objects.all()

    context = {'responses': responses}
    return render(request, 'admin_dashboard/pending_response.html', context)




