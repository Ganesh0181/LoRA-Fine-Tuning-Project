import re
import os
import random
import smtplib
import requests
from email.message import EmailMessage
from dotenv import load_dotenv
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

load_dotenv()

BASE_MODEL = "sshleifer/tiny-gpt2"

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
ADAPTER_PATH = os.path.join(PROJECT_ROOT, "outputs", "dpo_lora_final")

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")
SMTP_EMAIL = os.getenv("SMTP_EMAIL", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "").replace(" ", "")
ORS_API_KEY = os.getenv("ORS_API_KEY", "")

print("ORS_API_KEY =", ORS_API_KEY[:20] if ORS_API_KEY else "NOT FOUND")

tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)
base_model = AutoModelForCausalLM.from_pretrained(BASE_MODEL)

model = PeftModel.from_pretrained(
    base_model,
    ADAPTER_PATH,
    local_files_only=True
)

model.eval()


def clean(text):
    if not text:
        return ""
    return str(text).strip().rstrip(".").rstrip(",")


def confidence_score(tool_name):
    return {
        "book_cab": 0.95,
        "order_food": 0.94,
        "set_reminder": 0.93,
        "book_hotel": 0.92,
        "weather": 0.96,
        "send_email": 0.91,
        "unknown": 0.30
    }.get(tool_name, 0.50)


def weather_tool(city):
    city = clean(city)

    if not city:
        return {"status": "failed", "message": "City is missing"}

    if not OPENWEATHER_API_KEY:
        return {"status": "failed", "message": "OPENWEATHER_API_KEY missing"}

    try:
        response = requests.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params={
                "q": city,
                "appid": OPENWEATHER_API_KEY,
                "units": "metric"
            },
            timeout=10
        )

        data = response.json()

        if response.status_code != 200:
            return {
                "status": "failed",
                "message": data.get("message", "Weather API failed"),
                "city": city
            }

        return {
            "status": "success",
            "source": "OpenWeather API",
            "city": city,
            "temperature": f"{data['main']['temp']}°C",
            "humidity": f"{data['main']['humidity']}%",
            "condition": data["weather"][0]["description"]
        }

    except Exception as e:
        return {"status": "failed", "message": str(e)}


def geocode(city):
    city = clean(city)

    url = "https://api.openrouteservice.org/geocode/search"

    response = requests.get(
        url,
        params={
            "api_key": ORS_API_KEY,
            "text": city,
            "boundary.country": "IN",
            "size": 1
        },
        timeout=10
    )

    data = response.json()

    print("\n===== GEOCODE RESPONSE =====")
    print(data)

    if response.status_code != 200:
        raise Exception(data.get("error", {}).get("message", "ORS geocode failed"))

    if "features" not in data or len(data["features"]) == 0:
        raise Exception(f"No location found for {city}")

    return data["features"][0]["geometry"]["coordinates"]


def cab_tool(pickup, drop):
    pickup = clean(pickup)
    drop = clean(drop)

    if not pickup or not drop:
        return {
            "status": "failed",
            "message": "Pickup or drop location missing"
        }

    if not ORS_API_KEY:
        return {
            "status": "failed",
            "message": "ORS_API_KEY missing in .env"
        }

    try:
        start = geocode(pickup)
        end = geocode(drop)

        route_response = requests.post(
            "https://api.openrouteservice.org/v2/directions/driving-car",
            headers={
                "Authorization": ORS_API_KEY,
                "Content-Type": "application/json"
            },
            json={
                "coordinates": [
                    start,
                    end
                ]
            },
            timeout=15
        )

        route_data = route_response.json()

        print("\n===== ROUTE RESPONSE =====")
        print(route_data)

        if route_response.status_code != 200:
            return {
                "status": "failed",
                "source": "OpenRouteService",
                "message": route_data.get("error", {}).get("message", "ORS route failed")
            }

        summary = route_data["routes"][0]["summary"]

        distance_km = round(summary["distance"] / 1000, 1)
        duration_min = round(summary["duration"] / 60)
        estimated_fare = round(80 + distance_km * 12)

        return {
            "status": "success",
            "source": "OpenRouteService",
            "pickup": pickup,
            "drop": drop,
            "distance_km": distance_km,
            "duration_min": duration_min,
            "estimated_fare": f"₹{estimated_fare}",
            "eta": f"{duration_min} min"
        }

    except Exception as e:
        return {
            "status": "failed",
            "source": "OpenRouteService",
            "message": str(e)
        }


