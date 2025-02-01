from django.shortcuts import render
import requests
from django.http import JsonResponse
from django.conf import settings

def get_nearby_doctors(request):
    # Fetch latitude and longitude from GET parameters
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')

    # Check if lat and lon are provided
    if not lat or not lon:
        return JsonResponse({"error": "Location not provided"}, status=400)

    # API key from settings
    google_places_api_key = settings.GOOGLE_PLACES_API_KEY

    # Google Places API URL
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lon}&radius=5000&type=doctor&keyword=gynecologist&key={google_places_api_key}"
    
    # Make the request to Google Places API
    response = requests.get(url)
    data = response.json()

    # Check if the API response contains results
    if "results" in data:
        doctors = []

        for place in data["results"]:
            # Collect doctor details
            doctor = {
                "name": place.get("name", "No name available"),
                "address": place.get("vicinity", "No address available"),
                "phone": place.get("formatted_phone_number", "N/A"),
                "website": place.get("website", "#"),
            }
            doctors.append(doctor)

        # Render the doctors page and pass the doctor data as context
        return JsonResponse({'doctors': doctors})
    # Return an error if no results were found
    return render(request, 'doctors.html',{'error':"no doctors found nearby"})
