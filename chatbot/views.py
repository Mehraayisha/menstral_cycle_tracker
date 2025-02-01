from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os
# from google.cloud import aiplatform  # For Google Gemini integration
#sherin------
import requests
from django.http import HttpResponse
from django.conf import settings
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
@csrf_exempt  # Remove this in production if CSRF protection is needed
def generate_content(request):
    if request.method != 'POST':  # Only allow POST requests
        return JsonResponse({"reply": "Invalid request method."}, status=405)

    try:
        # Retrieve the Gemini API key from settings
        # api_key = settings.GEMINI_API_KEY
        
        if not GEMINI_API_KEY:
            return JsonResponse({"error": "Missing API key"}, status=500)

        # Define the endpoint for the Gemini API
        # endpoint = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
        endpoint = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=AIzaSyC4W6PgbkLkkeNlunJgFkqqYjLwYEMgmSo"

        # Extract input text from request body
        import json
        body = json.loads(request.body)
        input_text = body.get("text", "Explain how AI works")  # Default fallback text

        # Prepare the request headers and payload
        headers = {
            "Content-Type": "application/json",
        }
        data = {
            "contents": [{"parts": [{"text": input_text}]}]
        }

        # Make the POST request to Gemini API
        response = requests.post(f"{endpoint}?key={GEMINI_API_KEY}", headers=headers, json=data)

        # If the request is successful, return the generated content
        if response.status_code == 200:
            ai_response = response.json()
            text_output = ai_response["candidates"][0]["content"]["parts"][0]["text"]
            
            return JsonResponse({"reply": text_output})
            # return JsonResponse(response.json())
        else:
            return JsonResponse({"error": "Failed to generate content"}, status=response.status_code)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def example_view(request):
    # Accessing the Gemini API Key stored in settings.py
    # api_key = settings.GEMINI_API_KEY

    # Returning the API key in the response
    return HttpResponse(f"Gemini API Key: {GEMINI_API_KEY}")
#----------
# Set up Google Cloud credentials
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path_to_your_service_account_key.json"

@csrf_exempt
def chat_with_gemini(request):
    if request.method != "POST":
        return JsonResponse({"reply": "Invalid request method."}, status=405)
    try:
            # Parse the incoming request
            body = json.loads(request.body)
            user_message = body.get("message", "")

            if not user_message:
                return JsonResponse({"reply": "Please provide a message."})

            # Initialize AI Platform
            # aiplatform.init(project="your-project-id", location="us-central1")

            # Send the message to the Gemini model
            # client = aiplatform.gapic.PredictionServiceClient()
            endpoint = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=AIzaSyC4W6PgbkLkkeNlunJgFkqqYjLwYEMgmSo"
            # endpoint = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=AIzaSyCZ4uOsatH2bfkzoNmzkBiow_q6is3enFE"
            headers = {"Content-Type": "application/json"}
            data = {"contents": [{"parts": [{"text": user_message}]}]}

            response = requests.post(f"{endpoint}?key={GEMINI_API_KEY}", headers=headers, json=data)
            if response.status_code == 200:
                ai_response = response.json()
                ai_reply = ai_response["candidates"][0]["content"]["parts"][0]["text"]
                return JsonResponse({"reply": ai_reply})

            return JsonResponse({"error": "Failed to process request"}, status=response.status_code)
    except Exception as e:
            return JsonResponse({"reply": f"Error: {str(e)}"}, status=500)
    
            # response = client.predict(
            #     endpoint=endpoint,
            #     instances=[{"content": user_message}],
            #     parameters={"temperature": 0.7},  # Adjust as needed
            # )
            # ai_reply = response.predictions[0].get("content", "I couldn't process that.")
            # return JsonResponse({"reply": ai_reply})

    #     except Exception as e:
    #         return JsonResponse({"reply": f"Error: {str(e)}"})

    # return JsonResponse({"reply": "Invalid request method."})