def food_tool(item, restaurant):
    item = clean(item) or "food item"
    restaurant = clean(restaurant) or random.choice(["Paradise", "Dominos", "KFC", "Mehfil"])

    return {
        "status": "success",
        "source": "Swiggy/Zomato Mock API",
        "message": "Food order prepared",
        "item": item,
        "restaurant": restaurant,
        "estimated_price": f"₹{random.randint(120, 450)}",
        "delivery_time": f"{random.randint(20, 45)} min",
        "order_id": f"FOOD-{random.randint(10000, 99999)}"
    }


def reminder_tool(task, time_value):
    return {
        "status": "success",
        "message": "Reminder created",
        "task": clean(task),
        "time": clean(time_value),
        "reminder_id": f"REM-{random.randint(1000, 9999)}"
    }


def hotel_tool(city, date):
    return {
        "status": "success",
        "source": "Booking.com Mock API",
        "message": "Hotel search completed",
        "city": clean(city) or "Unknown City",
        "date": clean(date) or "Not specified",
        "hotel_name": random.choice(["Taj Stay", "OYO Premium", "Novotel", "ITC Grand", "Marriott"]),
        "rating": round(random.uniform(3.8, 4.9), 1),
        "price_per_night": f"₹{random.randint(1800, 6500)}",
        "booking_id": f"HOTEL-{random.randint(10000, 99999)}"
    }


def email_tool(to, subject, body):
    to = clean(to)
    subject = clean(subject) or "AI Tool Orchestrator Update"
    body = clean(body) or "This email was generated by AI Tool Orchestrator."

    if not to:
        return {"status": "failed", "message": "Receiver email missing"}

    if not SMTP_EMAIL or not SMTP_PASSWORD:
        return {
            "status": "draft_created",
            "message": "SMTP not configured. Email draft prepared only.",
            "to": to,
            "subject": subject,
            "body": body
        }

    try:
        msg = EmailMessage()
        msg["From"] = SMTP_EMAIL
        msg["To"] = to
        msg["Subject"] = subject
        msg.set_content(body)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(SMTP_EMAIL, SMTP_PASSWORD)
            smtp.send_message(msg)

        return {
            "status": "success",
            "source": "Gmail SMTP",
            "message": "Email sent successfully",
            "to": to,
            "subject": subject,
            "body": body
        }

    except Exception as e:
        return {
            "status": "failed",
            "message": str(e),
            "to": to,
            "subject": subject,
            "body": body
        }


def extract_cab(text):
    match = re.search(
        r"from\s+(.+?)\s+to\s+(.+?)(?:\s+and\s+|\s+then\s+|$)",
        text,
        re.I
    )

    return {
        "tool_name": "book_cab",
        "confidence": confidence_score("book_cab"),
        "arguments": {
            "pickup": clean(match.group(1)) if match else "",
            "drop": clean(match.group(2)) if match else ""
        }
    }


def extract_food(text):
    match = re.search(
        r"(order|get me|i want to eat|eat)\s+(.+?)\s+from\s+(.+?)(?:\s+and\s+|\s+then\s+|$)",
        text,
        re.I
    )

    return {
        "tool_name": "order_food",
        "confidence": confidence_score("order_food"),
        "arguments": {
            "item": clean(match.group(2)) if match else "",
            "restaurant": clean(match.group(3)) if match else ""
        }
    }


def extract_reminder(text):
    match = re.search(
        r"(remind me to|set reminder for|create reminder to)\s+(.+?)\s+at\s+(.+?)(?:\s+and\s+|\s+then\s+|$)",
        text,
        re.I
    )

    return {
        "tool_name": "set_reminder",
        "confidence": confidence_score("set_reminder"),
        "arguments": {
            "task": clean(match.group(2)) if match else "",
            "time": clean(match.group(3)) if match else ""
        }
    }


