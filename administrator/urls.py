from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admindb',views.admindb,name='admindb'),
    path('logout',views.logout,name='logout'),
    path('change_pwd',views.change_pwd,name='change_pwd'),
    path('change',views.change,name='change'),
    path('enquiry',views.enquiry,name='enquiry'),
    path('pending_response',views.pending_response,name='pending_response'),
]
