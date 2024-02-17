from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user
from django.contrib import messages
from .forms import SignUpForm, AddPhysicalInfoAboutBodybuilderForm
from .models import BodyBuilder, PhysicalIndicators, FitnessBracelet
import io
from django.http import HttpResponse
from django.utils import timezone
import random
import datetime
import matplotlib.pyplot as plt
import pylab
from statistics import mean
from django.db.models import Avg
import matplotlib.dates
import pandas as pd
from django.contrib.auth.decorators import login_required
# Create your views here.
def home(request):
    #body_builders = BodyBuilder.objects.all()
    #physical_infos = PhysicalIndicators.objects.all()
    #Check if user is logged in
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        #Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            #BodyBuilder(height = 0, weight = 0, username=username)
            bodybuilder = BodyBuilder.objects.get(username = username)
            bodybuilder_id = bodybuilder.id
            ids =PhysicalIndicators.objects.filter(bodybuilder_id = bodybuilder_id).values_list('id', flat=True)
            dates = FitnessBracelet.objects.filter(id__in = ids).values_list('date', flat=True)
            dates_arr = [date for date in dates]
            if dates_arr[-1] != datetime.date.today():
                generate_physical_indicators_for_last_day(request, bodybuilder_id)
            messages.success(request, 'You are now logged in')
            return redirect('update_info_about_bodybuilder')
        else:
            messages.success(request, 'There was an error Logging in, Please try again...')
            return redirect('home')
    else:
        return render(request, 'home.html')



def logout_user(request):
    logout(request)
    #PhysicalIndicators.objects.all().delete()
    #FitnessBracelet.objects.all().delete()
    #update_physical_indicators_for_last_day()
    #update_row(bodybuilder_id)
    messages.success(request, 'You are now logged out')
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Authenticate and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            #PhysicalIndicators.objects.all().delete()
            #FitnessBracelet.objects.all().delete()
            BodyBuilder(height = 0, weight = 0, username=username).save()
            bodybuilder = BodyBuilder.objects.get(username = username)
            bodybuilder_id = bodybuilder.id
            update_row(bodybuilder_id)
            generate_physical_indicators_for_register(request, bodybuilder_id)
            messages.success(request, 'You have successfully registered!')
            return redirect('update_info_about_bodybuilder')
    else:
        form = SignUpForm()

        return render(request, 'register.html', {'form': form})
    
    return render(request, 'register.html', {'form': form})

def add_physical_info_about_bodybuilder(request):
    form = AddPhysicalInfoAboutBodybuilderForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == 'POST':
            if form.is_valid():
                add_physical_info_about_bodybuilder = form.save()
                messages.success(request, 'You have successfully added your physical info!')
                return redirect('home')
        return render(request, 'add_physical_info_about_bodybuilder.html', {'form': form})
    else:
        messages.success(request, 'You must be registered to add your physical info!')
        return redirect('home')
    
# def add_physical_indicators(request):
#     form = AddPhysicalIndicators(request.POST or None)
#     if request.user.is_authenticated:
#         if request.method == 'POST':
#             if form.is_valid():
#                 add_physical_indicators = form.save()
#                 messages.success(request, 'You have successfully added your physical indicators!')
#                 return redirect('home')
#         return render(request, 'add_physical_indicators.html', {'form': form})
#     else:
#         messages.success(request, 'You must be registered to add your physical indicators!')
#         return redirect('home')
    

def generate_physical_indicators(request):
    #physical_infos = PhysicalIndicators.objects.all()
    #fitness_bracelets = FitnessBracelet.objects.all()
    if request.user.is_authenticated:
        #if request.method == 'POST': 
            # today = timezone.now().date()
            # start_date = today - timedelta(days=today.weekday())
            current_date = datetime.date.today()

