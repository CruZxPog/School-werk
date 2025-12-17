import requests
import uuid
import time
from typing import Optional, Dict, Any

# ==========================
# CONFIG
# ==========================

BASE_URL = "http://meowpi:1880/webhook/sensors"  # pas aan als nodig
SECRET = "2342EkP34xuSG3qnJ26@$m923jnv"  # zelfde als in je Node-RED flow

# Event-waarden die zeker de drempels triggerren
TEMP_OK = 25       # onder je alarmdrempel
TEMP_ALARM = 30    # boven je alarmdrempel
CO2_OK = 800       # onder je danger-drempel
CO2_DANGER = 1500  # boven je danger-drempel
HUMIDITY_VALUE = 55

# ==========================
# HELPER FUNCTIES
# ==========================

def print_title(title: str) -> None:
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def print_response(label: str, resp: requests.Response) -> None:
    print(f"\n[{label}] HTTP {resp.status_code}")
    try:
        data = resp.json()
        print("Response JSON:")
        for k, v in data.items():
            print(f"  {k}: {v}")
    except Exception:
        print("Raw response:")
        print(resp.text)


def send_request(
    payload: Optional[Dict[str, Any]] = None,
    secret: Optional[str] = SECRET,
    event_id: Optional[str] = None
) -> requests.Response:
    if event_id is None:
        event_id = str(uuid.uuid4())

    headers = {
        "Content-Type": "application/json"
    }

    if secret is not None:
        headers["X-Secret"] = secret

    # Alleen X-Event-Id sturen als we er eentje willen testen
    if event_id != "NO_HEADER":
        headers["X-Event-Id"] = event_id

    resp = requests.post(
        BASE_URL,
        headers=headers,
        json=payload
    )
    return resp


# ==========================
# TEST CASES
# ==========================

def test_missing_secret() -> None:
    print_title("TEST 1: Secret ontbreekt (verwacht 401)")
    payload = {"type": "temperature", "room": "lab1", "value": TEMP_OK}
    resp = send_request(payload=payload, secret=None)
    print_response("missing_secret", resp)


def test_wrong_secret() -> None:
    print_title("TEST 2: Secret fout (verwacht 401)")
    payload = {"type": "temperature", "room": "lab1", "value": TEMP_OK}
    resp = send_request(payload=payload, secret="wrong-secret")
    print_response("wrong_secret", resp)


def test_missing_event_id() -> None:
    print_title("TEST 3: Event-ID ontbreekt (verwacht 400)")
    payload = {"type": "temperature", "room": "lab1", "value": TEMP_OK}
    # Speciaal: "NO_HEADER" = we sturen geen X-Event-Id
    resp = send_request(payload=payload, event_id="NO_HEADER")
    print_response("missing_event_id", resp)


def test_temperature_ok_and_alarm() -> str:
    print_title("TEST 4: Temperature OK + Alarm (verwacht ok + alarm)")
    # OK
    payload_ok = {"type": "temperature", "room": "lab1", "value": TEMP_OK}
    resp_ok = send_request(payload=payload_ok)
    print_response("temp_ok", resp_ok)

    # Alarm
    event_id_alarm = str(uuid.uuid4())
    payload_alarm = {"type": "temperature", "room": "lab1", "value": TEMP_ALARM}
    resp_alarm = send_request(payload=payload_alarm, event_id=event_id_alarm)
    print_response("temp_alarm", resp_alarm)

    print("\nCheck Telegram + Airtable tabel 'Temperature' voor twee rijen (ok + alarm).")
    return event_id_alarm


def test_temperature_duplicate(existing_event_id: str) -> None:
    print_title("TEST 5: Temperature duplicate (verwacht status duplicate)")
    payload = {"type": "temperature", "room": "lab1", "value": TEMP_ALARM}
    resp = send_request(payload=payload, event_id=existing_event_id)
    print_response("temp_duplicate", resp)
    print("\nIn Airtable zou GEEN extra rij mogen bijkomen voor dit event_id.")


