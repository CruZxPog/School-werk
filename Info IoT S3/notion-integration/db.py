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

import os
from datetime import datetime
from flask import g
import mysql.connector

def get_db():
    if "db" not in g:
        g.db = mysql.connector.connect(
            host=os.getenv("DB_HOST", "127.0.0.1"),
            port=int(os.getenv("DB_PORT", "3306")),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
        )
    return g.db

def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def init_db():
    db = mysql.connector.connect(
        host=os.getenv("DB_HOST", "127.0.0.1"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
    )
    cur = db.cursor()

    # Make sure database exists
    sql = "CREATE DATABASE IF NOT EXISTS notion_app CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
    cur.execute(sql)

    sql = "USE notion_app"
    cur.execute(sql)
    
    # Workspaces table
    sql = """
    CREATE TABLE IF NOT EXISTS workspaces (
        id INT AUTO_INCREMENT PRIMARY KEY,
        notion_workspace_id VARCHAR(255) UNIQUE,
        name VARCHAR(255),
        icon_url TEXT,
        created_at DATETIME,
        updated_at DATETIME
    )
    """
    cur.execute(sql)

    # Bots table
    sql = """
    CREATE TABLE IF NOT EXISTS bots (
        id INT AUTO_INCREMENT PRIMARY KEY,
        bot_id VARCHAR(255) UNIQUE,
        workspace_id INT,
        access_token TEXT,
        refresh_token TEXT,
        token_type VARCHAR(50),
        created_at DATETIME,
        updated_at DATETIME,
        FOREIGN KEY (workspace_id) REFERENCES workspaces(id)
    )
    """
    cur.execute(sql)

    # Users table
    sql = """
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        notion_user_id VARCHAR(255) UNIQUE,
        workspace_id INT,
        name VARCHAR(255),
        email VARCHAR(255),
        avatar_url TEXT,
        user_type VARCHAR(50),
        created_at DATETIME,
        FOREIGN KEY (workspace_id) REFERENCES workspaces(id)
    )
    """
    cur.execute(sql)

    db.commit()
    db.close()

def now_str():
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
