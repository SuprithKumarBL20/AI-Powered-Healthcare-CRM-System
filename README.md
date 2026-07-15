# 🚀 AI-First CRM for Healthcare Professionals (HCP)

An **AI-powered Customer Relationship Management (CRM)** platform built for pharmaceutical sales representatives to efficiently manage interactions with **Healthcare Professionals (HCPs)**.

The application leverages **FastAPI**, **React**, **LangGraph**, **LangChain**, and **Groq LLM** to automate interaction logging, AI-assisted conversations, compliance analysis, follow-up generation, and HCP profile management.

---

# 📸 Application Preview

> Store all screenshots inside:

```
docs/screenshots/
```

### Dashboard

![Dashboard](docs/screenshots/dashboard.png)

### AI Chat Assistant

![Chat](docs/screenshots/chat-interface.png)

### HCP Profile

![HCP Profile](docs/screenshots/hcp-profile.png)

### Interaction History

![History](docs/screenshots/interaction-history.png)

### Edit Interaction

![Edit](docs/screenshots/edit-interaction.png)

### Follow-up Panel

![Follow Up](docs/screenshots/follow-up-panel.png)

---

# ✨ Features

## 🤖 AI CRM Assistant

- AI-powered conversational interface
- Natural language interaction logging
- Intelligent meeting detail extraction
- LangGraph-based tool-calling workflow
- Automatic form population

---

## 👨‍⚕️ HCP Management

- View Healthcare Professional profiles
- Access previous interaction history
- Maintain doctor information
- Track communication preferences
- View AI-generated next best action

---

## 📋 Interaction Management

- Log new interactions
- Edit previous interactions
- Track meeting summaries
- Store discussion topics
- Manage communication channels

---

## ✅ Compliance Analysis

- Real-time compliance verification
- Detect risky conversations
- Highlight policy violations
- Review discussion topics
- Generate compliance recommendations

---

## 📧 Follow-up Generation

- AI-generated follow-up tasks
- Personalized email drafts
- Reminder scheduling
- Next-step recommendations

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
          ┌────────────────┴────────────────┐
          │                                 │
          ▼                                 ▼
    LangGraph Agent                 SQLAlchemy ORM
          │                                 │
          ▼                                 ▼
   LangChain + Groq LLM                  MySQL
          │
          ▼
      AI Tool Execution
```

---

# 🛠️ Tech Stack

## Frontend

- React
- Vite
- JavaScript
- CSS
- Axios

### Backend

- Python
- FastAPI
- SQLAlchemy
- Pydantic

### AI Framework

- LangGraph
- LangChain
- Groq API
- Tool Calling Agent

### Database

- MySQL

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
│       ├── dashboard.png
│       ├── chat-interface.png
│       ├── hcp-profile.png
│       ├── interaction-history.png
│       ├── edit-interaction.png
│       └── follow-up-panel.png
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
- Groq API Key *(optional)*

---

# Backend Setup

Navigate to the backend directory:

```bash
cd backend
```

### Create a Virtual Environment

```bash
python -m venv venv
```

### Activate the Virtual Environment

**Windows**

```bash
venv\Scripts\activate
```

**Linux/macOS**

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

Create a `.env` file inside the `backend` directory.

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

### Start the Backend Server

```bash
uvicorn app.main:app --reload --port 8081
```

Backend API

```
http://localhost:8081
```

Swagger Documentation

```
http://localhost:8081/docs
```

---

# Frontend Setup

Navigate to the frontend folder.

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
User Request
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
      │
      ├────────► Log Interaction
      │
      ├────────► Analyze Compliance
      │
      ├────────► Generate Follow-up
      │
      └────────► Edit Interaction
```

---

# 🧰 AI Tools

| Tool | Purpose |
|------|---------|
| **Get HCP Profile** | Retrieves doctor information and interaction history |
| **Log Interaction** | Records meetings and discussion details |
| **Analyze Compliance** | Checks interactions against compliance rules |
| **Generate Follow-up** | Creates AI-powered follow-up tasks and email drafts |
| **Edit Interaction** | Updates previously logged interactions |

---

# 📦 API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | `/docs` | Swagger API Documentation |
| POST | `/api/chat` | AI Chat Assistant |
| GET | `/api/hcp` | Retrieve HCP Details |
| POST | `/api/interactions` | Create New Interaction |
| PUT | `/api/interactions/{id}` | Update Existing Interaction |

---

# 🎯 Future Enhancements

- 🎤 Voice-based interaction logging
- 🔐 User authentication & authorization
- 👥 Role-based access control
- 📊 Analytics dashboard
- 📄 PDF report generation
- 📅 Calendar scheduling
- 📧 Email integration
- ☁️ Cloud deployment
- 🤖 Multi-agent workflow

---

# 👨‍💻 Author

**Suprith Kumar B L**

Computer Science & Engineering

**Skills:** AI • LangGraph • LangChain • FastAPI • React • Python • Full Stack Development

GitHub: **https://github.com/SuprithKumarBL20**

---

# 📄 License

This project is developed for educational, research, and demonstration purposes.
