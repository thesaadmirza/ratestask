import datetime
import requests

from django.http import JsonResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from api.forms import PriceForm


def validate(date_from, date_to):
    """
    Validating date_from and date_to dates, if they are in right format and also if ranges are acceptable.
    :param date_from:
    :param date_to:
    :return: Boolean
    """
    try:
        datetime.datetime.strptime(date_from, '%Y-%m-%d')
        datetime.datetime.strptime(date_to, '%Y-%m-%d')
        if date_from <= date_to:
            return True
    except ValueError:
        return False


def currency_convert(value):
    """
    Exchnage Rates API Request to fetch Latest Exchange Rate with Base USD Currency.
    :param: Norwegian Value as Price
    :return: Converted USD as Price
    """

    # Request API with BASE USD
    url = 'https://openexchangerates.org/api/latest.json?app_id=' + settings.EXCHANGE_API_KEY

    # Making our request
    response = requests.get(url)
    data = response.json()

    # Convert Norwegian Currency to USD
    rate = data['rates']['NOK']
    convert_nok = int(value / rate)

    return convert_nok


def rates_api(request):
    """
    API Endpoint that takes following Parameters
    :date_from, date_to, origin, destination request:

    and return following data list in json
    :return: day, average price
    """

    date_from = request.GET.get('date_from', False)
    date_to = request.GET.get('date_to', False)
    origin = request.GET.get('origin', False)
    destination = request.GET.get('destination', False)

    if date_from and date_to and origin and destination:
        result = validate(date_from, date_to)
        if not result:
            return JsonResponse("Incorrect Date Format", safe=False, status=403)

        date_from = datetime.datetime.strptime(date_from, '%Y-%m-%d').date()
        date_to = datetime.datetime.strptime(date_to, '%Y-%m-%d').date()

        data = []

        # starting connection before loop to minimize time in starting and closing connection
        cursor = connection.cursor()

        # Loop Through all days from starting to end date.
        while date_from <= date_to:
            cursor.execute(
                "SELECT AVG(price) as avgprice FROM prices JOIN ports ON prices.orig_code=ports.code OR prices.dest_code=ports.code WHERE (prices.orig_code=%s OR ports.parent_slug=%s) AND (prices.dest_code=%s OR ports.parent_slug=%s) AND day=%s",
                [origin, origin, destination, destination, date_from])
            row = cursor.fetchone()

            data_internal = {
                'day': date_from.strftime('%Y-%m-%d'),
                'average_price': int(row[0]) if row[0] else "Null",  # if no result found against parameters
            }
            data.append(data_internal)

            # Increment the day
            date_from = date_from + datetime.timedelta(days=1)

        # DB connection Close
        cursor.close()
        return JsonResponse(data, safe=False, status=200)

    else:
        return JsonResponse('Sorry, you are not allowed to perform this operation', safe=False, status=403)


def rates_null(request):
    """
    API endpoint return an empty value (JSON null) for days which there are less than 3 prices in total.
    that takes following Parameters
    :date_from, date_to, origin, destination request:
    :return: day, average price
    """
    date_from = request.GET.get('date_from', False)
    date_to = request.GET.get('date_to', False)
    origin = request.GET.get('origin', False)
    destination = request.GET.get('destination', False)

    if date_from and date_to and origin and destination:
        result = validate(date_from, date_to)
        if not result:
            return JsonResponse("Incorrect Date Format", safe=False, status=403)

        date_from = datetime.datetime.strptime(date_from, '%Y-%m-%d').date()
        date_to = datetime.datetime.strptime(date_to, '%Y-%m-%d').date()

        # starting connection before loop to minimize time in starting and closing connection
        cursor = connection.cursor()
        data = []

        # Loop Through all days from starting to end date.
        while date_from <= date_to:
            cursor.execute(
                "SELECT AVG(p.price) as avgprice FROM  prices as p inner join (SELECT  prices.day from prices JOIN ports ON prices.orig_code=ports.code OR prices.dest_code=ports.code WHERE (prices.orig_code=%s OR ports.parent_slug=%s) AND (prices.dest_code=%s OR ports.parent_slug=%s) AND prices.day=%s GROUP BY prices.day HAVING COUNT(prices.price) > 3) d on d.day=p.day group by p.day",
                [origin, origin, destination, destination, date_from])
            row = cursor.fetchone()

            data_internal = {
                'day': date_from.strftime('%Y-%m-%d'),
                'average_price': int(row[0]) if row else "Null",  # if no result found against parameters
            }
            data.append(data_internal)

            # Increment the day
            date_from = date_from + datetime.timedelta(days=1)

        # DB connection Close
        cursor.close()
        return JsonResponse(data, safe=False, status=200)

    else:
        return JsonResponse('Sorry, you are not allowed to perform this operation', safe=False, status=403)


@csrf_exempt  # excempted for the sake of assignment
def price_insert(request):
    """
    API endpoint where you can POST a price, including the following parameters: date_from,date_to,origin_code,destination_code,price
    :param request:
    :return: success or Failure
    """
    if request.method == 'POST':
        form = PriceForm(request.POST)
        if form.is_valid():

            # Convert Norwegian Currency to USD
            currency_converted = currency_convert(form.cleaned_data['price'])

            # start database Connection
            cursor = connection.cursor()

            # Cleaned date objects from form
            date_from = form.cleaned_data['date_from']
            date_to = form.cleaned_data['date_to']

            while date_from <= date_to:
                try:
                    cursor.execute(
                        "INSERT INTO prices (orig_code, dest_code, day, price) VALUES(%s, %s, %s, %s)",
                        [form.cleaned_data['orig_code'], form.cleaned_data['destination_code'],
                         date_from,
                         currency_converted])
                except Exception as e:
                    # Error may occur due to not available of origin and destination foreign key relations
                    print("Whoopx, Something Happend")
                    print(e)  # Logg the Error

                # Increment the day
                date_from = date_from + datetime.timedelta(days=1)

            # Close the Connection
            cursor.close()

            return JsonResponse("Successfully Inserted", safe=False, status=200)
        else:
            return JsonResponse(form.errors, safe=False, status=403)
    else:
        return JsonResponse('Sorry, you are not allowed to perform this operation', safe=False, status=403)
