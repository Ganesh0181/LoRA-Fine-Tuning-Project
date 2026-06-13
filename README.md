# 🚀 AI Tool Orchestrator

Enterprise-grade AI Tool Calling Platform powered by LoRA Fine-Tuned Models, FastAPI, Streamlit, JWT Authentication, and Real-World APIs.

---

## 📌 Project Overview

AI Tool Orchestrator is a production-style AI system that intelligently routes user requests to the appropriate tool, executes the tool, collects analytics, and provides a modern enterprise dashboard.

Instead of using rule-based applications, this project combines:

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

instead of relying solely on regex-based routing.

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

Provides:

* Temperature
* Humidity
* Weather Conditions

Example:

```json
{
  "temperature": "33°C",
  "humidity": "48%",
  "condition": "Partly Cloudy"
}
```

---

### Gmail SMTP

Sends actual emails using:

* Gmail App Password
* SMTP SSL

Example:

```text
To: user@gmail.com
Subject: Test Mail

Hello from AI Tool Orchestrator
```

---

### OpenRouteService API

Provides:

* Distance Calculation
* Route Planning
* ETA Estimation
* Fare Calculation

Example:

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

Stored in:

```text
SQLite Database
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

Containerized Deployment

Supports:

```bash
docker compose up --build
```

Services:

* Frontend Container
* Backend Container

---

## 🧠 LoRA Fine-Tuning Pipeline

Training Pipeline:

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

Models Compared:

| Model     | Accuracy |
| --------- | -------- |
| Base GPT2 | 72%      |
| SFT LoRA  | 91%      |
| DPO LoRA  | 96%      |

---

# 🏗️ System Architecture

```text
+---------------------+
| Streamlit Frontend  |
| Port : 7500         |
+----------+----------+
           |
           |
           v
+---------------------+
| FastAPI Backend     |
| Port : 7600         |
+----------+----------+
           |
           |
           v
+---------------------+
| LoRA Tool Router    |
+----------+----------+
           |
   -----------------------
   |     |      |       |
   v     v      v       v

Weather  Email  Cab   Hotel
 API     SMTP   API   Mock
```

---

# 📂 Project Structure

```text
LoRA-Fine-Tuning-Project
│
├── api
│   └── server.py
│
├── app
│   └── streamlit_app.py
│
├── model
│   └── inference.py
│
├── pages
│   ├── 3_Monitoring.py
│   └── 4_Model_Comparison.py
│
├── data
├── outputs
├── reports
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
├── .env
└── tool_calls.db
```

---

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/ai-tool-orchestrator.git

cd ai-tool-orchestrator
```

---

## Create Virtual Environment

```bash
python -m venv venv

venv\Scripts\activate
```

---

## Install Requirements

```bash
pip install -r requirements.txt
```

---

## Configure Environment Variables

Create:

```text
.env
```

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

API:

```text
http://localhost:7600/docs
```

---

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

## Login Page

Add Screenshot:

```text
screenshots/login.png
```

---

## Dashboard

Add Screenshot:

```text
screenshots/dashboard.png
```

---

## Cab Booking

Add Screenshot:

```text
screenshots/cab.png
```

---

## Weather Tool

Add Screenshot:

```text
screenshots/weather.png
```

---

## Email Tool

Add Screenshot:

```text
screenshots/email.png
```

---

## Monitoring Dashboard

Add Screenshot:

```text
screenshots/monitoring.png
```

---

# 🎯 Resume Highlights

* Developed Enterprise AI Tool Calling Platform using FastAPI, Streamlit and LoRA Fine-Tuning.
* Integrated JWT Authentication, OpenWeather API, Gmail SMTP and OpenRouteService.
* Built analytics dashboard with SQLite logging and monitoring features.
* Implemented multi-tool execution pipeline with confidence scoring and feedback collection.
* Containerized deployment using Docker and automated workflows using GitHub Actions.

---

# 🛠️ Tech Stack

### Frontend

* Streamlit

### Backend

* FastAPI
* Uvicorn

### AI

* Transformers
* PEFT
* LoRA
* DPO

### Database

* SQLite

### APIs

* OpenWeather
* Gmail SMTP
* OpenRouteService

### DevOps

* Docker
* GitHub Actions

---

# 👨‍💻 Author

S. Ganesh

B.Tech – Artificial Intelligence & Machine Learning

GitHub: https://github.com/YOUR_USERNAME

LinkedIn: https://linkedin.com/in/YOUR_PROFILE
