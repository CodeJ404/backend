from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q, Count, Sum
from django.db.models.functions import ExtractMonth
from .models import ScheduledSession
import matplotlib.pyplot as plt
import io
import base64
import pandas as pd

def is_director(user):
    return user.is_authenticated and user.role == 'director'

@user_passes_test(is_director)
def director_dashboard(request):
    # Performa Instruktur
    instructors = ScheduledSession.objects.values(
        'instructor__username'
    ).annotate(
        total_sessions=Count('id'),
        completed_sessions=Count('id', filter=Q(is_completed=True)),
        completion_rate=100.0 * Count('id', filter=Q(is_completed=True)) / Count('id')
    ).order_by('-completion_rate')

    # Pendapatan Bulanan
    revenue_data = ScheduledSession.objects.values(
        month=ExtractMonth('start_time')
    ).annotate(
        revenue=Sum('fee')  # pastikan 'fee' ada di model ScheduledSession
    ).order_by('month')

    # Grafik 1: Performa
    plt.switch_backend('Agg')
    fig1, ax1 = plt.subplots()
    df1 = pd.DataFrame(list(instructors))
    if not df1.empty:
        df1.plot.bar(x='instructor__username', y='completion_rate', ax=ax1)
        ax1.set_title('Completion Rate by Instructor')
        chart1 = get_graph(fig1)
    else:
        chart1 = None

    # Grafik 2: Revenue
    fig2, ax2 = plt.subplots()
    df2 = pd.DataFrame(list(revenue_data))
    if not df2.empty:
        df2.plot.line(x='month', y='revenue', ax=ax2, marker='o')
        ax2.set_title('Monthly Revenue')
        chart2 = get_graph(fig2)
    else:
        chart2 = None

    context = {
        'chart1': chart1,
        'chart2': chart2,
    }
    return render(request, 'admin/director_dashboard.html', context)

def get_graph(fig):
    buffer = io.BytesIO()
    fig.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png).decode('utf-8')
    buffer.close()
    return graph
