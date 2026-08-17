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
  <img src="./assets/tracking.jpeg" alt="Tracking" width="180">
  <img src="./assets/contacts.jpeg" alt="Contacts" width="180">
  <img src="./assets/sos.jpeg" alt="SOS" width="180">
</p>

---

## ✨ Features

- 🚨 **One-Tap SOS Emergency Alerts:** Instantly notify trusted contacts with your live location via SMS.
- 📍 **Real-Time Live Location Tracking:** Share a live Google Maps link with your emergency contacts.
- 👥 **Trusted Contact Management:** Easily add, edit, and remove emergency contacts.
- 🔐 **Secure Authentication:** JWT-based user authentication with OTP email verification.
- 🤖 **AI-Powered Threat Detection:** An ML microservice analyzes audio recordings for distress keywords (e.g., "help", "bachao") and scream signatures.
- 🎤 **Emergency Audio Analysis:** Upload audio files for threat analysis and evidence storage.
- 🔄 **Real-Time Communication:** Utilizes WebSockets for instantaneous updates.
- ⚡ **High-Performance Backend:** Built with FastAPI for speed and scalability.

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
https://13.53.89.228:8000/docs

**ReDoc:**  
https://13.53.89.228:8000/redoc

> **⚠️ Backend Availability**
>
> The backend might be hosted on a temporary cloud instance. The API documentation links above may change or become unavailable. If the documentation is inaccessible, please run the backend locally.

---

##  Tech Stack

| Category | Technologies |
|-----------|--------------|
| **Backend** | FastAPI, SQLAlchemy, PostgreSQL |
| **Authentication** | JWT, OTP Verification |
| **Realtime** | WebSockets |
| **AI / ML** | Python, SpeechRecognition, NumPy |
| **Deployment** | Docker, Docker Compose |

---

## 📂 Repository Structure

```text
She-ield/
│
├── Backend/
│   ├── src/
│   ├── main.py
│   └── requirements.txt
│
├── ML-Services/
│   ├── main.py
│   └── requirements.txt
│
├── assets/
│   ├── architecture.png
│   └── *.jpeg
│
├── docker-compose.yaml
└── README.md
```

---

## ⚙️ Getting Started

### Clone Repository

```bash
git clone https://github.com/Aayansh-singh-24/She-ield.git
cd She-ield
```

### Install Dependencies

Navigate to the backend directory and install the required Python packages.

```bash
cd Backend
pip install -r requirements.txt
```

### Run Backend Server

Start the development server using Uvicorn.

```bash
uvicorn main:app --reload
```

The backend API will be available at `http://127.0.0.1:8000`.

- **Swagger Documentation:** `http://127.0.0.1:8000/docs`
- **ReDoc Documentation:** `http://127.0.0.1:8000/redoc`

### Run with Docker

For a complete setup including the database and ML service, you can use Docker Compose.

1.  Create a `docker-compose.env` file in the root directory for PostgreSQL credentials.
2.  Ensure your `Backend/.env` file is correctly configured.
3.  Run the following command from the root directory:

```bash
docker-compose up --build
```


## 📄 License

This project is licensed under the **MIT License**.
