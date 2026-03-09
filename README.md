
# CuraMind AI: HIPAA-Compliant Telehealth & Diagnostics Platform

![Django](https://img.shields.io/badge/Django-5.0+-092e20?style=for-the-badge&logo=django)
![Python](https://img.shields.io/badge/Python-3.12+-3776ab?style=for-the-badge&logo=python)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16+-336791?style=for-the-badge&logo=postgresql)
![Redis](https://img.shields.io/badge/Redis-Asynchronous-dc382d?style=for-the-badge&logo=redis)
![Celery](https://img.shields.io/badge/Celery-Distributed_Tasks-37814a?style=for-the-badge&logo=celery)
![License](https://img.shields.io/badge/Security-HIPAA_Compliant-blue?style=for-the-badge)


CuraMind AI is a secure, modular diagnostic platform designed to bridge the gap between patients and doctors through AI-driven medical image analysis. It features robust Role-Based Access Control (RBAC), secure DICOM/image handling, and asynchronous processing for high-performance diagnostics.

## 🖼️ Visual Showcase

| Input Medical X-Ray | AI-Generated Heatmap Analysis |
| --- | --- |
|  |  |
| *Original skull X-ray uploaded by patient.* | *Grad-CAM visualization highlighting diagnostic focus.* |

## 🚀 Features

* **Secure Authentication**: Custom User Model with dedicated Doctor and Patient roles.
* **Asynchronous AI Pipeline**: Celery and Redis integration for non-blocking image analysis.
* **HIPAA-Compliant Security**: Binary-level file validation and strict data isolation via RBAC.
* **Medical Dashboard**: A clean interface for patients to track report history and AI analysis status.
* **Telehealth Scheduling**: Appointment management system for doctor-patient consultations.

## 📂 Project Structure

```text
CuraMind-AI-Platform/
├── apps/
│   ├── users/          # Custom Auth & Role Management
│   ├── diagnostics/    # Medical Records & AI Inference
│   └── appointments/   # Scheduling Logic
├── config/             # Project Settings & Routing
├── media/              # Secure Medical Image Storage (HIPAA Validated)
├── static/             # Frontend Assets
└── manage.py

```

## 🛠️ Setup & Installation

1. **Clone the repository:**

```bash
git clone https://github.com/ArchitYadav07/CuraMind-AI-HIPAA-Compliant-Telehealth-Diagnostics-Platform.git
cd CuraMind-AI-HIPAA-Compliant-Telehealth-Diagnostics-Platform

```

2. **Set up Virtual Environment:**

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

```

3. **Install Dependencies:**

```bash
pip install -r requirements.txt

```

4. **Environment Variables:**
Create a `.env` file and configure your `PostgreSQL` and `Redis` credentials.
5. **Run Migrations:**

```bash
python manage.py migrate

```

6. **Start the Development Server:**

```bash
python manage.py runserver

```

## 📈 Development Roadmap

* [x] **Week 1**: Core Infrastructure & PostgreSQL setup.
* [x] **Week 2**: Secure Portals, RBAC, and File Validation.
* [x] **Week 3**: AI Integration & Asynchronous Workers.
* [ ] **Week 4**: Deployment via Docker & Nginx.

---

### Developed by

**Archit Yadav** [Portfolio](https://www.google.com/search?q=https://archityadav.netlify.app) | [GitHub](https://www.google.com/search?q=https://github.com/ArchitYadav07) | [LinkedIn](https://www.google.com/search?q=https://linkedin.com/in/archityadav07)

---

**Would you like me to help you create a Dockerfile or a `docker-compose.yml` to make this setup even easier for others to run?**
