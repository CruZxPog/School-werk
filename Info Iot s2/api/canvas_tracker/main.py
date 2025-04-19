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
from tabulate import tabulate
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

def get_user_data():
    response = requests.get(
        f"{BASE_URL}/users/{USER_ID}", headers=headers
    )
    if response.status_code != 200:
        print("Fout bij ophalen van gebruikersdata:", response.text)
        exit()
    user_data = response.json()
    print(user_data)

def get_courses():
    response = requests.get(
        f"{BASE_URL}/courses", headers=headers
    )
    if response.status_code != 200:
        print("Fout bij ophalen van gebruikersdata:", response.text)
        exit()
    courses = response.json()

    for course in courses:
        print(f"ID: {course.get('id','N/A')} => {course.get('name','N/A')} ")


def get_assignments(course_id):
    response = requests.get(
        f"{BASE_URL}/courses/{course_id}/assignments", headers=headers
    )
    if response.status_code != 200:
        print("Fout bij ophalen van gebruikersdata:", response.text)
        exit()

    assignments = response.json()

    if not assignments:
        print(f"No assignments found for course {course_id}.")
        exit()
    assignments_data = []
    for assignment in assignments:
        assignment_name = assignment.get('name')
        grade, submitted_at, workflow_state, graded_at, points, points_words, average_points = get_submission_details(course_id, assignment.get('id'))
        points_str = ", ".join(map(str, points)) if points else "N/A"
        points_words_str = ", ".join(points_words) if points_words else "N/A"
        assignments_data.append([
            assignment_name,
            grade,
            submitted_at,
            workflow_state,
            graded_at,
            points_str,
            points_words_str,
            average_points
        ])
    header = ["Assignment Name", "Grade", "Submitted At", "Workflow State", "Graded At", "Points", "Points Words", "Average Points"]
    assignments_data.sort(key=lambda x: (x[7] is None, x[7]))
    print(tabulate(assignments_data, headers=header, tablefmt="fancy_grid"))

def get_submission_details(course_id, assignment_id):
    response = requests.get(
        f"{BASE_URL}/courses/{course_id}/assignments/{assignment_id}/submissions/{USER_ID}?include[]=rubric_assessment", headers=headers
    )
    if response.status_code != 200:
        print("Fout bij ophalen van gebruikersdata:", response.text)
        exit()

    submission = response.json()


    if not submission:
        print(f"No submission found for assignment {assignment_id}.")
        exit()

    rubric_assessment = submission.get('rubric_assessment',{})
    points = list(map(lambda item: item[1].get('points', None), rubric_assessment.items()))
    points_mapping = {
        9.0: "Uitstekend",
        6.0: "Goed",
        4.0: "Bijna goed",
        0.1: "Nog niet goed",
        0.0: "Niet ingediend"
    }
    points_words = [points_mapping.get(point, "Unknown") for point in points]
    average_points = sum(points) / len(points) if points else 0
    grade = submission.get('grade', None)
    submitted_at = submission.get('submitted_at', None)
    workflow_state = submission.get('workflow_state', None)
    graded_at = submission.get('graded_at', None)

    return grade,submitted_at,workflow_state,graded_at,points,points_words, average_points

def main():
    get_user_data()
    get_courses()   
    course_id = input("Enter course ID: ")
    get_assignments(course_id)

if __name__ == "__main__":
    main()