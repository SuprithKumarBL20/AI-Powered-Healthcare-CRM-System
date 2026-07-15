<div align="center">

# 🚀 AI-First CRM for Healthcare Professionals (HCP)

### AI-Powered CRM Platform for Pharmaceutical Sales Representatives

Built using **React • FastAPI • LangGraph • LangChain • Groq LLM • MySQL**

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi)
![React](https://img.shields.io/badge/React-Frontend-61DAFB?logo=react)
![LangGraph](https://img.shields.io/badge/LangGraph-Agent-orange)
![LangChain](https://img.shields.io/badge/LangChain-LLM-green)
![MySQL](https://img.shields.io/badge/MySQL-Database-blue?logo=mysql)

</div>

---

## 📖 Overview

AI-First CRM for Healthcare Professionals (HCP) is an intelligent Customer Relationship Management platform developed for pharmaceutical sales representatives to efficiently manage doctor interactions.

The application combines **FastAPI**, **React**, **LangGraph**, **LangChain**, and **Groq LLM** to automate:

- 🤖 AI-assisted interaction logging
- 👨‍⚕️ Healthcare Professional profile management
- ✅ Compliance analysis
- 📧 AI-generated follow-ups
- 📊 Interaction history management

---

# 📸 Application Screenshots

<table>
<tr>
<td>

### Dashboard

<img src="docs/screenshots/dashboard.png" width="100%">

</td>

<td>

### AI Chat Assistant

<img src="docs/screenshots/chat-interface.png" width="100%">

</td>
</tr>

<tr>
<td>

### HCP Profile

<img src="docs/screenshots/hcp-profile.png" width="100%">

</td>

<td>

### Interaction History

<img src="docs/screenshots/interaction-history.png" width="100%">

</td>
</tr>

<tr>
<td>

### Edit Interaction

<img src="docs/screenshots/edit-interaction.png" width="100%">

</td>

<td>

### Follow-up Panel

<img src="docs/screenshots/follow-up-panel.png" width="100%">

</td>
</tr>
</table>

---

# ✨ Features

### 🤖 AI CRM Assistant

- AI-powered conversational interface
- Natural language interaction logging
- Intelligent meeting detail extraction
- LangGraph-based tool execution
- Automatic structured form generation

---

### 👨‍⚕️ HCP Management

- Healthcare Professional profiles
- Previous interaction history
- Communication preferences
- Doctor information management
- AI-generated next best action

---

### 📋 Interaction Management

- Create interactions
- Update interactions
- Meeting summaries
- Discussion tracking
- Communication channels

---

### ✅ Compliance Analysis

- Compliance verification
- Risk detection
- Conversation review
- Policy recommendations
- AI-generated compliance reports

---

### 📧 Follow-up Generation

- AI-generated follow-up tasks
- Personalized email drafts
- Reminder scheduling
- Suggested next actions

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
     Tool Calling Workflow
```

---

# 🛠️ Technology Stack

| Category | Technologies |
|-----------|--------------|
| Frontend | React, Vite, JavaScript, CSS, Axios |
| Backend | FastAPI, Python, SQLAlchemy, Pydantic |
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

# 🚀 Getting Started

## Prerequisites

- Python 3.10+
- Node.js 18+
- MySQL
- Groq API Key (Optional)

---

## Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/ai-first-crm-hcp.git

cd ai-first-crm-hcp
```

---

# Backend Setup

Create a virtual environment

```bash
python -m venv venv
```

Activate it

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Configure `.env`

```env
GROQ_API_KEY=YOUR_GROQ_API_KEY

DATABASE_URL=mysql+pymysql://username:password@localhost:3306/crmdb
```

Seed the database

```bash
python -m app.seed
```

Run backend

```bash
uvicorn app.main:app --reload --port 8081
```

Backend

```
http://localhost:8081
```

Swagger Docs

```
http://localhost:8081/docs
```

---

# Frontend Setup

Navigate to frontend

```bash
cd frontend
```

Install dependencies

```bash
npm install
```

Run the development server

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
Tool Selection
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
| Get HCP Profile | Retrieves doctor profile and history |
| Log Interaction | Stores interaction details |
| Analyze Compliance | Performs compliance analysis |
| Generate Follow-up | Creates AI follow-up tasks and emails |
| Edit Interaction | Updates previous interactions |

---

# 🎯 Future Enhancements

- Voice Interaction
- Multi-Agent Workflow
- Role-Based Access Control
- Email Integration
- Calendar Integration
- Analytics Dashboard
- Cloud Deployment

---

# 👨‍💻 Author

**Suprith Kumar B L**

Computer Science & Engineering

**Skills**

- Python
- FastAPI
- React
- LangGraph
- LangChain
- AI Agents
- Full Stack Development

GitHub

https://github.com/SuprithKumarBL20

---

# ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub.

---

# 📄 License

This project is developed for educational and demonstration purposes.
