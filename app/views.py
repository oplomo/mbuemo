# app/views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import DisasterReport
import json
import os
from django.conf import settings
from django.shortcuts import render


# 1. Home page view
def home(request):
    return render(request, "home.html")


# app/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import DisasterReport
import json
import os
from django.conf import settings
from django.shortcuts import render
from django.core.mail import send_mail
from django.template.loader import render_to_string


from django.template.loader import render_to_string
from django.utils import timezone
from django.core.mail import send_mail
from django.template.exceptions import TemplateDoesNotExist


@csrf_exempt
def report_location(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            lat = data.get("latitude")
            lng = data.get("longitude")

            if lat is None or lng is None:
                return JsonResponse(
                    {"error": "Missing latitude or longitude"}, status=400
                )

            # Convert to float to ensure valid coordinates
            try:
                lat = float(lat)
                lng = float(lng)
            except (TypeError, ValueError):
                return JsonResponse(
                    {"error": "Invalid latitude or longitude format"}, status=400
                )

            # Save to database
            report = DisasterReport.objects.create(
                latitude=lat, longitude=lng, reported_at=timezone.now()
            )

            # Send emergency email
            try:
                send_emergency_alert(lat, lng)
            except Exception as e:
                print(f"Failed to send email: {str(e)}")
                # Continue even if email fails

            return JsonResponse({"message": "Location saved successfully"})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    return JsonResponse({"error": "Only POST method allowed"}, status=405)


def send_emergency_alert(latitude, longitude):
    subject = "🚨 EMERGENCY LOCATION REPORT"
    google_maps_link = f"https://www.google.com/maps?q={latitude},{longitude}"
    current_time = timezone.now().strftime("%Y-%m-%d %H:%M:%S")

    # Create plain text message as fallback
    plain_message = f"""
EMERGENCY LOCATION ALERT

⚠️ New emergency location reported:

📍 Coordinates:
Latitude: {latitude}
Longitude: {longitude}

🗺️ Google Maps Link:
{google_maps_link}

⏰ Time Reported: {current_time}

Respond immediately!
"""

    # Try to render template first, fallback to plain text
    try:
        message = render_to_string(
            "emergency_email.txt",
            {
                "latitude": latitude,
                "longitude": longitude,
                "maps_link": google_maps_link,
                "time": current_time,
            },
        )
    except TemplateDoesNotExist:
        message = plain_message

    send_mail(
        subject,
        message,
        "adamssquare4@gmail.com",
        ["jerusalem4tech@gmail.com"],
        fail_silently=False,
    )
