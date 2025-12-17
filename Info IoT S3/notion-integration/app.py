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
# chatgpt.com (04/12)
# copilot.github.com (04/12)
# https://developers.notion.com/docs/authorization (04/12)
# https://developers.notion.com/docs/authorization#step-1-navigate-the-user-to-the-integrations-authorization-url (04/12)
# https://developers.notion.com/docs/authorization#step-3-send-the-code-in-a-post-request-to-the-notion-api (04/12)


from db import get_db, close_db, init_db, now_str
from flask import Flask, redirect, request, render_template, session, url_for
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth
import requests
import os

import sentry_sdk
from flask import Flask

load_dotenv()

sentry_sdk.init(
    dsn = os.getenv("SENTRY_DSN"),
    # Add data like request headers and IP for users,
    # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
    send_default_pii=True,
)

PORT = os.getenv("PORT")
SECRET_TOKEN = os.getenv("SECRET_TOKEN") 
DATABASE_ID = os.getenv("DATABASE_ID") 
NOTION_VERSION = os.getenv("NOTION_VERSION") 
CLIENT_ID = os.getenv("CLIENT_ID") 
REDIRECT_URI = os.getenv("REDIRECT_URI")

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")
app.teardown_appcontext(close_db)

with app.app_context():
    init_db()

@app.route("/", methods=["GET"])
def index():
    return redirect(url_for("login"))

@app.route("/login", methods=["GET"])
def login():
    notion_auth_url = (
        f"https://api.notion.com/v1/oauth/authorize"
        f"?client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&response_type=code"
    )
    return render_template("login.html", notion_auth_url=notion_auth_url, dashboard_url=url_for("dashboard"), sentry_test_url=url_for("sentry_test"))

@app.route("/oauth/redirect", methods=["GET"])
def login_redirect():
    
    code = request.args.get("code")
    if not code:
        sentry_sdk.capture_message(
            "No code received in OAuth redirect",
            level="warning"
        )
        return "Fout: Geen code ontvangen", 400

    profile_data = get_token(code)
    
    save_to_db(profile_data)

    # Debug optional
    print("PROFILE DATA:", profile_data)

    owner = profile_data.get("owner", {})
    user = owner.get("user", {})
    name = user.get("name", "Onbekende gebruiker")

    session["user_logged_in"] = True

    return redirect(url_for("dashboard"))

def get_token(code):
    token_url = "https://api.notion.com/v1/oauth/token"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI
    }

    response = requests.post(
        token_url,
        auth=HTTPBasicAuth(CLIENT_ID, SECRET_TOKEN),
        json=data,
        headers=headers
    )

    if not response.ok:
        print(response.text)
        return {"owner": {"name": "Unknown"}, "error": True}

    return response.json()

def save_to_db(token_data):
    db = get_db()
    cur = db.cursor(dictionary=True)
    now = now_str()
    
    workspace_db_id = save_workspace(token_data, cur, now)
    
    save_bot(token_data, workspace_db_id, cur, now)
    
    save_user(token_data, workspace_db_id, cur, now)

    db.commit()

def save_workspace(token_data, cur, now):
    workspace_id_notion = token_data.get("workspace_id")
    workspace_name = token_data.get("workspace_name")
    workspace_icon = token_data.get("workspace_icon")

    sql = "SELECT id FROM workspaces WHERE notion_workspace_id = %s"
    val = (workspace_id_notion,)
    cur.execute(sql, val)
    existing = cur.fetchone()

    if existing:
        sql = """
            UPDATE workspaces
            SET name = %s,
                icon_url = %s,
                updated_at = %s
            WHERE id = %s
        """
        val = (workspace_name, workspace_icon, now, existing["id"])
        cur.execute(sql, val)
        workspace_db_id = existing["id"]
    else:
        sql = """
            INSERT INTO workspaces (notion_workspace_id, name, icon_url, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s)
        """
        val = (workspace_id_notion, workspace_name, workspace_icon, now, now)
        cur.execute(sql, val)
        workspace_db_id = cur.lastrowid

    return workspace_db_id

def save_bot(token_data, workspace_db_id, cur, now):
    bot_id = token_data.get("bot_id")
    access_token = token_data.get("access_token")
    refresh_token = token_data.get("refresh_token")
    token_type = token_data.get("token_type", "bearer")

    sql = "SELECT id FROM bots WHERE bot_id = %s"
    val = (bot_id,)
    cur.execute(sql, val)
    bot_existing = cur.fetchone()

    if bot_existing:
        sql = """
            UPDATE bots
            SET workspace_id = %s,
                access_token = %s,
                refresh_token = %s,
                token_type = %s,
                updated_at = %s
            WHERE id = %s
        """
        val = (
            workspace_db_id,
            access_token,
            refresh_token,
            token_type,
            now,
            bot_existing["id"],
        )
        cur.execute(sql, val)
    else:
        sql = """
            INSERT INTO bots (bot_id, workspace_id, access_token, refresh_token, token_type, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        val = (
            bot_id,
            workspace_db_id,
            access_token,
            refresh_token,
            token_type,
            now,
            now,
        )
        cur.execute(sql, val)

def save_user(token_data, workspace_db_id, cur, now):
    owner = token_data.get("owner", {})
    user = owner.get("user", {})

    notion_user_id = user.get("id")
    name = user.get("name")
    avatar_url = user.get("avatar_url")
    user_type = user.get("type")

    person = user.get("person") or {}
    email = person.get("email")

    if not notion_user_id:
        # Nothing to store
        return

    sql = "SELECT id FROM users WHERE notion_user_id = %s"
    val = (notion_user_id,)
    cur.execute(sql, val)
    existing = cur.fetchone()

    if existing:
        sql = """
            UPDATE users
            SET workspace_id = %s,
                name = %s,
                email = %s,
                avatar_url = %s,
                user_type = %s
            WHERE id = %s
        """
        val = (
            workspace_db_id,
            name,
            email,
            avatar_url,
            user_type,
            existing["id"],
        )
        cur.execute(sql, val)
    else:
        sql = """
            INSERT INTO users
                (notion_user_id, workspace_id, name, email, avatar_url, user_type, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        val = (
            notion_user_id,
            workspace_db_id,
            name,
            email,
            avatar_url,
            user_type,
            now,
        )
        cur.execute(sql, val)

@app.route("/dashboard", methods=["GET"])
def dashboard():
    
    if "user_logged_in" not in session:
        sentry_sdk.capture_message(
            "Unauthorized access to dashboard",
            level="warning"
        )
        return redirect(url_for("login"))
    
    db = get_db()
    cur = db.cursor(dictionary=True)
    sql = "SELECT * FROM workspaces"
    cur.execute(sql)
    workspaces = cur.fetchall()

    sql = "SELECT * FROM bots"
    cur.execute(sql)
    bots = cur.fetchall()

    sql = "SELECT * FROM users"
    cur.execute(sql)
    users = cur.fetchall()

    return render_template("dashboard.html",
                           workspaces=workspaces,
                           bots=bots,
                           users=users)

@app.route("/sentry-test")
def sentry_test():
    1/0  # raises an error
    return "<p>Hello, World!</p>"
app.run(host="0.0.0.0", port=5000, debug=True)