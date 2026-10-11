# Hospital Room Radar AI

**AI-powered hospital room safety screening using specialized vision agents.**

Hospital Room Radar AI analyzes hospital room images to identify potential safety concerns. Using three specialized AI agents, the application generates structured safety reports with supporting evidence, risk levels, and recommended actions.

**Live Demo : https://hospital-room-radar-ai.vercel.app/**

## Features

- **Patient & Fall Safety:** Identifies visible trip hazards, obstructed walking paths, and potential fall risks.
- **Equipment & Patient Accessibility:** Identifies visible equipment setup concerns, disconnected connections, and barriers to accessing essential devices.
- **Infection Control:** Detects visible hygiene, cleanliness, and medical-waste handling concerns.
- **AI-Powered Report Consolidation:** Uses Google Gemini to combine agent findings and reduce duplicate reports.
- **Structured Safety Reports:** Presents identified concerns with evidence, risk levels, source agents, and recommended actions.
- **Human Verification:** Flags AI-generated findings for review before corrective action.

## Tech Stack

| Component | Technology |
|---|---|
| Frontend | React, Vite |
| Backend | Python, FastAPI |
| Vision Analysis | Groq-hosted vision model |
| Report Generation | Google Gemini API |
| Image Storage | AWS DynamoDB |
| Frontend Deployment | Vercel |
| Backend Deployment | Render |

## Getting Started

### Prerequisites

- Python and pip
- Node.js and npm
- Git
- Required API credentials and AWS configuration

### 1. Clone the Repository

```bash
git clone https://github.com/Yamini1025/Hospital-Room-Radar-AI.git
cd Hospital-Room-Radar-AI
```

### 2. Start the Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

On Windows, activate the virtual environment with:

```bash
venv\Scripts\activate
```

Create a `.env` file in the `backend` directory and add the environment variables required by the application. Use the variable names defined in the source code.

Start the API:

```bash
uvicorn main:app --reload
```

The backend should be available at `http://127.0.0.1:8000`.

If enabled, API documentation is available at `http://127.0.0.1:8000/docs`.

### 3. Start the Frontend

Open a separate terminal:

```bash
cd frontend
npm install
npm run dev
```

Open the local URL provided by Vite. Ensure the frontend is configured to communicate with the backend URL you are using.

## Deployment

The application is deployed using:

- **Vercel** for the frontend
- **Render** for the backend

The deployed application requires the appropriate environment variables, API credentials, and backend access configuration.

## Responsible AI & Limitations

Hospital Room Radar AI is an experimental AI-assisted visual screening prototype.

- Findings may be inaccurate or incomplete.
- Image analysis cannot reliably establish whether equipment is operational or whether a surface is contaminated.
- Risk levels are AI-generated estimates, not clinically validated measurements.
- All findings require human verification.

**This application does not replace professional hospital safety inspections, clinical judgment, or established infection-control procedures. It does not certify a room as safe.**

## Future Improvements

- Improve hazard detection accuracy and consistency.
- Reduce false positives and duplicate findings.
- Evaluate performance using labeled hospital-room images.
- Improve agent error handling and report traceability.
