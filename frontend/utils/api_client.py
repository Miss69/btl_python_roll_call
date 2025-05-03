import requests
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000/face_recognition"

def check_in(employee_id: int):
    payload = {
        "id_employee": employee_id,
        "check_in": datetime.now().strftime("%H:%M:%S"),
        "date": datetime.now().strftime("%Y-%m-%d")
    }
    response = requests.post(f"{BASE_URL}/checkin", json=payload)
    response.raise_for_status()  # Raise lỗi nếu có
    return response.json()

def check_out(employee_id: int):
    payload = {
        "id_employee": employee_id,
        "check_out": datetime.now().strftime("%H:%M:%S"),
        "date": datetime.now().strftime("%Y-%m-%d")
    }
    response = requests.post(f"{BASE_URL}/checkout", json=payload)
    response.raise_for_status()
    return response.json()

def get_attendance_history(employee_id: int):
    response = requests.get(f"{BASE_URL}/attendance", params={"id_employee": employee_id})
    response.raise_for_status()
    return response.json()
