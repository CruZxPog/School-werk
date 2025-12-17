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
# chatgpt.com (26/10)
# copilot.github.com (26/10)
# https://www.w3schools.com/sql/sql_having.asp (26/10)
# https://www.w3schools.com/sql/sql_join_left.asp (26/10)
import mysql.connector
from dotenv import load_dotenv
import sys
import os

load_dotenv()

def get_db_connection():
    try:
        db_connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            port=int(os.getenv("DB_PORT")),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
        )
        return db_connection
    except Exception as error:
        print(f"database connection failed: {error}")
        sys.exit(2) # Connection error

def main():
    try:
        db_connection = get_db_connection()
        db_cursor = db_connection.cursor()

        # Check for sensors without readings in the last 30 days
        # used chatgpt to help write this query because of left join and date functions
        # https://www.w3schools.com/sql/sql_having.asp (26/10)
        # https://www.w3schools.com/sql/sql_join_left.asp (26/10)
        
        sql = """
        SELECT
            devices.id,
            devices.device_type,
            devices.serial_number,
        MAX(maintenance_logs.log_date)
        FROM devices
        LEFT JOIN maintenance_logs
            ON maintenance_logs.device_id = devices.id
        GROUP BY devices.id, devices.device_type, devices.serial_number
        HAVING MAX(maintenance_logs.log_date) IS NULL
            OR MAX(maintenance_logs.log_date) < DATE_SUB(CURDATE(), INTERVAL 6 MONTH)
        ORDER BY maintenance_logs.log_date IS NULL DESC, maintenance_logs.log_date ASC
        """

        val = ()
        db_cursor.execute(sql, val)
        rows = db_cursor.fetchall()

        if not rows:
            print("All devices have recent maintenance logs within the last 6 months.")
            db_cursor.close()
            db_connection.close()
            sys.exit(0) # Success
        
        print(f"{'ID':<5} {'Type':<18} {'Serial':<16} {'Last maintenance'}")
        print("-" * 60)
        for device_id, device_type, serial_number, last_maintenance in rows:
            last_str = last_maintenance.strftime("%Y-%m-%d") if last_maintenance else "never"
            print(f"{device_id:<5} {device_type:<18} {serial_number:<16} {last_str}")

        db_cursor.close()
        db_connection.close()
        sys.exit(0) # Success

    except mysql.connector.errors.DataError as data_error:
        print(f"db data error: {data_error}")
        sys.exit(3)
    except mysql.connector.errors.IntegrityError as integrity_error:
        print(f"db integrity error: {integrity_error}")
        sys.exit(4)
    except Exception as unexpected_error:
        print(f"Unexpected error: {unexpected_error}")
        sys.exit(5)

if __name__ == "__main__":
    main()