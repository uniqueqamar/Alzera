
# ALZERA

**Clinical Decision Support for Progressive Diagnostic Prioritization**

ALZERA is a clinical decision-support proof of concept designed to help clinicians prioritize patients for progressive diagnostic evaluation. It aggregates longitudinal patient data, risk indicators, trajectory signals, contributing factors, and suggested next diagnostic stages into a single interface.

> [!IMPORTANT]
> **Clinical Disclaimer:** ALZERA is a decision-support prototype. It **does not** diagnose Alzheimer's disease, prescribe treatment, or replace clinical judgment. The current demonstration relies entirely on synthetic patient data.

---

## Overview

Progressive neurodegenerative conditions often require clinicians to interpret complex information collected across multiple visits. ALZERA addresses this friction by providing an actionable prioritization layer.

Rather than acting as a static record viewer, ALZERA delivers:

* **Patient-level risk prioritization** to highlight urgent cases.
* **Longitudinal trajectory tracking** across multi-visit observations.
* **Explainable evidence confidence** and contributing risk factors.
* **Clinician-in-the-loop workflows** featuring explicit acceptance or override controls.
* **Audit logging** to trace all human decision interactions.

---

## Key Features

### 1. Patient Prioritization & Trajectories

* Surface high-priority cases using risk scores, diagnostic stages, and trajectory signals (e.g., stable vs. rapidly worsening).
* Monitor multi-visit patient records dynamically instead of analyzing isolated points in time.

### 2. Explainable Insights

* Contextualize scores with explicit contributing factors, confidence levels, and clinical safety disclaimers.

### 3. Progressive Diagnostic Recommendations

* Propose next diagnostic steps accompanied by explicit reasoning.
* Requires mandatory clinician review—recommendations are never autonomous.

### 4. Override & Audit Workflows

* **Accept / Override:** Allows clinicians to accept recommendations or force an alternate stage with documented reasoning.
* **Audit Trail:** Logs every decision with `patient_id`, `action`, `details`, and `timestamp`.

---

## Architecture

```text
┌──────────────────────────────────────────────────────────┐
│                        ALZERA UI                         │
│       Next.js 14 + React + TypeScript + Tailwind CSS      │
└────────────────────────────┬─────────────────────────────┘
                             │ HTTP / REST
                             ▼
┌──────────────────────────────────────────────────────────┐
│                        ALZERA API                        │
│             FastAPI + Pydantic + Pandas                  │
└────────────────────────────┬─────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────┐
│                    Synthetic Dataset                     │
│        patient_visits.csv | patient_summary.csv          │
└──────────────────────────────────────────────────────────┘

```

---

## Technology Stack

| Layer | Technologies |
| --- | --- |
| **Frontend** | Next.js, React, TypeScript, Tailwind CSS |
| **Visualization & UI** | Recharts, Framer Motion |
| **Backend API** | FastAPI, Uvicorn, Pydantic |
| **Data Processing** | Pandas, NumPy |
| **Storage** | Synthetic CSV Datasets |

---

## Project Structure

```text
Alzera/
├── backend/
│   ├── app/
│   │   └── main.py
│   ├── data/
│   │   ├── patient_summary.csv
│   │   └── patient_visits.csv
│   └── requirements.txt
│
├── frontend/
│   ├── app/
│   │   ├── analytics/
│   │   ├── audit/
│   │   ├── patient/
│   │   ├── layout.tsx
│   │   └── page.tsx
│   ├── components/
│   ├── lib/
│   └── package.json
│
├── .gitignore
└── README.md

```

---

## Getting Started

### Prerequisites

* **Python** 3.10+
* **Node.js** 18+
* **npm**

### 1. Clone the Repository

```bash
git clone https://github.com/Tannuuuu/Alzera.git
cd Alzera

```

### 2. Backend Setup

```bash
cd backend

# Create and activate virtual environment
python -m venv .venv

# On Windows:
.venv\Scripts\Activate.ps1
# On macOS/Linux:
# source .venv/bin/activate

# Install dependencies and launch
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

```

* **API Base:** `http://localhost:8000`
* **Interactive Docs (Swagger):** `http://localhost:8000/docs`

### 3. Frontend Setup

Open a new terminal session:

```bash
cd frontend

# Install dependencies
npm install

# Configure environment
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

# Run development server
npm run dev

```

* **App URL:** `http://localhost:3000`

---

## API Reference

| Endpoint | Method | Description |
| --- | --- | --- |
| `/health` | `GET` | Returns status and synthetic record count |
| `/dashboard` | `GET` | Fetches latest record per patient, sorted by risk score |
| `/patients` | `GET` | Retrieves full list of available patient records |
| `/patients/{id}` | `GET` | Fetches patient details and historical longitudinal trajectory |
| `/patients/{id}/explanation` | `GET` | Surfacing contributing factors, risk score, and confidence |
| `/patients/{id}/recommendation` | `GET` | Returns current and suggested diagnostic stage transitions |
| `/patients/{id}/accept` | `POST` | Logs acceptance of the system suggestion |
| `/patients/{id}/override` | `POST` | Overrides suggestion with custom next stage and reasoning |
| `/audit` | `GET` | Fetches system-wide audit event logs |

---

## Clinical Safety & Disclaimer

ALZERA is strictly an **experimental research prototype** and **not a medical device**.

* It does not provide real medical diagnoses or prescribe treatments.
* It must not be deployed in clinical environments without formal validation, privacy controls, regulatory compliance, and security oversight.
* **No real patient data (PHI)** should ever be uploaded to or processed by this repository.

---

## License

This project is provided for research and development purposes. See the repository root for licensing details.
