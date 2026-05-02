# 🎓 AlumniConnect®
> **A premium, cinematic mentorship and networking platform bridging the gap between ambitious students and experienced alumni.**

[![Python](https://img.shields.io/badge/python-3.12%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/django-6.0-092e20?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

AlumniConnect® is a high-fidelity, production-grade web application designed for educational institutions. It facilitates meaningful mentorships, secure networking, and professional growth through a stunning, cinematic user experience.

---

## ✨ Premium Features & Cinematic UI

### 🎞️ Cinematic Entrance & Visuals
*   **Logo-Fill Preloader**: A professional, session-aware cinematic entrance animation that prevents "hurried" page loads.
*   **CanvasFire Background**: A real-time particle engine rendering dynamic sparks, embers, and glow that blends seamlessly with the institutional campus background.
*   **Glassmorphic Design System**: A custom CSS framework utilizing deep blur effects, glowing borders, and tactile micro-interactions.

### 🔐 Modern Authentication
*   **Role-Specific Portals**: Dedicated, sequenced entrance animations for Student, Alumni, and Admin logins.
*   **Advanced Security**: Password visibility toggles, session-based memory, and secure role separation.

### 🤝 Mentorship & Networking
*   **1:1 Mentorship System**: Verified students can request mentorship from experienced alumni.
*   **Secure Messaging**: Direct, real-time communication channel unlocked upon mentorship approval.
*   **Opportunity Hub**: Centralized board for alumni to post job openings, internships, and events.

---

## 🛠 Tech Stack

| Category | Technology |
| :--- | :--- |
| **Backend** | Django 6.0 (Python 3.12+) |
| **Styling** | Vanilla CSS3 (Custom Design System), Bootstrap 5 |
| **Interactions** | Vanilla JavaScript (ES6+), Canvas API (Particles) |
| **Database** | SQLite (Dev) / PostgreSQL (Prod) |
| **Typography** | Instrument Serif, Inter, Instrument Sans |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.12 or higher
- pip (Python package installer)

### Installation

**1. Clone and Navigate**
```bash
git clone https://github.com/yourusername/AlumniConnect.git
cd AlumniConnect
```

**2. Virtual Environment & Dependencies**
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Unix:
source venv/bin/activate

pip install django pillow
```

**3. Database Initialization**
```bash
cd alumniconnect
python manage.py migrate
python seed_data.py                         # Generates mock students, alumni, and jobs
```

**4. Start the Engine**
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000` to experience the cinematic entrance.

---

## 📁 Architecture Highlights

- **`static/css/main.css`**: The core design system including the Glassmorphism layers.
- **`static/js/main.js`**: Orchestrates the Particle Engine and AJAX animations.
- **`mainapp/`**: Contains the custom User model and the core mentorship logic.
- **`templates/base.html`**: The cinematic foundation containing the background canvas and session-aware preloader.

---

## 📜 License
Distributed under the MIT License. Built with ❤️ for educational excellence and professional connection.

---
*AlumniConnect® — Where Futures Connect*