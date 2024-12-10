import requests
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from .forms import CityForm
from .models import city
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from decouple import os
from dotenv import load_dotenv

load_dotenv()


def index(request):
    new_city, url, token_key = None, '', str(os.getenv('TOKEN_KEY', ''))
    error_msg, message, message_class = '', '', ''
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            new_city = form.cleaned_data['name']
            url = f'http://api.openweathermap.org/data/2.5/weather?q={new_city}&units=metric&appid={token_key}'
            current_city_count = city.objects.filter(name=new_city).count()
            if current_city_count == 0:
                r = requests.get(url).json()
                if r['cod'] == 200:
                    form.save()
                else:
                    error_msg = "City does not exist"
            else:
                error_msg = "City already exists in the database!"
        if error_msg:
            message = error_msg
            message_class = 'alert-danger'
        else:
            message = "City added succesfully!"
            message_class = "alert-success"
    
    form = CityForm()
    cities = city.objects.all()

    weather_data = []

    for c in cities:
        url = f'http://api.openweathermap.org/data/2.5/weather?q={c}&units=metric&appid={token_key}'
        r = requests.get(url).json()
        city_weather = {
            'city': c.name,
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
        }

        weather_data.append(city_weather)
        
    context = {
        'weather_data' : weather_data,
        'form': form,
        'message':message,
        'message_class':message_class
    }
    return render(request, 'weather/home.html', context)


def about(request):
    return render(request, 'weather/about.html')


def delete_city(request, city_name):
    city.objects.get(name=city_name).delete()
    return redirect('home')


def help(request):
    return render(request, 'weather/help.html')