# Вычисляем количество дней, прошедших с последнего понедельника
            days_since_monday = (current_date.weekday() - 0) % 7

            # Вычисляем дату понедельника, прошедшего на указанное количество дней назад
            monday_date = current_date - datetime.timedelta(days=days_since_monday)
            
            # Генерируем данные для указанного количества дней
            for i in range(days_since_monday+1):
                date_1 = monday_date + datetime.timedelta(days=i)
                #date = start_date + timedelta(days=i)
                pulse_1 = random.randint(60, 100)
                steps_1 = random.randint(1000, 10000)
                distance_1 = steps_1 * 0.7
                #sleep_hours_1 = datetime.timedelta(hours=random.randint(1, 12), minutes=random.randint(0, 59))
                physical_indicators = PhysicalIndicators(id=i+1, bodybuilder_id=1, pulse=pulse_1, steps=steps_1, distance=distance_1)
                physical_indicators.save()
                fitnes = FitnessBracelet(id=i+1, physical_indicators_id=i+1, date=date_1)
                
                fitnes.save()
    return redirect('home')

def generate_physical_indicators_for_last_day(request, bodybuilder_id):
    if request.user.is_authenticated:
        #if request.method == 'POST': 
            # today = timezone.now().date()
            # start_date = today - timedelta(days=today.weekday())
            current_date = datetime.date.today()
            # if current_date.weekday() == 0:
            #     PhysicalIndicators.objects.all().delete()
            #     FitnessBracelet.objects.all().delete()
            
# Вычисляем количество дней, прошедших с последнего понедельника
            #days_since_monday = (current_date.weekday() - 0) % 7

            # Вычисляем дату понедельника, прошедшего на указанное количество дней назад
            #monday_date = current_date - datetime.timedelta(days=days_since_monday)
            #id_last_record = PhysicalIndicators.objects.values_list('id', flat=True)
            last_record = PhysicalIndicators.objects.latest("id")
            last_record_id = last_record.id
            # Генерируем данные для указанного количества дней
           
            #date_1 = monday_date + datetime.timedelta(days=last_record_id)
            #date = start_date + timedelta(days=i)
            pulse_1 = random.randint(60, 100)
            steps_1 = random.randint(1000, 10000)
            distance_1 = steps_1 * 0.7
            #sleep_hours_1 = datetime.timedelta(hours=random.randint(1, 12), minutes=random.randint(0, 59))
            physical_indicators = PhysicalIndicators(id=last_record_id+1, bodybuilder_id=bodybuilder_id, pulse=pulse_1, steps=steps_1, distance=distance_1)
            physical_indicators.save()
            fitnes = FitnessBracelet(id=last_record_id+1, physical_indicators_id=last_record_id+1, date=current_date)
            
            fitnes.save()
    return redirect('home')

def generate_physical_indicators_for_register(request, bodybuilder_id):
    #physical_infos = PhysicalIndicators.objects.all()
    #fitness_bracelets = FitnessBracelet.objects.all()
    if request.user.is_authenticated:
        #if request.method == 'POST': 
            # today = timezone.now().date()
            # start_date = today - timedelta(days=today.weekday())
            current_date = datetime.date.today()

# Вычисляем количество дней, прошедших с последнего понедельника
            days_since_monday = (current_date.weekday() - 0) % 7

            # Вычисляем дату понедельника, прошедшего на указанное количество дней назад
            monday_date = current_date - datetime.timedelta(days=days_since_monday)

            # Генерируем данные для указанного количества дней
            last_record = PhysicalIndicators.objects.latest("id")
            last_record_id = last_record.id
            date_1 = monday_date + datetime.timedelta(days=days_since_monday)
            #date = start_date + timedelta(days=i)
            pulse_1 = random.randint(60, 100)
            steps_1 = random.randint(1000, 10000)
            distance_1 = steps_1 * 0.7
            #sleep_hours_1 = datetime.timedelta(hours=random.randint(1, 12), minutes=random.randint(0, 59))
            physical_indicators = PhysicalIndicators(id=last_record_id, bodybuilder_id=bodybuilder_id, pulse=pulse_1, steps=steps_1, distance=distance_1)
            physical_indicators.save()
            fitnes = FitnessBracelet(id=last_record_id, physical_indicators_id=last_record_id, date=date_1)
            
            fitnes.save()
    return redirect('home')

