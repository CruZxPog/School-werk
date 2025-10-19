from coapthon.client.helperclient import HelperClient
from dotenv import load_dotenv
import os, random, time, json

load_dotenv()
# HOST = os.getenv("IP")
# PORT = os.getenv("COAP_PORT")
HOST = "192.168.0.106"   # vervang door je Pi IP
PORT = 5683
client = HelperClient(server=(HOST, PORT))

def rnd(a, b, d=1):
    val = random.uniform(a, b)
    return round(val, d)

try:
    while True:
        # # 1) Bodemvocht 0-100%
        bodem = {"bodemvocht": int(rnd(15, 85, 0))}
        client.put("/sensor/bodemvocht", json.dumps(bodem))
        print("PUT /sensor/bodemvocht", bodem)
        # time.sleep(2)
        # 2) Omgevingslicht 0-100000 lux
        # Maak het geloofwaardig met daglichtfluctuatie
        licht = {"omgevingslicht": int(rnd(200, 80000, 0))}
        client.put("/sensor/omgevingslicht", json.dumps(licht))
        print("PUT /sensor/omgevingslicht", licht)
        # time.sleep(2)
        # 3) Temperatuur + luchtvochtigheid samen
        tempvocht = {
            "temperature": rnd(8, 34, 1),
            "luchtvochtigheid": int(rnd(35, 95, 0))
        }
        client.put("/sensor/tempVocht", json.dumps(tempvocht))
        print("PUT /sensor/tempVocht", tempvocht)
        time.sleep(5)
except KeyboardInterrupt:
    print("\nStopped.")

    
