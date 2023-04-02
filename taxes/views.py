from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView, ListView, DetailView
from .models import (
    Entry, 
    Status,
    PaymentMethod,
    Category
)
from .forms import EntryForm
from .helpers import generate_spending_data
from django.shortcuts import get_object_or_404, redirect
from uuid import UUID
import json
from django.contrib.auth import get_user_model
from decimal import Decimal
from datetime import datetime, timedelta
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.decorators import user_passes_test
from accounts.models import CustomUser
from django.utils import timezone
from django.contrib.sessions.models import Session
import matplotlib.pyplot as plt

@user_passes_test(lambda u: u.is_superuser)
def is_superuser(user):
    return user.is_superuser

class DashboardView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Entry
    context_object_name = 'entries'
    template_name = 'taxes/dashboard.html'

    def test_func(self):
        return self.request.user.is_superuser
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        chart_data = generate_spending_data(6)
        chart_labels = []
        chart_values = []
        for label, total in zip(chart_data['labels'], chart_data['totals']):
            chart_labels.append(label)
            chart_values.append(float(total))

        # Retrieve active sessions
        active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
        user_ids = []

        for session in active_sessions:
            data = session.get_decoded()
            user_id = data.get('_auth_user_id', None)
            if user_id:
                user_ids.append(user_id)

        # Get custom user model 
        User = get_user_model()
        # Get online users from User Model 
        online_users = User.objects.filter(id__in=user_ids)

        context['entry_form'] = EntryForm()
        context['payment_methods'] = PaymentMethod.objects.all()
        context['categories'] = Category.objects.all()
        context['statuses'] = Status.objects.all()
        context['users'] = User.objects.all()
        context['online_users'] = online_users
        # Add the chart image path to the context
        context['labels'] = chart_labels
        context['values'] = chart_values
        return context
def change_status(request, pk):
    entry = get_object_or_404(Entry, pk=pk)
    if request.method == 'POST':
        tmp_status = request.POST.get('status')
        status = Status.objects.get(name=tmp_status)
        entry.status = status
        entry.save()
    return redirect('taxes:dashboard')

def change_title(request, pk):
    entry = get_object_or_404(Entry, pk=pk)
    if request.method == 'POST':
        body = json.loads(request.body)
        title = body.get('title')
        if title is None:
             return JsonResponse({'success': False, 'message': 'Title cannot be empty'})
        entry.title = title
        entry.save()
        return JsonResponse({'success': True, 'new_title': entry.title})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

def change_description(request, pk):
    entry = get_object_or_404(Entry, pk=pk)
    if request.method == 'POST':
        body = json.loads(request.body)
        description = body.get('description')
        if description is None:
             return JsonResponse({'success': False, 'message': 'Description cannot be empty'})
        entry.description = description
        entry.save()
        return JsonResponse({'success': True, 'new_description': entry.description})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

def update_receipt(request, pk):
    entry = get_object_or_404(Entry, pk=pk)
    if request.method == 'POST':
        receipt_file = request.FILES.get('file', None)
        if receipt_file is None:
            return JsonResponse({'success': False, 'message': 'Image cannot be empty'})
        entry.receipt_img = receipt_file
        entry.save()
        return JsonResponse({'success': True, 'message': 'Success Save'})
    return JsonResponse({'success': False, 'message': 'Invalid request'})


def create_entry(request):
    if request.method == 'POST':
        form = EntryForm(request.POST, request.FILES)
        if form.is_valid():
            entry = form.save()
            return JsonResponse({'success':True})
    
    return JsonResponse({'success':False})

def change_body(request, pk):
    if request.method == 'POST':
        try:
            # Get the entry object
            entry = get_object_or_404(Entry, pk=pk)

            # Update the fields
            entry.category = get_object_or_404(Category, name=request.POST.get('category'))
            entry.tax_year = request.POST.get('tax-year')
            entry.total_price = Decimal(request.POST.get('total-price'))
            entry.purchase_date = datetime.strptime(request.POST.get('purchase-date'), '%Y-%m-%d')
            entry.status = get_object_or_404(Status, name=request.POST.get('status'))
            entry.payment_method = get_object_or_404(PaymentMethod, name=request.POST.get('payment-method'))
            User = get_user_model()
            entry.user = get_object_or_404(User, username=request.POST.get('user'))

            # Save the entry
            entry.save()

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    return HttpResponse('Invalid request method', status=405)

def delete_entry(request, pk):
    if request.method == 'POST':
        entry = get_object_or_404(Entry, pk=pk)
        entry.delete()
        return redirect('taxes:dashboard')
    return HttpResponse('Invalid request method', status=405)

class EntryDetailView(DetailView):
    model = Entry
    template_name = 'taxes/entry_detail.html'

def get_entry(request, pk):
    entry = get_object_or_404(Entry, pk=pk)
    data = {
        "title": entry.title,
        "description": entry.description,
        "memo": entry.memo,
        "user": entry.user.username,
        "total_price": str(entry.total_price),
        "tax_year": str(entry.tax_year),
        "purchase_date": str(entry.purchase_date),
        "status": entry.status.name,
        "category": entry.category.name,
        "payment_method": entry.payment_method.name,
        "created_at": str(entry.created_at),
        "updated_at": str(entry.updated_at),
        "img": str(entry.receipt_img),
    }
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type="application/json")
