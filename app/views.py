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
    return render(request, 'home.html')


# 2. Report location view
@csrf_exempt
def report_location(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            lat = data.get('latitude')
            lng = data.get('longitude')

            if lat is None or lng is None:
                return JsonResponse({'error': 'Missing latitude or longitude'}, status=400)

            # Save to database
            report = DisasterReport.objects.create(
                latitude=lat,
                longitude=lng,
                reported_at=timezone.now()
            )

            # Optional: Save all to a JSON file
            all_reports = DisasterReport.objects.values('latitude', 'longitude', 'reported_at')
            file_path = os.path.join(settings.BASE_DIR, 'location_reports.json')
            with open(file_path, 'w') as f:
                json.dump(list(all_reports), f, indent=4, default=str)

            return JsonResponse({'message': 'Location saved successfully'})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

    return JsonResponse({'error': 'Only POST method allowed'}, status=405)