def update_physical_indicators_for_last_day():

        
    #if request.method == 'POST': 
        # today = timezone.now().date()
        # start_date = today - timedelta(days=today.weekday())
        current_date = datetime.date.today()

# Вычисляем количество дней, прошедших с последнего понедельника
        days_since_monday = (current_date.weekday() - 0) % 7

        # Вычисляем дату понедельника, прошедшего на указанное количество дней назад
        monday_date = current_date - datetime.timedelta(days=days_since_monday)

        # Генерируем данные для указанного количества дней
        
        date_1 = monday_date + datetime.timedelta(days=days_since_monday)
        #date = start_date + timedelta(days=i)
        pulse_1 = random.randint(60, 100)
        steps_1 = random.randint(1000, 10000)
        distance_1 = steps_1 * 0.7
        #sleep_hours_1 = datetime.timedelta(hours=random.randint(1, 12), minutes=random.randint(0, 59))
        current_record = PhysicalIndicators.objects.get(id=days_since_monday)
        #current_record_bracelet = FitnessBracelet.objects.get()
        current_record.pulse = pulse_1
        current_record.steps = steps_1
        current_record.distance = distance_1
        
        #physical_indicators = PhysicalIndicators(id=days_since_monday, bodybuilder_id=1, pulse=pulse_1, steps=steps_1, distance=distance_1)
        current_record.save()
   

def manipulating_with_indicators(request):
  
    # pulse = PhysicalIndicators.objects.values_list('pulse', flat=True)
    # date = FitnessBracelet.objects.values_list('date', flat=True)
    # plt.plot(date, pulse)
    # plt.title('Pulse statistic')
    # plt.xlabel('Date')
    # plt.ylabel('Pulse')
    # graph_path = 'D:/health_monotoring/health_monotoring/media/graph.png'
    # plt.savefig(graph_path)
    
    return render(request, 'manipulating_with_indicators.html')

def table(request):
    user= get_user(request)
    username = user.username
    bodybuilder = BodyBuilder.objects.get(username = username)
    bodybuilder_id = bodybuilder.id
    pulses = PhysicalIndicators.objects.filter(bodybuilder_id = bodybuilder_id).values_list('pulse', flat=True)
    steps = PhysicalIndicators.objects.filter(bodybuilder_id = bodybuilder_id).values_list('steps', flat=True)
    distances = PhysicalIndicators.objects.filter(bodybuilder_id = bodybuilder_id).values_list('distance', flat=True)
    ids =PhysicalIndicators.objects.filter(bodybuilder_id = bodybuilder_id).values_list('id', flat=True)
    dates = FitnessBracelet.objects.filter(id__in = ids).values_list('date', flat=True)
    items = [{'date':date,'pulse': pulse,'steps': steps, 'distance': distance} for date, pulse, steps, distance in zip(dates,pulses,steps,distances)]
    return render(request, 'table.html', {'items': items})

def update_info_about_bodybuilder(request):
    if request.user.is_authenticated:
        user = get_user(request)
        username = user.username
        bodybuilder = BodyBuilder.objects.get(username = username)
        bodybuilder_id = bodybuilder.id

        current_record = BodyBuilder.objects.get(id=bodybuilder_id)
        form = AddPhysicalInfoAboutBodybuilderForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            
            return redirect('home')
        return render(request, 'update_info_about_bodybuilder.html', {'form':form})
    else:
        messages.success(request, "You Must Be Logged In...")
        return redirect('home')
     
def update_row(bodybuilder_id):
    current_record = BodyBuilder.objects.get(id=bodybuilder_id)
    current_record.height = 0
    current_record.weight = 0
    current_record.save()

