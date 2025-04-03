#		     █████████                  █████                    
#			 ███░░░░░███                ░░███                    
#			░███    ░███  ████████    ███████  ████████   ██████ 
#			░███████████ ░░███░░███  ███░░███ ░░███░░███ ███░░███
#			░███░░░░░███  ░███ ░███ ░███ ░███  ░███ ░░░ ░███████ 
#			░███    ░███  ░███ ░███ ░███ ░███  ░███     ░███░░░  
#			█████   █████ ████ █████░░████████ █████    ░░██████ 
#			░░░░░   ░░░░░ ░░░░ ░░░░░  ░░░░░░░░ ░░░░░      ░░░░░░ 

# Vergeet de bronnen niet toe te voegen!
# Bronnen:
# chatgpt.com (03/04)
# copilot.github.com (03/04)
# https://canvas.instructure.com/doc/api/ (03/04)


from dotenv import load_dotenv
import os
import requests

load_dotenv()
ACCESS_TOKEN = os.getenv("CANVAS_API_KEY")
USER_ID = os.getenv("CANVAS_USER_ID")
BASE_URL = "https://canvas.kdg.be/api/v1/"

hearders = {
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}

response = requests.get(
    f"{BASE_URL}/users/{USER_ID}", headers=hearders
)
user_data = response.json()
print(user_data)

response = requests.get(
    f"{BASE_URL}/courses", headers=hearders
)
courses = response.json()
for course in courses:
    print(f"{course['name']}, ID: {course['id']}")

course_id = input("Enter course ID: ")
response = requests.get(
    f"{BASE_URL}/courses/{course_id}/assignments", headers=hearders
)
assignments = response.json()
for assignment in assignments:
    print(f"{assignment['name']}, ID: {assignment['id']}")
