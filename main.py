import requests
import os
from datetime import datetime

APP_ID = os.environ["NUTRITIONIX_APP_ID"]
API_KEY = os.environ["NUTRITIONIX_API_KEY"]

GENDER = "male"
WEIGHT_KG = 88.5
HEIGHT_CM = 182.9
AGE = 30

nutritionix_exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
user_input = input("Tell me what exercises you did: ")

sheet_endpoint = os.environ["SHEET_ENDPOINT"]

nutritionix_headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}

nutritionix_parameters = {
    "query": user_input,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}

response = requests.post(url=nutritionix_exercise_endpoint, json=nutritionix_parameters, headers=nutritionix_headers)
result = response.json()
print(result)

# Write the exercises to google sheets
today = datetime.now().strftime("%d-%m-%Y")
right_now = datetime.now().strftime("%X")
sheety_bearer_token = os.environ["SHEETY_BEARER_TOKEN"]
sheety_auth = {
    "Authorization": f"Bearer {sheety_bearer_token}"
}

for item in result['exercises']:
    sheets_input = {
        "workout": {
            "date": today,
            "time": right_now,
            "exercise": item["name"].title(),
            "duration": item["duration_min"],
            "calories": item["nf_calories"],
        }
    }
    sheets_response = requests.post(url=sheet_endpoint, json=sheets_input, headers=sheety_auth)
    print(sheets_response)
