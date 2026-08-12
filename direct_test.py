import requests

login = requests.post("http://127.0.0.1:8000/api/v1/auth/login", json={
    "email": "shop@altprint.in",
    "password": "Shop1234!"
})
print("Login status:", login.status_code)
token = login.json().get("access_token")
print("Got token:", bool(token))

headers = {"Authorization": f"Bearer {token}"}
ticket = requests.post("http://127.0.0.1:8000/api/v1/tickets", json={
    "subject": "DirectTest001",
    "description": "testing directly via script",
    "priority": "normal"
}, headers=headers)
print("Ticket status:", ticket.status_code)
print("Ticket response:", ticket.json())
