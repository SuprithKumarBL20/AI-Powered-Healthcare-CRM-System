<div align="center">

# 🚀 AI-First CRM for Healthcare Professionals (HCP)

### AI-Powered Healthcare CRM using React, FastAPI, LangGraph & Groq LLM

An intelligent Customer Relationship Management (CRM) platform designed for pharmaceutical sales representatives to efficiently manage Healthcare Professional (HCP) interactions using conversational AI and agentic workflows.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi)
![React](https://img.shields.io/badge/React-Vite-61DAFB?logo=react)
![LangGraph](https://img.shields.io/badge/LangGraph-Agent-orange)
![LangChain](https://img.shields.io/badge/LangChain-LLM-green)
![Groq](https://img.shields.io/badge/Groq-LLM-red)
![MySQL](https://img.shields.io/badge/MySQL-Database-blue?logo=mysql)

</div>

---

# 📖 Overview

AI-First CRM for Healthcare Professionals is an AI-powered Customer Relationship Management platform developed for pharmaceutical sales representatives.

The application enables representatives to interact with an intelligent AI assistant that understands natural language, extracts meeting details, performs compliance analysis, generates follow-up tasks, and manages Healthcare Professional (HCP) information.

The system is powered by **LangGraph**, **LangChain**, and **Groq LLM**, providing an intelligent workflow for healthcare interaction management.

---

# ✨ Key Features

## 🤖 AI CRM Assistant

- Natural language interaction logging
- Conversational AI assistant
- Intelligent meeting detail extraction
- Automatic form population
- LangGraph tool-calling workflow

---

## 👨‍⚕️ HCP Profile Management

- View Healthcare Professional profiles
- Previous interaction history
- Contact preferences
- Specialization details
- AI-generated Next Best Action

---

## 📋 Interaction Management

- Create interactions
- Edit previous interactions
- Store meeting summaries
- Discussion tracking
- Communication channel management

---

## ✅ Compliance Analysis

- Real-time compliance verification
- Detect risky conversations
- Highlight policy violations
- AI-generated compliance reports
- Review discussion topics

---

## 📧 Follow-up Generation

- AI-generated follow-up tasks
- Personalized email drafts
- Reminder scheduling
- Recommended next actions

---

# 🏗️ System Architecture

```text
                    React Frontend
                          │
                    REST API Calls
                          │
                          ▼
                  FastAPI Backend
                          │
          ┌───────────────┴───────────────┐
          │                               │
          ▼                               ▼
     LangGraph Agent              SQLAlchemy ORM
          │                               │
          ▼                               ▼
    LangChain + Groq LLM              MySQL
          │
          ▼
     AI Tool Execution
```

---

# 🛠️ Technology Stack

| Category | Technologies |
|-----------|--------------|
| Frontend | React, Vite, JavaScript, CSS, Axios |
| Backend | Python, FastAPI, SQLAlchemy, Pydantic |
| AI | LangGraph, LangChain, Groq LLM |
| Database | MySQL |

---

# 📂 Project Structure

```text
ai-first-crm-hcp/
│
├── backend/
│   ├── app/
│   │   ├── agent/
│   │   │   ├── graph.py
│   │   │   ├── llm.py
│   │   │   └── tools.py
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── seed.py
│   │   └── main.py
│   │
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   ├── src/
│   ├── package.json
│   └── vite.config.js
│
├── docs/
│   └── screenshots/
│
├── .gitignore
└── README.md
```

---

# 📸 Application Screenshots

## 🏠 Dashboard

<p align="center">
  <img src="docs/screenshots/dashboard.png" width="900">
</p>

---

## 🤖 AI Chat Assistant

<p align="center">
  <img src="docs/screenshots/chat-interface.png" width="900">
</p>

---

## 👨‍⚕️ HCP Profile

<p align="center">
  <img src="docs/screenshots/hcp-profile.png" width="900">
</p>

---

## 📜 Interaction History

<p align="center">
  <img src="docs/screenshots/interaction-history.png" width="900">
</p>

---

## ✏️ Edit Interaction

<p align="center">
  <img src="docs/screenshots/edit-interaction.png" width="900">
</p>

---

## 📧 Follow-up Panel

<p align="center">
  <img src="docs/screenshots/follow-up-panel.png" width="900">
</p>

---

# 🚀 Getting Started

## Prerequisites

- Python 3.10 or above
- Node.js 18 or above
- MySQL Server
- Groq API Key *(Optional)*

---

# Backend Setup

Navigate to the backend directory.

```bash
cd backend
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

#### Windows

```bash
venv\Scripts\activate
```

#### Linux / macOS

```bash
source venv/bin/activate
```

---

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

### Configure Environment Variables

Create a `.env` file inside the backend folder.

```env
GROQ_API_KEY=YOUR_GROQ_API_KEY

DATABASE_URL=mysql+pymysql://username:password@localhost:3306/crmdb
```

---

### Seed the Database

```bash
python -m app.seed
```

---

### Run the Backend

```bash
uvicorn app.main:app --reload --port 8081
```

Backend

```
http://localhost:8081
```

Swagger Documentation

```
http://localhost:8081/docs
```

---

# Frontend Setup

Navigate to frontend.

```bash
cd frontend
```

Install dependencies.

```bash
npm install
```

Start the development server.

```bash
npm run dev
```

Frontend

```
http://localhost:5173
```

---

# 🤖 AI Agent Workflow

```text
User Input
     │
     ▼
LangGraph Agent
     │
     ▼
Groq LLM
     │
     ▼
AI Tool Selection
     │
     ├────────► Get HCP Profile
     ├────────► Log Interaction
     ├────────► Analyze Compliance
     ├────────► Generate Follow-up
     └────────► Edit Interaction
```

---

# 🧰 AI Tools

| Tool | Description |
|------|-------------|
| Get HCP Profile | Retrieves Healthcare Professional details and interaction history |
| Log Interaction | Stores interaction details in the database |
| Analyze Compliance | Reviews conversations against compliance rules |
| Generate Follow-up | Creates AI-powered follow-up tasks and email drafts |
| Edit Interaction | Updates previously logged interactions |

---

# 📦 API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | `/docs` | Swagger API Documentation |
| POST | `/api/chat` | Conversational AI Assistant |
| GET | `/api/hcp` | Retrieve HCP Profile |
| POST | `/api/interactions` | Create Interaction |
| PUT | `/api/interactions/{id}` | Update Interaction |

---

# 🎯 Future Enhancements

- 🎤 Voice-based interaction logging
- 👥 Multi-agent AI workflow
- 🔐 Role-based authentication
- 📊 Analytics dashboard
- 📄 PDF report generation
- 📅 Calendar scheduling
- 📧 Email integration
- ☁️ Cloud deployment
- 📱 Mobile application support

---

# 👨‍💻 Author

**Suprith Kumar B L**

Computer Science & Engineering

### Skills

- Python
- FastAPI
- React
- LangGraph
- LangChain
- AI Agents
- Full Stack Development

**GitHub**

https://github.com/SuprithKumarBL20

---

# ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub.

---

# 📄 License

This project is intended for educational, research, and demonstration purposes.
