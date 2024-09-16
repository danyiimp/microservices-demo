import os


NOTIFICATION_URL = os.getenv(
    "NOTIFICATION_URL", "http://localhost:9000/reservation"
)
