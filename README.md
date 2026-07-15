# 🚀 AI-First CRM for Healthcare Professionals (HCP)

An AI-powered Customer Relationship Management (CRM) platform designed for pharmaceutical sales representatives to efficiently manage Healthcare Professional (HCP) interactions.

The application combines **FastAPI**, **React**, **LangGraph**, **LangChain**, and **Groq LLM** to automate interaction logging, compliance analysis, follow-up generation, and HCP profile management.

---

# ✨ Features

## 🤖 AI CRM Assistant
- Natural language interaction logging
- AI-powered conversation assistant
- Intelligent extraction of meeting details
- Tool-calling agent using LangGraph

## 👨‍⚕️ HCP Management
- View Healthcare Professional profiles
- Maintain interaction history
- Update existing interactions
- Track communication channels

## 📋 Interaction Management
- Log meetings
- Edit previous interactions
- View interaction history
- Store meeting summaries

## ✅ Compliance Analysis
- Detect potential compliance violations
- Review discussion topics
- Generate compliance recommendations
- Highlight risky conversations

## 📧 Follow-up Generation
- AI-generated follow-up tasks
- Email draft generation
- Action recommendations
- Next-step planning

---

# 🏗️ Project Architecture

```
                React Frontend
                      │
                      │ REST API
                      ▼
              FastAPI Backend
                      │
          ┌───────────┴───────────┐
          │                       │
          ▼                       ▼
      LangGraph Agent       SQLAlchemy ORM
          │                       │
          ▼                       ▼
     LangChain + Groq          MySQL
          │
          ▼
      Tool Execution
```

---

# 🛠️ Tech Stack

## Frontend

- React
- Vite
- JavaScript
- CSS
- Axios

## Backend

- FastAPI
- Python
- SQLAlchemy
- Pydantic

## AI

- LangGraph
- LangChain
- Groq LLM
- Tool Calling Agent

## Database

- MySQL

---

# 📂 Project Structure

```
ai-first-crm-hcp
│
├── backend
│   ├── app
│   │   ├── agent
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
├── frontend
│
├── docs
│   └── screenshots
│
└── README.md
```

---

# 📸 Screenshots

## Dashboard

![Dashboard](docs/screenshots/dashboard.png)

---

## AI Chat Assistant

![Chat](docs/screenshots/chat-interface.png)

---

## HCP Profile

![HCP Profile](docs/screenshots/hcp-profile.png)

---

## Interaction History

![History](docs/screenshots/interaction-history.png)

---

## Edit Interaction

![Edit](docs/screenshots/edit-interaction.png)

---

## Follow-up Panel

![Follow Up](docs/screenshots/follow-up-panel.png)

---

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/yourusername/ai-first-crm-hcp.git

cd ai-first-crm-hcp
```

---

# Backend Setup

## Create Virtual Environment

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment Variables

Create a `.env` file inside the backend directory.

```env
GROQ_API_KEY=YOUR_GROQ_API_KEY

DATABASE_URL=mysql+pymysql://username:password@localhost:3306/crmdb
```

---

## Start Backend

```bash
uvicorn app.main:app --reload --port 8081
```

Backend runs at

```
http://localhost:8081
```

Swagger Docs

```
http://localhost:8081/docs
```

---

# Frontend Setup

```bash
cd frontend

npm install

npm run dev
```

Frontend runs at

```
http://localhost:3000
```

---

# 🤖 AI Agent Workflow

```
User Message
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
      ├──────────────► Get HCP Profile
      │
      ├──────────────► Log Interaction
      │
      ├──────────────► Compliance Check
      │
      ├──────────────► Generate Follow-up
      │
      └──────────────► Edit Interaction
```

---

# 🧰 Available AI Tools

| Tool | Description |
|------|-------------|
| Get HCP Profile | Retrieves doctor information |
| Log Interaction | Stores meeting details |
| Analyze Compliance | Checks compliance rules |
| Generate Follow-up | Creates tasks and emails |
| Edit Interaction | Updates previous records |

---

# 📦 API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | /docs | Swagger Documentation |
| POST | /api/chat | AI Chat |
| GET | /api/hcp | HCP Details |
| POST | /api/interactions | Create Interaction |
| PUT | /api/interactions/{id} | Update Interaction |

---

# 🎯 Future Enhancements

- Voice interaction
- Multi-user authentication
- Role-based access control
- Analytics dashboard
- PDF report generation
- Email integration
- Calendar scheduling
- Cloud deployment

---

# 👨‍💻 Author

**Suprith Kumar B L**

Computer Science & Engineering

AI • Full Stack Development • LangGraph • FastAPI • React • Python

---

# 📄 License

This project is developed for educational and demonstration purposes.
