# 🛡️ She-ield

<p align="center">
  <h2 align="center">AI-Powered Women's Safety Platform</h2>

  <p align="center">
    Real-Time Safety • Live Location Tracking • AI Threat Detection • Emergency Response
  </p>
</p>

---

## 📱 Application Preview

<p align="center">
  <img src="./assets/login.jpeg" alt="Login" width="180">
  <img src="./assets/home.jpeg" alt="Home" width="180">
  <img src="./assets/tracking.jpeg" alt="Tracking" width="180">
  <img src="./assets/contacts.jpeg" alt="Contacts" width="180">
  <img src="./assets/sos.jpeg" alt="SOS" width="180">
  <img src="./assets/profile.jpeg" alt="Profile" width="180">
</p>

---

## ✨ Features

- 🚨 One-Tap SOS Emergency Alerts
- 📍 Real-Time Live Location Tracking
- 👥 Trusted Contact Management
- 🔐 JWT-Based Secure Authentication
- 🤖 AI-Powered Threat Detection
- 🎤 Emergency Audio Analysis
- 📷 Evidence Upload Support
- 🔄 Real-Time Communication using WebSockets
- ⚡ High Performance FastAPI Backend

---

## 🏗️ System Architecture

<p align="center">
  <img src="./assets/architecture.png" width="900" alt="She-ield Architecture"/>
</p>

---

## 🔗 Project Links

### 🌐 Frontend Repository

**Frontend:**  
https://github.com/Aayansh-singh-24/Fronted-Safe_her

### 📚 Backend API Documentation

**Swagger UI:**  
https://your-backend-domain/docs

**ReDoc:**  
https://your-backend-domain/redoc

> **⚠️ Backend Availability**
>
> The backend is hosted on a temporary cloud instance.
> The API documentation links above may change or become unavailable when the server expires.
> If the documentation is inaccessible, please run the backend locally.

---

## 🚀 Tech Stack

| Category | Technologies |
|-----------|--------------|
| **Backend** | FastAPI, SQLAlchemy, PostgreSQL |
| **Authentication** | JWT |
| **Realtime** | WebSockets |
| **AI / ML** | Python, Speech Recognition, Threat Detection |
| **Deployment** | Docker, Docker Compose, AWS EC2 |

---

## 📂 Repository Structure

```text
She-ield
│
├── backend/
├── ml-service/
├── assets/
│   ├── architecture.png
│   ├── login.jpeg
│   ├── home.jpeg
│   ├── tracking.jpeg
│   ├── contacts.jpeg
│   ├── sos.jpeg
│   └── profile.jpeg
│
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## ⚙️ Getting Started

### Clone Repository

```bash
git clone https://github.com/Aayansh-singh-24/She-ield.git

cd She-ield
```

---

### Install Dependencies

```bash
cd backend

pip install -r requirements.txt
```

---

### Run Backend

```bash
uvicorn app.main:app --reload
```

Backend will be available at

```
http://127.0.0.1:8000
```

Swagger Documentation

```
http://127.0.0.1:8000/docs
```

ReDoc Documentation

```
http://127.0.0.1:8000/redoc
```

---

## 🔮 Roadmap

- ✅ Live Location Tracking
- ✅ Trusted Contacts
- ✅ SOS Alerts
- ✅ JWT Authentication
- 🚧 Offline Threat Detection
- 🚧 Background Location Updates
- 🚧 Push Notifications
- 🚧 Voice Distress Detection
- 🚧 Wearable Device Integration

---

## 📄 License

This project is licensed under the **MIT License**.
