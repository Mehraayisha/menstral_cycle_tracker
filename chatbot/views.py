from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os
from google.cloud import aiplatform  # For Google Gemini integration

# Set up Google Cloud credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path_to_your_service_account_key.json"

@csrf_exempt
def chat_with_gemini(request):
    if request.method == "POST":
        try:
            # Parse the incoming request
            body = json.loads(request.body)
            user_message = body.get("message", "")

            if not user_message:
                return JsonResponse({"reply": "Please provide a message."})

            # Initialize AI Platform
            aiplatform.init(project="your-project-id", location="us-central1")

            # Send the message to the Gemini model
            client = aiplatform.gapic.PredictionServiceClient()
            endpoint = "projects/YOUR_PROJECT_ID/locations/us-central1/endpoints/YOUR_ENDPOINT_ID"

            response = client.predict(
                endpoint=endpoint,
                instances=[{"content": user_message}],
                parameters={"temperature": 0.7},  # Adjust as needed
            )

            # Extract AI response
            ai_reply = response.predictions[0].get("content", "I couldn't process that.")
            return JsonResponse({"reply": ai_reply})

        except Exception as e:
            return JsonResponse({"reply": f"Error: {str(e)}"})

    return JsonResponse({"reply": "Invalid request method."})