def create_graphic(request):
    if request.user.is_authenticated:
        user= get_user(request)
        username = user.username
        bodybuilder = BodyBuilder.objects.get(username = username)
        bodybuilder_id = bodybuilder.id
        pulses = PhysicalIndicators.objects.filter(bodybuilder_id = bodybuilder_id).values_list('pulse', flat=True)
        #pulses = PhysicalIndicators.objects.values_list('pulse', flat=True)
        #dates = FitnessBracelet.objects.values_list('date', flat=True)
        ids =PhysicalIndicators.objects.filter(bodybuilder_id = bodybuilder_id).values_list('id', flat=True)
        dates = FitnessBracelet.objects.filter(id__in = ids).values_list('date', flat=True)
        
        data = [{'date': date, 'pulse': pulse} for date, pulse in zip(dates, pulses)]

    # Создать списки дат и значений пульса
        dates_1 = [entry['date'] for entry in data]
        values = [entry['pulse'] for entry in data]
     
        axes = pylab.subplot(1, 1, 1)
        axes.tick_params(axis='x', labelrotation=55)
        # Создать график
        plt.figure(figsize=(10, 8))
        plt.plot(dates_1, values, marker='o')
        #plt.xlim(min(dates), max(dates))
        #plt.xticks(range(min(dates_1), max(dates_1))) 
        
        if len(dates_1)==1:
            x_ticks_labels = dates_1
            plt.xticks(dates_1, x_ticks_labels)
        else:
            plt.gca().xaxis.set_major_locator(plt.MultipleLocator(1))
            axes.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%d.%m.%Y"))
        plt.yticks(range(min(values)-1, max(values)+1))
        #plt.ylim(min(pulses), max(pulses)+2)
        plt.xlabel('Дата')
        plt.ylabel('Значение пульса')
        plt.tight_layout()
        # Сохранить график в байтовый поток
        image_stream = io.BytesIO()
        plt.savefig(image_stream, format='png')
        plt.close()

        # Вернуть график в виде HTTP-ответа
        image_stream.seek(0)
        response = HttpResponse(image_stream, content_type='image/png')
        return response
    
def create_diagram_for_pulse(request):
    if request.user.is_authenticated:
        user= get_user(request)
        username = user.username
        bodybuilder = BodyBuilder.objects.get(username = username)
        bodybuilder_id = bodybuilder.id
        pulses = PhysicalIndicators.objects.filter(bodybuilder_id = bodybuilder_id).values_list('pulse', flat=True)
        #pulses = PhysicalIndicators.objects.values_list('pulse', flat=True)
        #dates = FitnessBracelet.objects.values_list('date', flat=True)
        ids =PhysicalIndicators.objects.filter(bodybuilder_id = bodybuilder_id).values_list('id', flat=True)
        dates = FitnessBracelet.objects.filter(id__in = ids).values_list('date', flat=True)
        #pulses = PhysicalIndicators.objects.values_list('pulse', flat=True)
        #dates = FitnessBracelet.objects.values_list('date', flat=True)
        data = [{'date': date, 'pulse': pulse} for date, pulse in zip(dates, pulses)]

    # Создать списки дат и значений пульса
        dates_1 = [entry['date'] for entry in data]
        values = [entry['pulse'] for entry in data]
     
        axes = pylab.subplot(1, 1, 1)
        axes.tick_params(axis='x', labelrotation=55)
        # Создать график
        plt.figure(figsize=(10, 8))
        plt.bar(dates_1, values)
        #plt.xlim(min(dates), max(dates))
        #plt.xticks(range(min(dates_1), max(dates_1))) 
        plt.gca().xaxis.set_major_locator(plt.MultipleLocator(1))
        axes.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%d.%m.%Y"))
        y_ticks_labels = values
        plt.yticks(values, y_ticks_labels)
        #plt.ylim(min(pulses), max(pulses)+2)
        plt.xlabel('Дата')
        plt.ylabel('Значение пульса')
        plt.tight_layout()
        # Сохранить график в байтовый поток
        image_stream = io.BytesIO()
        plt.savefig(image_stream, format='png')
        plt.close()

        # Вернуть график в виде HTTP-ответа
        image_stream.seek(0)
        response = HttpResponse(image_stream, content_type='image/png')
        return response

