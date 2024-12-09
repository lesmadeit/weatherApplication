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

