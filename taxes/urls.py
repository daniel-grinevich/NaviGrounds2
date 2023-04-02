from django.urls import path, re_path
from uuid import UUID
from .views import (
    DashboardView, 
    change_status, 
    create_entry, 
    EntryDetailView, 
    get_entry, 
    change_title,
    delete_entry,
    change_description,
    change_body,
    update_receipt,
)
app_name = 'taxes'

urlpatterns = [
    path('dashboard/',DashboardView.as_view(),name='dashboard'),
    path('dashboard/details/<uuid:pk>/', EntryDetailView.as_view(), name='details'),
    path('dashboard/get/<uuid:pk>/', get_entry, name='get_entry'),
    re_path(r'^dashboard/(?P<pk>[\w-]+)/change-status/$', change_status, name='change_status'),
    path('dashboard/create_entry/', create_entry, name='create_entry'),
    path('dashboard/update/<uuid:pk>/title', change_title, name='change_title'),
    path('dashboard/update/<uuid:pk>/description', change_description, name='change_description'),
    path('dashboard/update/<uuid:pk>/body', change_body, name='change_body'),
     path('dashboard/update/<uuid:pk>/receipt', update_receipt, name='update_receipt'),
    path('dashboard/delete/<uuid:pk>/', delete_entry, name='delete_entry'),
]
