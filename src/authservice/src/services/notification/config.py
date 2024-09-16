import os


VERIFICATION_TOKEN_URL = os.getenv(
    "VERIFICATION_TOKEN_URL", "http://localhost:9000/verification-token"
)

RESET_TOKEN_URL = os.getenv(
    "RESET_TOKEN_URL", "http://localhost:9000/reset-token"
)
