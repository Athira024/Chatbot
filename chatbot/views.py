from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from datetime import datetime
from Chatbot import models
import json
from . import ChatBot
from django.core.serializers import serialize
from django.http import JsonResponse
def home(request):
    return render(request,'home/home.html')

def login(request):
    return render(request,'login/index.html') 

def check_login(request):
    username=request.POST["username"]
    password=request.POST["password"]
    log_info=models.Login.objects.filter(username=username,password=password)
    for info in log_info:
        if info.username==username and info.password==password:
            if info.usertype=='Admin':
                request.session['semail']=info.username
                request.session['usertype']=info.usertype
                return redirect("../administrator/admindb")
            else:
                return redirect("login")
    messages.error(request, 'invalid data entered')
    return redirect("login")    

def forgot_pwd(request):
    return render(request,'login/forgot_pwd.html') 

def save_enquiry(request):
    full_name=request.POST['full_name']
    address=request.POST['address']
    phone_no=request.POST['phone_no']
    email=request.POST['email']
    message=request.POST['message']
    obj_chat=models.Enquiry(full_name=full_name,address=address,phone_no=phone_no,email=email,message=message)
    obj_chat.save()
    messages.success(request,'Message send successfully!')
    return redirect('home')

def enquiry_form(request):
    return render(request,'home/enquiry_form.html')

def about(request):
    return render(request,'home/about.html')

def ug_courses(request):
    return render(request,'home/ug_courses.html')

def pg_courses(request):
    return render(request,'home/pg_courses.html')

def phd_courses(request):
    return render(request,'home/phd_courses.html')
def chat(request):
    return render(request,'home/chat.html')
def send_chat(request):
    config="D:\\MainProject\\Chatbot\\Chatbot\\intents.json"
    chat_model="D:\\MainProject\\Chatbot\\Chatbot\\data.pth"

    bot = ChatBot.ChatBot('intents.json', 'data.pth')
    response_data=[]
    if request.method == 'POST':
        cur_date=datetime.now().date()
        token=request.POST['csrfmiddlewaretoken']
        chat_master_list=models.ChatMaster.objects.filter(chat_date=cur_date)
        fk_master_chatid=0
        if len(chat_master_list)==0:
            obj_save=models.ChatMaster(chat_date=cur_date,token=token)
            obj_save.save()
            fk_master_chatid=obj_save.master_chatid
        else:
            for clist in chat_master_list:
                fk_master_chatid=clist.master_chatid
        
        question=request.POST['message']
        position=1
        postedby="You"
        obj_saved=models.Chat(fk_master_chatid=fk_master_chatid,response=question,position=position,postedby=postedby)
        obj_saved.save()
        answer= bot.get_response(question)
        if answer=='I apologize, I do not have enough information to answer that yet?':
            qdate=datetime.now().date()
            position=1
            # question=request.POST['message']
            response=question
            obj_pending=models.PendingResponse(response=question,date=qdate,position=position)
            obj_pending.save()
        postedby="Bot"
        
        obj_saved=models.Chat(fk_master_chatid=fk_master_chatid,response=answer,position=position,postedby=postedby)
        obj_saved.save()
        chat_master_list_res=models.ChatMaster.objects.raw('select * from chat_master cm join chat c on(cm.master_chatid=c.fk_master_chatid)')
        for chat in chat_master_list_res:
            thisdict = {
                        "response": chat.response,
                        "position": chat.position,
                        "postedby":chat.postedby,
                        }
            response_data.append(thisdict)
         # Convert queryset to list of dictionaries
       # chat_master_list_dict = list(chat_master_list_res.values())
         # Serialize queryset to JSON
        #response_data = serialize('json', response_data)
        # Convert to JSON
        response_data = json.dumps(response_data)
        
        # Return JSON response
    return HttpResponse(response_data)
def chat_image(request):
     return render(request,'home/chat_image.html') 
    
