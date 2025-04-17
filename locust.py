from locust import HttpUser, task, between
import random
import string
import base64
import os

def random_email():
    return ''.join(random.choices(string.ascii_lowercase, k=8)) + "@example.com"

def random_username():
    return ''.join(random.choices(string.ascii_lowercase, k=6))

def random_password():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))

class ExamProctoringUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        self.email = random_email()
        self.username = random_username()
        self.password = random_password()
        self.user = {}  # Store logged-in user data (e.g., id, email)

        self.register()
        self.login()

    def register(self):
        response = self.client.post("/students/signup/", json={
            "email": self.email,
            "username": self.username,
            "password": self.password
        })

        if response.status_code == 201:
            print(f"[✔] Registered: {self.email}")
        elif response.status_code == 400:
            print(f"[!] Email already exists: {self.email}")
        else:
            print(f"[✖] Registration failed ({response.status_code}): {response.text}")

    def login(self):
        response = self.client.post("/students/login/", json={
            "email": self.email,
            "password": self.password
        })

        if response.status_code == 200:
            self.user = response.json()  # Store user data from response (expects 'id' and 'email')
            print(f"[✔] Logged in: {self.user}")
        else:
            print(f"[✖] Login failed: {response.status_code} | {response.text}")

    @task
    def fetch_quiz(self):
        self.client.get("/get_quiz/")

    @task
    def send_webcam_snapshot(self):
        if not self.user:
            return
        # Replace this path with a valid local image (e.g., from webcam screenshot)
        with open("test_frame.jpg", "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode("utf-8")

        # Create the data URI prefix
        data_uri = f"data:image/jpeg;base64,{encoded_string}"

        payload = {
            "image": data_uri,
            "id": random.randint(1, 100),  # Simulate different student IDs
        }

        with self.client.post("/detect/", json=payload, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Failed: {response.status_code} - {response.text}")

    @task
    def submit_score(self):
        if not self.user:
            return
        score = random.randint(5, 10)
        self.client.put("/students/update_marks/", json={
            "email": self.user["email"],
            "marks_obtained": score
        })

    @task
    def upload_video(self):
        if not self.user:
            return
        # Use a small placeholder file if you don't have a real video
        if not os.path.exists("sample_video.mp4"):
            with open("sample_video.mp4", "wb") as f:
                f.write(os.urandom(1024))  # Create a 1KB fake file

        with open("sample_video.mp4", "rb") as f:
            files = {
                "video": ("recording.mp4", f, "video/mp4")
            }
            data = {
                "email": self.user["email"]
            }
            self.client.post("/students/upload_video/", files=files, data=data)
