from django.urls import path
from api.views import rates_api, rates_null

urlpatterns = [
    path('rates', rates_api, name="rates_api"),
    path('rates_null', rates_null, name="rates_null"),
]