def create_diagram_for_steps(request):
    if request.user.is_authenticated:
        user= get_user(request)
        username = user.username
        bodybuilder = BodyBuilder.objects.get(username = username)
        bodybuilder_id = bodybuilder.id
        steps = PhysicalIndicators.objects.filter(bodybuilder_id = bodybuilder_id).values_list('steps', flat=True)
        #pulses = PhysicalIndicators.objects.values_list('pulse', flat=True)
        #dates = FitnessBracelet.objects.values_list('date', flat=True)
        ids =PhysicalIndicators.objects.filter(bodybuilder_id = bodybuilder_id).values_list('id', flat=True)
        dates = FitnessBracelet.objects.filter(id__in = ids).values_list('date', flat=True)
        #steps = PhysicalIndicators.objects.values_list('steps', flat=True)
        #dates = FitnessBracelet.objects.values_list('date', flat=True)
        data = [{'date': date, 'steps': steps} for date, steps in zip(dates, steps)]

    # Создать списки дат и значений пульса
        dates_1 = [entry['date'] for entry in data]
        values = [entry['steps'] for entry in data]
     
        axes = pylab.subplot(1, 1, 1)
        axes.tick_params(axis='x', labelrotation=55)
        # Создать график
        plt.figure(figsize=(8, 6))
        plt.bar(dates_1, values)
        #plt.xlim(min(dates), max(dates))
        #plt.xticks(range(min(dates_1), max(dates_1))) 
        plt.gca().xaxis.set_major_locator(plt.MultipleLocator(1))
        axes.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%d.%m.%Y"))
        y_ticks_labels = values
        plt.yticks(values, y_ticks_labels)
        #plt.ylim(min(pulses), max(pulses)+2)
        plt.xlabel('Дата')
        plt.ylabel('Количество шагов за день')
        plt.tight_layout()
        # Сохранить график в байтовый поток
        image_stream = io.BytesIO()
        plt.savefig(image_stream, format='png')
        plt.close()

        # Вернуть график в виде HTTP-ответа
        image_stream.seek(0)
        response = HttpResponse(image_stream, content_type='image/png')
        return response

def recomendation(request):
    recomendations = []
    values = []
    user= get_user(request)
    username = user.username
    bodybuilder = BodyBuilder.objects.get(username = username)
    bodybuilder_id = bodybuilder.id
        
    if request.user.is_authenticated:
        height = BodyBuilder.objects.get(id=bodybuilder_id).height
        weight = BodyBuilder.objects.get(id=bodybuilder_id).weight
        steps = PhysicalIndicators.objects.filter(bodybuilder_id = bodybuilder_id).values_list('steps', flat=True)
        pulse = PhysicalIndicators.objects.filter(bodybuilder_id = bodybuilder_id).values_list('pulse', flat=True)

        
        #pulse = PhysicalIndicators.objects.values_list('pulse', flat=True)
        #steps = PhysicalIndicators.objects.values_list('steps', flat=True)
        avg_pulse = round(mean(pulse))
        avg_steps = round(mean(steps))
        
        # values.append(avg_pulse)
        # values.append(avg_steps)

        itm = round(weight / ((height/100) ** 2), 2)
        #values.append(itm)

        values = [{'pulse': avg_pulse,'steps': avg_steps, 'itm': itm}]
        if itm > 24.9:
            recomendations.append('Вам следует увеличить количество физических нагрузок')
        if avg_pulse > 90:
            recomendations.append('Вам следует обратиться к врачу')
        if avg_steps < 6000:
            recomendations.append('Вам следует больше гулять на свежем воздухе')
       
        return render(request,'recomendation.html', {'values': values, 'recomendations': recomendations})
        
