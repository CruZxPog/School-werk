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
    
def read_user_input():
    serial_number = input("Enter device serial number: ").strip()
    if not serial_number:
        print("Input error: Sensor serial number cannot be empty.")
        sys.exit(1) # Input error
    if len(serial_number) > 255:
        print("Input error: Sensor serial number exceeds 255 characters.")
        sys.exit(1) # Input error

    sensor_type = input("Enter sensor type: ").strip()
    if not sensor_type:
        print("Input error: Sensor type cannot be empty.")
        sys.exit(1) # Input error
    if len(sensor_type) > 255:
        print("Input error: Sensor type exceeds 255 characters.")
        sys.exit(1) # Input error
    
    limit_str = input("Enter how many readings to display: ").strip()
    if not limit_str.isdigit() or int(limit_str) <= 0:
        print("Input error: Reading value cannot be empty.")
        sys.exit(1) # Input error
    limit = int(limit_str)
    return serial_number, sensor_type, limit

def get_sensor_id(db_cursor, serial_number, sensor_type):
    # Check if sensor exists
        sql = """
        SELECT sensors.id 
        FROM sensors 
        JOIN devices ON sensors.device_id = devices.id 
        WHERE devices.serial_number = %s and sensors.sensor_type = %s 
        LIMIT 2;
        """
        val = (serial_number, sensor_type)
        db_cursor.execute(sql, val)
        result = db_cursor.fetchall()
        if len(result) == 0:
            print(f"Input error: No sensor found with serial number '{serial_number}' and type '{sensor_type}'.")
            sys.exit(1) # Input error
        elif len(result) > 1:
            print(f"Input error: Multiple sensors found with serial number '{serial_number}' and type '{sensor_type}'. Please specify unique identifiers.")
            sys.exit(1) # Input error
        return result[0][0]

def main():
    try:
        serial_number, sensor_type, limit = read_user_input()
        
        db_connection = get_db_connection()
        db_cursor = db_connection.cursor()
        
        sensor_id = get_sensor_id(db_cursor, serial_number, sensor_type)

        sql = """
        SELECT reading_timestamp, reading_value 
        FROM sensor_readings 
        WHERE sensor_id = %s
        ORDER BY reading_timestamp DESC
        LIMIT %s
        """

        val = (sensor_id, limit)  # Limit to 10 readings
        db_cursor.execute(sql, val)
        results = db_cursor.fetchall()
        for reading_timestamp, reading_value in results:
            format_timestamp = reading_timestamp.strftime("%Y-%m-%d %H:%M:%S")
            print(f"Timestamp: {format_timestamp} | Value: {reading_value}")
        
        db_cursor.close()
        db_connection.close()
        sys.exit(0) # Success

    except ValueError as value_error:
        print(f"Input error: {value_error}")
        sys.exit(1) # Input error
    except mysql.connector.errors.DataError as data_error:
        print(f"db data error: {data_error}")
        sys.exit(3) # Data error
    except mysql.connector.errors.IntegrityError as integrity_error:
        print(f"db integrity error: {integrity_error}")
        sys.exit(4) # Integrity error
    except Exception as unexpected_error:
        print(f"Unexpected error: {unexpected_error}")
        sys.exit(5) # Unexpected error

if __name__ == "__main__":
    main()