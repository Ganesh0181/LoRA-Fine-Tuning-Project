from dotenv import load_dotenv
import os

load_dotenv()

print("JWT:", os.getenv("JWT_SECRET"))
print("Weather:", os.getenv("OPENWEATHER_API_KEY"))
print("SMTP:", os.getenv("SMTP_EMAIL"))
print("Maps:", os.getenv("GOOGLE_MAPS_API_KEY"))