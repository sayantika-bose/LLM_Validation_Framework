# OWASP LLM Test Framework

This project provides a simple framework to test Large Language Models (LLMs) against 5 selected OWASP Top 10 LLM security risks. It features a modular FastAPI backend and a static HTML/JS frontend, all containerized for easy deployment.

## Features
- **Predefined OWASP LLM test cases**: 5 categories, each with multiple randomized prompts
- **Frontend**: Simple UI to select, run, and mark test cases as pass/fail, with test history
- **Backend**: Modular FastAPI app using LangChain and Ollama for LLM interaction
- **Dockerized**: Easy to run locally with Docker Compose

---

## Project Structure

```
CNLABS_TASK/
├── backend/
│   ├── main.py                # FastAPI entry point
│   ├── requirements.txt      # Backend dependencies
│   ├── Dockerfile            # Backend Dockerfile
│   └── app/
│       ├── models/           # Pydantic models
│       ├── routers/          # FastAPI routers
│       ├── services/         # LLM service logic
│       └── prompts/          # Jinja2 prompt templates
├── frontend/
│   ├── index.html            # Main UI
│   ├── style.css             # UI styles
│   ├── app.js                # UI logic
│   ├── Dockerfile            # Frontend Dockerfile
│   └── nginx.conf            # Nginx config for static/API proxy
├── docker-compose.yml        # Orchestration for backend/frontend
└── .gitignore
```

---

## Setup & Usage

### Prerequisites
- [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/)

### 1. Build and Run with Docker Compose
From the project root:
```sh
docker-compose up --build
```
- The **frontend** will be available at: [http://localhost](http://localhost)
- The **backend API** will be at: [http://localhost:8000](http://localhost:8000)

### 2. Manual (Dev) Setup (Optional)
If you want to run the backend and frontend separately (without Docker):

#### Backend
```sh
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend
Just open `frontend/index.html` in your browser (API must be running at localhost:8000).

---

## How It Works

### Frontend
- Select a test case (OWASP LLM risk category)
- Click **Run Test** to send a random prompt from that category to the backend
- View the model's response (with optional "think" reasoning toggle)
- Mark the result as **Pass** or **Fail**
- Click **Continue Testing** to try more prompts
- Test history is shown below the UI

### Backend
- Receives prompt via `/api/ask` endpoint
- Renders the prompt using a Jinja2 template
- Sends the prompt to the LLM (via LangChain + Ollama)
- Returns the LLM's response to the frontend

---

## Customization
- Add or edit prompts in `backend/app/prompts/chat_prompt.j2` or in the frontend JS
- Add more test cases or categories in `frontend/app.js`
- Adjust backend logic in `backend/app/services/llm_service.py`

---

## License
MIT