def assessment_of_physical_conditions(request):
    assessments = []
    user= get_user(request)
    username = user.username
    bodybuilder = BodyBuilder.objects.get(username = username)
    bodybuilder_id = bodybuilder.id
    if request.user.is_authenticated:
        height = BodyBuilder.objects.get(id=bodybuilder_id).height
        weight = BodyBuilder.objects.get(id=bodybuilder_id).weight
        itm = round(weight / ((height/100) ** 2), 2)
        #
        if height >= 180:
            assessments.append('Высокий')
        if 180 > height >=165:
            assessments.append('Средний')
        if height < 165:
            assessments.append('Низкий')

        if itm >= 30:
            assessments.append('Неудовлетворительно\n(слишком высокий)')
        if 30 > itm >= 25:
            assessments.append('Удовлетворительно')
        if 25 > itm >= 18.5:
            assessments.append('Превосходно')
        if itm < 18.5:
            assessments.append('Неудовлетворительно\n(слишком низкий)')
        steps = PhysicalIndicators.objects.filter(bodybuilder_id = bodybuilder_id).values_list('steps', flat=True)
        pulse = PhysicalIndicators.objects.filter(bodybuilder_id = bodybuilder_id).values_list('pulse', flat=True)

        distance =  PhysicalIndicators.objects.filter(bodybuilder_id = bodybuilder_id).values_list('distance', flat=True)
        avg_pulse = round(mean(pulse))
        avg_steps = round(mean(steps))
        avg_distance = round(mean(distance))

        values = [{'height': height, 'weight': weight, 'pulse': avg_pulse,'steps': avg_steps, 'distance': avg_distance}]

        if avg_pulse >= 90:            
            assessments.append('Неудовлетворительно\n(слишком высокий)')
        if 90 > avg_pulse >= 80:
            assessments.append('Удовлетворительно')
        if 80 > avg_pulse > 60:
            assessments.append('Превосходно')
        if avg_pulse < 60:
            assessments.append('Неудовлетворительно\n(слишком низкий)')

        if avg_steps < 6000:
            assessments.append('Неудовлетворительно') 
        if 6000 <= avg_steps <= 8000:
            assessments.append('Удовлетворительно')
        if 8000 < avg_steps <= 10000:
            assessments.append('Превосходно')

        if avg_distance < 4200:
            assessments.append('Неудовлетворительно')
        if 4200 <= avg_distance <= 5600:
            assessments.append('Удовлетворительно')
        if 5600 < avg_distance <= 7000: 
            assessments.append('Превосходно')
        return render(request, 'assessment_of_physical_conditions.html', {'values': values, 'assessments': assessments})
# def manipulating_with_indicators(request):
   
#     pulse = PhysicalIndicators.objects.all()
#     date = FitnessBracelet.objects.all()
#     stats = QuerySetStats(pulse, 'date')
#     date_pulse = stats.time_series(date, 'pulse')
#     dates = [entry[0] for entry in date_pulse]
#     pulse_values = [entry[1] for entry in date_pulse]
    
#     return render(request, 'manipulating_with_indicators.html', {'dates': dates, 'pulse_values': pulse_values})
# def manipulating_with_indicators(request):
#     if request.user.is_authenticated:
#         pulse = PhysicalIndicators.objects.values_list('pulse', flat=True)
#         date = FitnessBracelet.objects.values_list('date', flat=True)
#         fig, ax = plt.subplots()

#         # Построение графика
#         ax.plot(date, pulse)

#         # Создание объекта для записи картинки в буфер
#         buf = io.BytesIO()

#         # Сохранение графика в буфер
#         plt.savefig(buf, format='png')

#         # Очистка и закрытие графика
#         plt.close(fig)

#         # Перемещение указателя буфера в начало
#         buf.seek(0)

#         # Генерация HTML шаблона с картинкой
#         template = loader.get_template('manipulating_with_indicators.html')
#         context = {'image': buf.getvalue()}
#         html = template.render(context)

#         return HttpResponse(html)
