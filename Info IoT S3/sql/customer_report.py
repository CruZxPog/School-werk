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
# https://www.w3schools.com/SQL/func_sqlserver_coalesce.asp (26/10)
# https://www.geeksforgeeks.org/sql/sql-subquery/ (26/10)
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
        database_connection = get_db_connection()
        database_cursor = database_connection.cursor()
        
        # I used ChatGPT to help design and explain this SQL query.
        # It calculates, for each customer, how many devices and sensors they have by
        # combining aggregated subqueries from the devices and sensors tables.
        # The query uses LEFT JOINs so customers with zero devices or sensors still appear.
        # https://www.w3schools.com/SQL/func_sqlserver_coalesce.asp (26/10)
        # https://www.geeksforgeeks.org/sql/sql-subquery/ (26/10)
        # https://www.w3schools.com/sql/sql_join_left.asp (26/10)
        
        sql = """
        SELECT
          customers.id,
          cCONCAT(ustomers.first_name, ' ', customers.last_name) AS customer_name,
          COALESCE(devices_counts.device_count, 0) AS device_count,
          COALESCE(sensor_counts.sensor_count, 0) AS sensor_count
        FROM customers
        LEFT JOIN (
          SELECT customer_id, COUNT(*) AS device_count
          FROM devices
          GROUP BY customer_id
        ) AS devices_counts
          ON devices_counts.customer_id = customers.id
        LEFT JOIN (
          SELECT devices.customer_id, COUNT(sensors.id) AS sensor_count
          FROM sensors
          JOIN devices ON sensors.device_id = devices.id
          GROUP BY devices.customer_id
        ) AS sensor_counts
          ON sensor_counts.customer_id = customers.id
        ORDER BY customer_name
        """

        val = ()
        database_cursor.execute(sql, val)
        rows = database_cursor.fetchall()

        if not rows:
            print("No customers found.")
            database_cursor.close()
            database_connection.close()
            sys.exit(0) # Success

        print(f"{'ID':<5} {'Customer':<25} {'Devices':<10} {'Sensors'}")
        print("-" * 55)
        for customer_id, customer_name, device_count, sensor_count in rows:
            print(f"{customer_id:<5} {customer_name:<25} {device_count:<10} {sensor_count}")

        database_cursor.close()
        database_connection.close()
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