from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Date, StatusEntry, Minimum
import datetime


def test(request):
    return HttpResponse('Hello, world!')


def list_diary(request):
    dates = Date.objects.prefetch_related('statusentry', 'minimum').all().order_by('date')
    context = {'title': 'diary一覧', 'dates': dates}
    template = loader.get_template('diary/list_diary.html')
    return HttpResponse(template.render(context, request))


def top(request, year=None, month=None, day=None):
    success_message = None
    error_message = None
    date = f'{datetime.date.today().year}-{datetime.date.today().month}-{datetime.date.today().day}'
    if year and month and day:
        date = f'{year}-{month}-{day}'
    if request.method == 'POST' and 'date' in request.POST:
        date = request.POST.get('date')

        day, created = Date.objects.get_or_create(date=date)
        day = Date.objects.prefetch_related('statusentry', 'minimum').get(date=date)
        se_morning, created = StatusEntry.objects.get_or_create(date=day, time_of_day='1')
        se_return, created = StatusEntry.objects.get_or_create(date=day, time_of_day='2')
        se_bedtime, created = StatusEntry.objects.get_or_create(date=day, time_of_day='3')
        minimum, created = Minimum.objects.get_or_create(date=day)
        try:
            day.up = request.POST.get('up') if request.POST.get('up') else None
            day.down = request.POST.get('down') if request.POST.get('down') else None
            day.return_time = request.POST.get('return_time') if request.POST.get('return_time') else None
            day.nap_time = request.POST.get('nap_time') if request.POST.get('nap_time') else None
            day.note1 = request.POST.get('note1') if request.POST.get('note1') else ''
            day.save()

            # statusentryに各データを保存
            se_morning.physical = request.POST.get('up_physical') if request.POST.get('up_physical') else '0'
            se_morning.mental = request.POST.get('up_mental') if request.POST.get('up_mental') else '0'
            se_return.physical = request.POST.get('down_physical') if request.POST.get('down_physical') else '0'
            se_return.mental = request.POST.get('down_mental') if request.POST.get('down_mental') else '0'
            se_bedtime.physical = request.POST.get('return_time_physical') if request.POST.get('return_time_physical') else '0'
            se_bedtime.mental = request.POST.get('return_time_mental') if request.POST.get('return_time_mental') else '0'
            se_morning.save()
            se_return.save()
            se_bedtime.save()

            # minimumに各データを保存
            minimum.min_physical = min(se_morning.physical, se_return.physical, se_bedtime.physical) if se_morning.physical and se_return.physical and se_bedtime.physical else 0
            minimum.min_mental = min(se_morning.mental, se_return.mental, se_bedtime.mental) if se_morning.mental and se_return.mental and se_bedtime.mental else 0
            minimum.save()
            success_message = '保存しました'
        except Exception as e:
            error_message = f'エラーが発生しました: {e}'
    try:
        day = Date.objects.get(date=date)
    except Date.DoesNotExist:
        day = None
    if day:
        status_entry = StatusEntry.objects.filter(date=day).order_by('time_of_day')
    else:
        status_entry = []
    jst = datetime.timezone(datetime.timedelta(hours=9), 'JST')
    now = datetime.datetime.now(jst)
    after7days = now + datetime.timedelta(days=7)
    aft7d_str = after7days.strftime('%Y-%m-%d')
    dates = Date.objects.filter(date__lte=aft7d_str).prefetch_related('statusentry', 'minimum').all().order_by('date')
    context = {'title': '週間データ', 'dates': dates, 'today': day, 'status_entry': status_entry, 'success_message': success_message, 'error_message': error_message}
    template = loader.get_template('diary/top.html')
    return HttpResponse(template.render(context, request))


# 過去一週間の日記を表示する
def list_diary_week(request):
    year = datetime.date.today().year
    month = datetime.date.today().month
    day = datetime.date.today().day
    dates = Date.objects.filter(date__lte=f'{year}-{month}-{int(day)+7}').prefetch_related('statusentry', 'minimum').all().order_by('date')
    context = {'title': '週間データ', 'dates': dates}
    template = loader.get_template('diary/list_diary.html')
    return HttpResponse(template.render(context, request))


# 一ヶ月の日記を表示する
def list_diary_month(request, year, month):
    dates = Date.objects.filter(date__year=year, date__month=month).prefetch_related('statusentry', 'minimum').all().order_by('date')
    context = {'title': f'{year}年{month}月', 'dates': dates}
    template = loader.get_template('diary/list_diary.html')
    return HttpResponse(template.render(context, request))


def detail_diary(request, date):
    date = Date.objects.get(date=date)
    status_entries = StatusEntry.objects.filter(date=date)
    minimum = Minimum.objects.get(date=date)
    context = {'title': 'diary詳細', 'date': date, 'status_entries': status_entries, 'minimum': minimum}
    template = loader.get_template('diary/detail_diary.html')
    return HttpResponse(template.render(context, request))
