import requests
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response


def get_dolar_blue(amount):
    response = requests.get(settings.API_DOLAR_URL)

    if response.status_code == 200:
        tipo_dolar = response.json()
        dolar_blue = float(tipo_dolar[1]['casa']['venta'].replace(',', '.'))
        total_usd = amount / dolar_blue
        return total_usd
    else:
        return Response(
            {"Error message": "No se pudo establecer la conexión con www.dolarsi.com"},
            status=status.HTTP_400_BAD_REQUEST
        )