def extract_hotel(text):
    city_match = re.search(
        r"(hotel|room)\s+(in|at)\s+(.+?)(?:\s+for|\s+on|\s+and\s+|\s+then\s+|$)",
        text,
        re.I
    )

    date_match = re.search(
        r"(for|on)\s+(.+?)(?:\s+and\s+|\s+then\s+|$)",
        text,
        re.I
    )

    return {
        "tool_name": "book_hotel",
        "confidence": confidence_score("book_hotel"),
        "arguments": {
            "city": clean(city_match.group(3)) if city_match else "",
            "date": clean(date_match.group(2)) if date_match else ""
        }
    }


def extract_weather(text):
    match = re.search(
        r"(weather|temperature)\s+(in|at|for)\s+(.+?)(?:\s+and\s+send|\s+and\s+email|\s+then\s+send|\s+then\s+email|\s+and\s+|\s+then\s+|$)",
        text,
        re.I
    )

    return {
        "tool_name": "weather",
        "confidence": confidence_score("weather"),
        "arguments": {
            "city": clean(match.group(3)) if match else ""
        }
    }


def extract_email(text):
    to_match = re.search(
        r"to\s+([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,})",
        text,
        re.I
    )

    subject_match = re.search(
        r"subject\s+(.+?)(?:\s+message|\s+body|$)",
        text,
        re.I
    )

    body_match = re.search(
        r"(message|body)\s+(.+)$",
        text,
        re.I
    )

    return {
        "tool_name": "send_email",
        "confidence": confidence_score("send_email"),
        "arguments": {
            "to": clean(to_match.group(1)) if to_match else "",
            "subject": clean(subject_match.group(1)) if subject_match else "",
            "body": clean(body_match.group(2)) if body_match else ""
        }
    }


def execute_tool(tool_call):
    tool_name = tool_call["tool_name"]
    args = tool_call["arguments"]

    if tool_name == "book_cab":
        return cab_tool(args.get("pickup", ""), args.get("drop", ""))

    if tool_name == "order_food":
        return food_tool(args.get("item", ""), args.get("restaurant", ""))

    if tool_name == "set_reminder":
        return reminder_tool(args.get("task", ""), args.get("time", ""))

    if tool_name == "book_hotel":
        return hotel_tool(args.get("city", ""), args.get("date", ""))

    if tool_name == "weather":
        return weather_tool(args.get("city", ""))

    if tool_name == "send_email":
        return email_tool(
            args.get("to", ""),
            args.get("subject", ""),
            args.get("body", "")
        )

    return {"status": "failed", "message": "Unknown tool"}


def detect_tools(text):
    lower = text.lower()
    tools = []

    if "weather" in lower or "temperature" in lower:
        tools.append(extract_weather(text))

    if "cab" in lower or "taxi" in lower or "ride" in lower:
        tools.append(extract_cab(text))

    if (
        "order" in lower
        or "food" in lower
        or "biryani" in lower
        or "pizza" in lower
        or "burger" in lower
        or "restaurant" in lower
        or "get me" in lower
        or re.search(r"\beat\b", lower)
    ):
        tools.append(extract_food(text))

    if "remind" in lower or "reminder" in lower:
        tools.append(extract_reminder(text))

    if "hotel" in lower or "room" in lower:
        tools.append(extract_hotel(text))

    if "email" in lower or "mail" in lower or re.search(r"\bsend\s+email\b", lower):
        tools.append(extract_email(text))

    if not tools:
        tools.append({
            "tool_name": "unknown",
            "confidence": confidence_score("unknown"),
            "arguments": {}
        })

    return tools


def predict_tool_call(text):
    tool_calls = detect_tools(text)
    results = []
    seen_tools = set()

    for tool_call in tool_calls:
        tool_name = tool_call.get("tool_name", "unknown")

        if tool_name in seen_tools and tool_name != "unknown":
            continue

        seen_tools.add(tool_name)

        results.append({
            "tool_call": tool_call,
            "tool_result": execute_tool(tool_call)
        })

    if len(results) == 1:
        return results[0]

    return {
        "multi_tool": True,
        "tool_calls": results
    }