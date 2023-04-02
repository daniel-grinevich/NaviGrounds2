from datetime import datetime, timedelta, date
from .models import Entry
from django.db.models import Sum

def get_last_x_months(x):
    today = date.today()
    delta_days = 30 * x
    x_months_ago = today - timedelta(days=delta_days)
    return x_months_ago.strftime("%Y-%m-%d"), today.strftime("%Y-%m-%d")

def generate_spending_data(months):
    start_date, end_date_str = get_last_x_months(x=months)
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

    print(start_date)
    print(end_date)
    entries = Entry.objects.filter(created_at__range=(start_date,end_date))
    print(entries)
    totals = []
    labels = []

    for i in range(months):
        month = (end_date - timedelta(days=i*30)).strftime('%B')
        total = entries.filter(created_at__month=(end_date - timedelta(days=i*30)).month).aggregate(Sum('total_price'))['total_price__sum'] or 0
        totals.append(total)
        labels.append(month)
    return {'labels': labels[::-1], 'totals': totals[::-1]}