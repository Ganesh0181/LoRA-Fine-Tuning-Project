# 🚀 AI Tool Orchestrator

Enterprise-grade AI Tool Calling Platform powered by LoRA Fine-Tuned Models, FastAPI, Streamlit, JWT Authentication, and Real-World APIs.

---

## 📌 Project Overview

AI Tool Orchestrator is a production-style AI system that intelligently routes user requests to the appropriate tool, executes the tool, collects analytics, and provides a modern enterprise dashboard.

This project combines:

* LoRA Fine-Tuned Language Models
* Tool Calling Architecture
* JWT Authentication
* FastAPI Backend
* Streamlit Frontend
* OpenWeather API
* Gmail SMTP
* OpenRouteService Routing API
* SQLite Analytics Database

The system can understand natural language requests such as:

> "Book a cab from Hyderabad to Warangal"

> "What is the weather in Hyderabad?"

> "Send an email to [xyz@gmail.com](mailto:xyz@gmail.com)"

and automatically execute the appropriate tool.

---

# ✨ Features

## 🔐 Authentication & Security

* JWT Authentication
* User Signup
* User Login
* Role-Based Access Control
* Admin/User Roles
* Secure API Access

---

## 🤖 AI Tool Routing

LoRA Fine-Tuned Model predicts:

```json
{
  "tool": "book_cab"
}
```

Supported tools:

| Tool         | Description              |
| ------------ | ------------------------ |
| book_cab     | Route & fare estimation  |
| weather      | Real-time weather        |
| send_email   | SMTP email sending       |
| order_food   | Food ordering simulation |
| book_hotel   | Hotel booking simulation |
| set_reminder | Reminder scheduling      |

---

## 🌎 Real API Integrations

### OpenWeather API

Provides temperature, humidity, and weather conditions.

```json
{
  "temperature": "33°C",
  "humidity": "48%",
  "condition": "Partly Cloudy"
}
```

### Gmail SMTP

Sends actual emails using Gmail App Password and SMTP SSL.

### OpenRouteService API

Provides distance calculation, route planning, ETA estimation, and fare calculation.

```json
{
  "pickup": "Hyderabad",
  "drop": "Warangal",
  "distance_km": 148.3,
  "duration_min": 126,
  "estimated_fare": "₹1860"
}
```

---

## 📊 Analytics Dashboard

Tracks:

* Total Requests
* Success Rate
* Average Latency
* Confidence Score
* Unique Tools Used
* Tool Usage Statistics

Data is stored in SQLite database:

```text
tool_calls.db
```

---

## 📈 Monitoring Dashboard

Monitors:

* CPU Usage
* RAM Usage
* Disk Usage
* Total Requests
* Success %
* Failure %

Built using:

```text
psutil
SQLite
Streamlit
```

---

## 🐳 Docker Support

```bash
docker compose up --build
```

Services:

* Frontend Container
* Backend Container

---

## 🧠 LoRA Fine-Tuning Pipeline

```text
Dataset
   ↓
SFT Training
   ↓
LoRA Adapter
   ↓
DPO Fine-Tuning
   ↓
Inference API
```

| Model     | Accuracy |
| --------- | -------- |
| Base GPT2 | 72%      |
| SFT LoRA  | 91%      |
| DPO LoRA  | 96%      |

---

# 🏗️ System Architecture

<img width="1536" height="1024" alt="System Architecture" src="https://github.com/user-attachments/assets/4df2da30-1685-4424-bb09-bcda50e73649" />

---

# 📂 Project Structure

<img width="1536" height="1024" alt="Project Structure" src="https://github.com/user-attachments/assets/c4cf4bc6-935e-4170-bd55-29fb4a856569" />

---

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/Ganesh0181/ai-tool-orchestrator.git
cd ai-tool-orchestrator
```

## Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
```

## Install Requirements

```bash
pip install -r requirements.txt
```

## Configure Environment Variables

Create a `.env` file:

```env
JWT_SECRET=your_secret_key
OPENWEATHER_API_KEY=your_key
SMTP_EMAIL=your_email@gmail.com
SMTP_PASSWORD=your_app_password
ORS_API_KEY=your_openrouteservice_key
```

---

# 🚀 Running the Project

## Backend

```bash
python -m uvicorn api.server:app --reload --port 7600
```

API Docs:

```text
http://localhost:7600/docs
```

## Frontend

```bash
streamlit run app/streamlit_app.py --server.port 7500
```

Application:

```text
http://localhost:7500
```

---

# 📸 Screenshots

## 1. Login Page

<img width="1536" height="1024" alt="Login Page" src="https://github.com/user-attachments/assets/8b3ed798-f686-4ed7-9dbb-4d5df01b3bc0" />

---

## 2. Dashboard

<img width="1536" height="1024" alt="Dashboard" src="https://github.com/user-attachments/assets/f7064b28-9c3e-4162-9fd5-9a6bb14608dc" />

---

## 3. Cab Booking

<img width="1536" height="1024" alt="Cab Booking" src="https://github.com/user-attachments/assets/bc80e1bc-db80-4b75-b020-fcd52931aaf6" />

---

## 4. Weather Tool

<img width="1536" height="1024" alt="Weather Tool" src="https://github.com/user-attachments/assets/0b0e78a1-f55e-44ab-baa2-29d47597c213" />

---

## 5. Email Tool

<img width="1536" height="1024" alt="Email Tool" src="https://github.com/user-attachments/assets/0121da1c-7481-4195-ba5f-9d2c58d56c98" />

---

## 6. Monitoring Dashboard

<img width="1536" height="1024" alt="Monitoring Dashboard" src="https://github.com/user-attachments/assets/604494d4-b185-4a93-869a-c17a170c6ddd" />

---

# 🎯 Resume Highlights

* Developed Enterprise AI Tool Calling Platform using FastAPI, Streamlit, and LoRA Fine-Tuning.
* Integrated JWT Authentication, OpenWeather API, Gmail SMTP, and OpenRouteService.
* Built analytics dashboard with SQLite logging and monitoring features.
* Implemented multi-tool execution pipeline with confidence scoring and feedback collection.
* Containerized deployment using Docker and automated workflows using GitHub Actions.

---

# 🛠️ Tech Stack

## Frontend

* Streamlit

## Backend

* FastAPI
* Uvicorn

## AI

* Transformers
* PEFT
* LoRA
* DPO

## Database

* SQLite

## APIs

* OpenWeather
* Gmail SMTP
* OpenRouteService

## DevOps

* Docker
* GitHub Actions

---

# 👨‍💻 Author

S. Ganesh

B.Tech – Artificial Intelligence & Machine Learning

GitHub: https://github.com/Ganesh0181

LinkedIn: https://www.linkedin.com/in/ganesh-chary-sanugondla-14b14133b
