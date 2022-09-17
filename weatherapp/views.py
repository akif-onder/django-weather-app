
from django.shortcuts import render
from decouple import config
import requests
from pprint import pprint
from django.contrib import messages
from .models import City

# Create your views here.


def index(request):
    API_KEY = config("API_KEY")
    # city = "Istanbul"
    u_city = request.POST.get("name")

    if u_city:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={u_city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        # print(response.ok)

        if response.ok:
            content = response.json()
            r_city = content["name"]
            if City.objects.filter(name=r_city):
                messages.warning(request, "City already exist")
            else:
                City.objects.create(name=r_city)
                messages.warning(request, "New city added")
        else:
            messages.warning(request, "There is no city.")

    # response = requests.get(url)
    # content =requests.get(url).json()
    # pprint(content)

    # pprint(content["name"])
    # pprint(content["main"]["temp"])
    # pprint(content["weather"][0]["description"])
    # pprint(content["weather"][0]["icon"])

    city_data = []
    cities = City.objects.all()

    for city in cities:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        content = response.json()
        data = {
            "city": content["name"],
            "temp": content["main"]["temp"],
            "icon": content["weather"][0]["icon"],
            "desc": content["weather"][0]["description"]
        }
        city_data.append(data)

    context = {
        "city_data" : city_data
    }

    return render(request, 'weatherapp/index.html', context)
