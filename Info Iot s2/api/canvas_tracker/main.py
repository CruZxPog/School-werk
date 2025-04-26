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
# https://canvasapi.readthedocs.io/en/stable/index.html (19/04)

from dotenv import load_dotenv
import os
import requests
from flask import Flask
from flask import render_template

load_dotenv()
ACCESS_TOKEN = os.getenv("CANVAS_API_KEY")
USER_ID = os.getenv("CANVAS_USER_ID")
BASE_URL = "https://canvas.kdg.be/api/v1/"

if not ACCESS_TOKEN or not USER_ID:
    print("Error: Canvas API key or user ID not found in environment variables.")
    exit()

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}

app = Flask(__name__)

@app.route("/")
def home_page():
    courses = get_courses()
    all_data = []

    for course in courses:
        course_id = course.get('id')
        course_name = course.get('name')
        assignments = []

        response = requests.get(
            f"{BASE_URL}/courses/{course_id}/assignments", headers=headers
        )
        if response.status_code != 200:
            continue

        for assignment in response.json():
            assignment_name = assignment.get('name')
            grade, submitted_at, workflow_state, graded_at, points, points_words, average_points = get_submission_details(course_id, assignment.get('id'))

            beoordeling = min(points_words, default="Geen beoordeling")
            score_class = beoordeling_to_class(beoordeling)

            assignments.append({
                "name": assignment_name,
                "grade": grade,
                "submitted_at": submitted_at,
                "workflow_state": workflow_state,
                "graded_at": graded_at,
                "points": points,
                "points_words": points_words,
                "average_points": average_points,
                "beoordeling": beoordeling,
                "score_class": score_class,
                "html_url" : assignment.get('html_url')
            })

        # Sorteer de opdrachten op beoordelingsvolgorde
        beoordeling_order = [
            "Niet ingediend",
            "Nog niet goed",
            "Bijna goed",
            "Goed",
            "Uitstekend",
            None
        ]
        def sort_key(assignment):
            beoordeling = assignment["beoordeling"]
            if beoordeling in beoordeling_order:
                return beoordeling_order.index(beoordeling)
            return len(beoordeling_order)

        assignments.sort(key=sort_key)

        # Zoek de slechtste beoordeling voor deze cursus (behalve "Niet ingediend")
        beoordeling_values = []
        for a in assignments:
            beoordeling = a["beoordeling"]
            if beoordeling != "Niet ingediend":
                beoordeling_values.append(beoordeling)
        
        def beoordeling_sort_key(value):
            if value in beoordeling_order:
                return beoordeling_order.index(value)
            return len(beoordeling_order)

        worst_beoordeling = min(beoordeling_values, default=None, key=beoordeling_sort_key)
        course_class = beoordeling_to_class(worst_beoordeling)

        all_data.append({
            "course_name": course_name,
            "course_id": course_id,
            "assignments": assignments,
            "course_class": course_class
        })

    return render_template("index.html", title="Canvas Dashboard", courses=all_data)


def get_user_data():
    response = requests.get(
        f"{BASE_URL}/users/{USER_ID}", headers=headers
    )
    if response.status_code != 200:
        print("Fout bij ophalen van gebruikersdata:", response.text)
        exit()
    return response.json()


def get_courses():
    response = requests.get(
        f"{BASE_URL}/courses", headers=headers
    )
    if response.status_code != 200:
        print("Fout bij ophalen van cursusdata:", response.text)
        exit()
    return response.json()


def get_submission_details(course_id, assignment_id):
    response = requests.get(
        f"{BASE_URL}/courses/{course_id}/assignments/{assignment_id}/submissions/{USER_ID}?include[]=rubric_assessment", headers=headers
    )
    if response.status_code != 200:
        return (None, None, None, None, [], [], 0)

    submission = response.json()

    rubric_assessment = submission.get('rubric_assessment', {})
    points = [item.get('points', None) for item in rubric_assessment.values()]
    points_mapping = {
        9.0: "Uitstekend",
        6.0: "Goed",
        4.0: "Bijna goed",
        0.1: "Nog niet goed",
        0.0: "Niet ingediend"
    }
    points_words = [points_mapping.get(point, "Onbekend") for point in points]
    average_points = sum(points) / len(points) if points else 0
    grade = submission.get('grade', None)
    submitted_at = submission.get('submitted_at', None)
    workflow_state = submission.get('workflow_state', None)
    graded_at = submission.get('graded_at', None)

    return grade, submitted_at, workflow_state, graded_at, points, points_words, average_points

def beoordeling_to_class(beoordeling):
    mapping = {
        "Uitstekend": "score-uitstekend",
        "Goed": "score-goed",
        "Bijna goed": "score-bijna-goed",
        "Nog niet goed": "score-niet-goed",
        "Niet ingediend": "score-niet-ingediend",
        "Geen beoordeling": "score-geen"
    }
    return mapping.get(beoordeling, "score-geen")
