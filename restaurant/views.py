from django.shortcuts import render
from .forms import BookingForm
from .models import Booking
from django.core import serializers
from datetime import datetime
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def book(request):
    return render(request, 'book.html')

@csrf_exempt
def bookings(request):

    # CREATE BOOKING
    if request.method == 'POST':
        data = json.load(request)

        exist = Booking.objects.filter(
            reservation_date=data['reservation_date'],
            reservation_slot=data['reservation_slot']
        ).exists()

        if not exist:
            Booking.objects.create(
                first_name=data['first_name'],
                reservation_date=data['reservation_date'],
                reservation_slot=data['reservation_slot']
            )
        else:
            return HttpResponse(
                '{"error":1}',
                content_type='application/json'
            )

    # FETCH BOOKINGS
    date = request.GET.get('date', datetime.today().date())

    bookings = Booking.objects.filter(reservation_date=date)

    booking_json = serializers.serialize('json', bookings)

    return HttpResponse(
        booking_json,
        content_type='application/json'
    )

