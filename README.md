# 🎓 AlumniConnect®

> **A premium, full-stack mentorship and networking platform bridging the gap between ambitious students and experienced alumni.**

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![Django](https://img.shields.io/badge/django-4.x-success)
![Bootstrap](https://img.shields.io/badge/bootstrap-5.x-purple)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

AlumniConnect® is a cinematic, production-grade web application built to facilitate meaningful mentorships, professional networking, and opportunity sharing within educational institutions. Designed with a stunning **Dark Glassmorphic (Noir)** UI, it provides a seamless and engaging experience for all users.

---

## ✨ Key Features

- **Role-Based Access Control**: Dedicated portals and workflows for Students, Alumni, and Administrators.
- **Mentorship System**: Students can browse verified alumni profiles and send personalized mentorship requests.
- **Real-Time Communication**: A built-in, secure 1:1 messaging system unlocked after mentorship approval.
- **Opportunity Board**: A centralized hub for alumni to post jobs, internships, and networking events.
- **Cinematic UI/UX**: Built with a custom glassmorphism design system, smooth fade-rise animations, and modern typography (Instrument Serif & Inter).
- **Dynamic Dashboards**: Personalized analytics, pending requests, and activity feeds tailored to each user's role.
- **AJAX-Powered Modals**: Instant, reload-free profile viewing and interactions.

---

## 🛠 Tech Stack

| Category | Technology |
| :--- | :--- |
| **Backend Framework** | Django (Python) |
| **Frontend Styling** | Vanilla CSS, Bootstrap 5 (Grid & Utilities) |
| **Frontend Logic** | Vanilla JavaScript (AJAX, DOM Manipulation) |
| **Database** | SQLite (Development) / PostgreSQL (Production) |
| **Typography** | Google Fonts (Instrument Serif, Inter) |
| **Icons** | Bootstrap Icons |

---

## 🚀 Getting Started

Follow these instructions to set up the project on your local machine for development and testing.

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/yourusername/AlumniConnect.git
cd AlumniConnect
```

**2. Set up a virtual environment (Recommended)**
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

**3. Install dependencies**
```bash
pip install django pillow
```

**4. Run database migrations**
```bash
cd alumniconnect
python manage.py makemigrations mainapp
python manage.py migrate
```

**5. Seed the database with sample data**
```bash
python seed_data.py
```
*Note: This generates sample administrators, alumni, students, mentorship requests, and job posts.*

**6. Start the development server**
```bash
python manage.py runserver
```

Navigate to `http://127.0.0.1:8000` in your browser.

---

## 🔐 User Roles & Authentication

The platform features distinct login portals to maintain security and tailored user experiences:

| Role | Default Login URL | Access Level |
| :--- | :--- | :--- |
| **Student** | `/login/student/` | Can browse alumni, request mentorships, view jobs. |
| **Alumni** | `/login/alumni/` | Can accept/reject mentees, post jobs, network. |
| **Admin** | `/login/admin/` | Platform oversight, user verification, analytics. |

**Sample Credentials (from seed data):**
- **Admin**: `Admin` / `Admin@123`
- **Alumni**: `alumni1` / `Test@123`
- **Student**: `student1` / `Test@123`
- **Student**: `student2` / `basit123`

---

## 📁 Project Architecture

```text
alumniconnect/
├── alumniconnect/          # Django core configuration (settings, urls, wsgi)
├── mainapp/                # Main application logic
│   ├── models.py           # Database schemas (Custom User, Profile, Post, Message)
│   ├── views.py            # Route controllers and business logic
│   ├── urls.py             # Application routing
│   └── forms.py            # Django form definitions
├── static/                 # Static assets
│   ├── css/main.css        # Custom Glassmorphic CSS design system
│   ├── js/main.js          # Global JavaScript and AJAX handlers
│   └── images/             # UI icons and backgrounds
├── templates/              # HTML templates
│   ├── auth/               # Role-specific login & registration
│   ├── dashboard/          # Role-specific dashboard layouts
│   └── ...                 # Component and page templates
├── manage.py               # Django command-line utility
└── seed_data.py            # Script for populating initial mock data
```

---

## 🎨 Design System & Aesthetics

AlumniConnect ditches the standard corporate look for a **Premium Noir** aesthetic.

- **Color Palette**: Deep ocean backgrounds (`#001a2c`) paired with cyan (`#00c8ff`) and gold (`#f0b429`) accents.
- **Glassmorphism**: Extensive use of `backdrop-filter: blur()`, semi-transparent backgrounds, and subtle glowing borders (`.glass-card`, `.form-control-glass`).
- **Micro-Interactions**: Hover lifts, fade-in-up observers (`.animate-rise`), and dynamic autocomplete styling fixes to maintain the dark theme.

---

## 🌐 Production Deployment

For production environments, ensure you update `settings.py` securely:

1. Set `DEBUG = False`.
2. Configure a secure `SECRET_KEY` via environment variables.
3. Set `ALLOWED_HOSTS` to your domain.
4. Configure a production-grade database (e.g., **PostgreSQL**).
5. Use **WhiteNoise** or a reverse proxy (Nginx) for serving static files.
6. Deploy using a WSGI server like **Gunicorn**.

---

## 🤝 Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📜 License

Distributed under the MIT License. Built with ❤️ for educational and institutional use.

---
*AlumniConnect® — Where Futures Connect*