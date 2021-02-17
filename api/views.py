import datetime

from django.http import JsonResponse
from django.db import connection


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
        if date_from < date_to:
            return True
    except ValueError:
        return False


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

        date_from = datetime.datetime.strptime(date_from, '%Y-%m-%d')
        date_to = datetime.datetime.strptime(date_to, '%Y-%m-%d')

        data = []

        # starting connection before loop to minimize time in starting and closing connection
        cursor = connection.cursor()

        # Loop Through all days from starting to end date.
        while date_from <= date_to:
            cursor.execute(
                "SELECT AVG(price) as avgprice  FROM prices JOIN ports ON prices.orig_code=ports.code WHERE (ports.code=%s OR ports.parent_slug=%s) AND (ports.code=%s OR ports.parent_slug=%s) AND day>=%s AND day<=%s",
                [origin, origin, destination, destination, date_from, date_to])
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

        date_from = datetime.datetime.strptime(date_from, '%Y-%m-%d')
        date_to = datetime.datetime.strptime(date_to, '%Y-%m-%d')

        data = []

        # starting connection before loop to minimize time in starting and closing connection
        cursor = connection.cursor()

        # Loop Through all days from starting to end date.
        while date_from <= date_to:
            cursor.execute("SELECT AVG(p.price) as avgprice FROM    prices p inner join (SELECT  day from prices JOIN ports ON prices.orig_code=ports.code WHERE (ports.code=%s OR ports.parent_slug=%s) AND (ports.code=%s OR ports.parent_slug=%s) AND day>=%s AND day<=%s GROUP BY day HAVING COUNT(price) > 3) d on d.day=p.day group by  p.day",
                [origin, origin, destination, destination, date_from, date_to])
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
