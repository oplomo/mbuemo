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


# 2. Report location view
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

            # Save to database
            report = DisasterReport.objects.create(
                latitude=lat, longitude=lng, reported_at=timezone.now()
            )

            # Send emergency email
            send_emergency_alert(lat, lng)

            # Optional: Save all to a JSON file
            all_reports = DisasterReport.objects.values(
                "latitude", "longitude", "reported_at"
            )
            file_path = os.path.join(settings.BASE_DIR, "location_reports.json")
            with open(file_path, "w") as f:
                json.dump(list(all_reports), f, indent=4, default=str)

            return JsonResponse({"message": "Location saved successfully"})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    return JsonResponse({"error": "Only POST method allowed"}, status=405)


def send_emergency_alert(latitude, longitude):
    subject = "🚨 EMERGENCY LOCATION REPORT"
    google_maps_link = f"https://www.google.com/maps?q={latitude},{longitude}"

    message = render_to_string(
        "emergency_email.txt",
        {
            "latitude": latitude,
            "longitude": longitude,
            "maps_link": google_maps_link,
            "time": timezone.now().strftime("%Y-%m-%d %H:%M:%S"),
        },
    )

    send_mail(
        subject,
        message,
        "adamssquare4@gmail.com",  # From email
        ["jerusalem4tech@gmail.com"],  # To email (your email)
        fail_silently=False,
    )