def test_co2_ok_and_danger() -> str:
    print_title("TEST 6: CO2 OK + Danger (verwacht ok + danger)")
    # OK
    payload_ok = {"type": "co2", "room": "lab2", "value": CO2_OK}
    resp_ok = send_request(payload=payload_ok)
    print_response("co2_ok", resp_ok)

    # Danger
    event_id_danger = str(uuid.uuid4())
    payload_danger = {"type": "co2", "room": "lab2", "value": CO2_DANGER}
    resp_danger = send_request(payload=payload_danger, event_id=event_id_danger)
    print_response("co2_danger", resp_danger)

    print("\nCheck Telegram + Airtable tabel 'CO2' voor ok + danger rij.")
    return event_id_danger


def test_co2_duplicate(existing_event_id: str) -> None:
    print_title("TEST 7: CO2 duplicate (verwacht status duplicate)")
    payload = {"type": "co2", "room": "lab2", "value": CO2_DANGER}
    resp = send_request(payload=payload, event_id=existing_event_id)
    print_response("co2_duplicate", resp)


def test_humidity_logged() -> None:
    print_title("TEST 8: Humidity logged only (geen alarm, wel logging)")
    payload = {"type": "humidity", "room": "lab3", "value": HUMIDITY_VALUE}
    resp = send_request(payload=payload)
    print_response("humidity_logged", resp)
    print("\nCheck Airtable tabel 'Humidity' voor een nieuwe rij.")


def test_invalid_body() -> None:
    print_title("TEST 9: Foutieve body (bijv. string ipv JSON object)")
    # Hier sturen we bv. een body zonder type/value
    payload = {"room": "lab1"}  # mist type en value
    resp = send_request(payload=payload)
    print_response("invalid_body", resp)


def test_unknown_sensor_type() -> None:
    print_title("TEST 10: Onbekend sensortype (verwacht fout)")
    payload = {"type": "noise", "room": "lab1", "value": 50}
    resp = send_request(payload=payload)
    print_response("unknown_type", resp)


def test_rate_limit_temperature() -> None:
    print_title("TEST 11: Rate limit temperature alarm (2x snel na elkaar)")
    payload_alarm = {"type": "temperature", "room": "lab1", "value": TEMP_ALARM}

    # Eerste alarm
    event_id_1 = str(uuid.uuid4())
    resp1 = send_request(payload=payload_alarm, event_id=event_id_1)
    print_response("temp_alarm_1", resp1)

    # Kort wachten (rate limit is 30s, dus dit moet nog "te snel" zijn)
    time.sleep(2)

    event_id_2 = str(uuid.uuid4())
    resp2 = send_request(payload=payload_alarm, event_id=event_id_2)
    print_response("temp_alarm_2", resp2)

    print("\nCheck in Node-RED / Telegram of je maar één alarm krijgt door de rate limit.")


def test_rate_limit_co2() -> None:
    print_title("TEST 12: Rate limit CO2 danger (2x snel na elkaar)")
    payload_danger = {"type": "co2", "room": "lab2", "value": CO2_DANGER}

    # Eerste danger
    event_id_1 = str(uuid.uuid4())
    resp1 = send_request(payload=payload_danger, event_id=event_id_1)
    print_response("co2_danger_1", resp1)

    time.sleep(2)

    # Tweede danger, ander event_id maar binnen 5 minuten
    event_id_2 = str(uuid.uuid4())
    resp2 = send_request(payload=payload_danger, event_id=event_id_2)
    print_response("co2_danger_2", resp2)

    print("\nCheck in Node-RED / Telegram of er maar één ventilatie-actie gebeurt.")


# ==========================
# MAIN
# ==========================

def run_all_tests() -> None:
    print_title("START: Alle tests voor multisensor webhook")

    test_missing_secret()
    time.sleep(1)

    test_wrong_secret()
    time.sleep(1)

    test_missing_event_id()
    time.sleep(1)

    temp_alarm_event_id = test_temperature_ok_and_alarm()
    time.sleep(1)

    test_temperature_duplicate(temp_alarm_event_id)
    time.sleep(1)

    co2_danger_event_id = test_co2_ok_and_danger()
    time.sleep(1)

    test_co2_duplicate(co2_danger_event_id)
    time.sleep(1)

    test_humidity_logged()
    time.sleep(1)

    test_invalid_body()
    time.sleep(1)

    test_unknown_sensor_type()
    time.sleep(1)

    test_rate_limit_temperature()
    time.sleep(1)

    test_rate_limit_co2()

    print_title("KLAAR: Alle tests zijn verstuurd. Check Node-RED, Airtable en Telegram.")


if __name__ == "__main__":
    run_all_tests()
