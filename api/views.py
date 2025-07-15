import os
import json
import requests
from requests.auth import HTTPBasicAuth
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

@csrf_exempt
@require_http_methods(["POST"])
def search_food(request):
    try:
        # Get Client ID and Secret from environment variables
        client_id = os.environ.get("FATSECRET_CONSUMER_KEY", "").strip()
        client_secret = os.environ.get("FATSECRET_CONSUMER_SECRET", "").strip()

        if not client_id or not client_secret:
            return JsonResponse({"error": "API credentials are not configured."}, status=500)

        # Get an Access Token from FatSecret
        token_url = "https://oauth.fatsecret.com/connect/token"
        auth = HTTPBasicAuth(client_id, client_secret)
        data = {"grant_type": "client_credentials", "scope": "basic"}
        
        token_response = requests.post(token_url, auth=auth, data=data)
        
        if token_response.status_code != 200:
            return JsonResponse({
                "error": "Failed to get access token",
                "details": token_response.json()
            }, status=token_response.status_code)

        access_token = token_response.json().get("access_token")

        # Use the Access Token to call the main API
        data = json.loads(request.body)
        query = data.get("query", "")
        if not query:
            return JsonResponse({"error": "Missing query"}, status=400)

        api_url = "https://platform.fatsecret.com/rest/server.api"
        headers = {"Authorization": f"Bearer {access_token}"}
        params = {
            "method": "foods.search",
            "format": "json",
            "search_expression": query
        }

        response = requests.get(api_url, headers=headers, params=params)

        return JsonResponse(response.json(), status=response.status_code)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)