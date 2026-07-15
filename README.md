# AI-First CRM HCP Module – Log Interaction Screen

This project is a high-fidelity prototype of an **AI-First Customer Relationship Management (CRM) system** designed specifically for the **Healthcare Professional (HCP) module** in Life Sciences. It enables pharmaceutical sales representatives to seamlessly log and audit interactions with clinicians.

The application offers representatives the flexibility to record interactions through either a **structured, manual data-entry form** or a **conversational AI agent interface**—both backed by a live **PhRMA guideline compliance checking engine**.

---

## Key Features

1. **Dual Logging Modes**:
   - **Conversational AI Logger**: A chat panel where field representatives talk to the CRM AI assistant naturally (e.g., *"I met Dr. Jenkins today about Zyntra..."*). The agent extracts details in real-time, displaying them in a live-synced side form.
   - **Structured Form Logger**: A traditional input form for manual entries, with a button to pre-run AI compliance scans on notes prior to saving.

2. **LangGraph Agent & The 5 Sales-Related Tools**:
   An agentic workflow orchestrates five specialized tools to handle the CRM data pipeline:
   - **`log_interaction`** (Mandatory): Takes extracted/form parameters (HCP ID, date, channel, notes, topics) and saves them in the database, automatically analyzing sentiment, creating follow-ups, and adding compliance audit logs.
   - **`edit_interaction`** (Mandatory): Modifies previously logged interactions. Updates to notes or summaries re-trigger compliance checks to ensure ongoing compliance.
   - **`get_hcp_profile`**: Resolves doctor details, specializations, contact preferences, and retrieves a list of past interaction summaries.
   - **`analyze_compliance`**: Performs real-time audit on conversation notes against industry **PhRMA guidelines** (flagging travel offers, cash/gift incentives, and off-label product promotions).
   - **`generate_follow_up`**: Schedules follow-up tasks and produces a personalized draft email template referencing discussed topics.

3. **Database Integration**: Fully modeled via SQLAlchemy. Configured for SQLite locally for lightweight execution, but ready to map directly to PostgreSQL or MySQL by setting the `DATABASE_URL` environment variable.

4. **Premium Obsidian/Glassmorphic Design**: Built using Google Inter typography, dynamic glow effects, smooth CSS hover transitions, and dark modes to ensure a modern, state-of-the-art interface.

---

## Tech Stack

*   **Frontend**: React (Vite), Redux Toolkit (State Management), Lucide Icons, Vanilla CSS
*   **Backend**: Python, FastAPI, SQLAlchemy
*   **Agentic AI**: LangGraph, LangChain, Groq API (Default model: `gemma2-9b-it`)
*   **Database**: SQLite (default) / MySQL / PostgreSQL

---

## Project Structure

```text
ai-first-crm-hcp/
├── backend/
│   ├── app/
│   │   ├── agent/
│   │   │   ├── __init__.py
│   │   │   ├── graph.py       # LangGraph state machine workflow
│   │   │   ├── llm.py         # Groq LLM setup (with mock fallback)
│   │   │   └── tools.py       # The 5 custom sales agent tools
│   │   ├── __init__.py
│   │   ├── database.py        # SQLAlchemy engine & session configurations
│   │   ├── main.py            # FastAPI endpoints & startup events
│   │   ├── models.py          # SQLAlchemy schemas (HCP, Interaction, Product, FollowUp, Compliance)
│   │   ├── schemas.py         # Pydantic validation schemas
│   │   └── seed.py            # Pre-populates database with mock doctors & products
│   ├── .env.example
│   ├── .env                   # Configuration file (API keys, DB settings)
│   └── requirements.txt       # Python backend dependencies
└── frontend/
    ├── src/
    │   ├── components/
    │   │   ├── ChatInterface.jsx         # Conversational agent UI with live state cards
    │   │   ├── FollowUpPanel.jsx         # AI email templates and follow-ups dashboard
    │   │   ├── HistoryPanel.jsx          # Audited logs history list and edit dialog
    │   │   ├── HcpSelector.jsx           # Sidebar listing HCPs and detail card
    │   │   └── Navbar.jsx                # Header and DB seeding controls
    │   ├── store/
    │   │   ├── index.js                  # Redux store setup
    │   │   └── slices.js                 # Redux state slices & async API thunks
    │   ├── App.jsx                       # Main view switching container
    │   ├── index.css                     # Premium obsidian stylesheet
    │   └── main.jsx                      # React entrypoint
    ├── index.html
    ├── vite.config.js
    └── package.json
```

---

## How to Run Locally

### Prerequisite Checklist
*   Python 3.8+
*   Node.js v16+
*   Groq API Key (Optional: The application automatically triggers a high-fidelity **Mock LLM Fallback** if no API key is set, making the entire project runnable out-of-the-box!)

### Step 1: Run the Backend API

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure environment variables. Rename `.env.example` to `.env` or create it:
   ```env
   GROQ_API_KEY=YOUR_GROQ_API_KEY_HERE
   DATABASE_URL=mysql+pymysql://root:root%40123@127.0.0.1:3306/crmdb
   ```
   *(Note: Ensure password special characters are URL-encoded. E.g. `@` as `%40`).*
5. Seed the database with mock records (HCPs, pharmaceutical products, history):
   ```bash
   python -m app.seed
   ```
6. Start the FastAPI server:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```
   The API will be available at `http://localhost:8000`. You can inspect documentation at `http://localhost:8000/docs`.

### Step 2: Run the Frontend UI

1. Navigate to the frontend directory:
   ```bash
   cd ../frontend
   ```
2. Install npm dependencies:
   ```bash
   npm install
   ```
3. Launch the Vite dev server:
   ```bash
   npm run dev
   ```
4. Open your browser and navigate to the local URL (usually `http://localhost:3000`).

---

## Demonstration Walkthrough (For Recording)

When presenting the 10-15 minute video demo, you can showcase these scenarios:

1.  **HCP Profile Retrieval (`get_hcp_profile`)**:
    Select **Dr. Sarah Jenkins** on the left panel. View the card displaying her specialization, clinic, preferences, and the AI-calculated *Next Best Action*.
2.  **Conversational Logging (`log_interaction`)**:
    Switch to **Conversational AI Logger**. Click the quick prompt button: *"Log Zyntra meeting today..."* or type:
    > *"Log an in-person meeting with Dr. Jenkins today about Zyntra. She was excited and wants the clinical brochures."*
    Observe the AI processing the text, executing the graph, and populating the **Live Extraction State** sidebar card with structured fields in real-time.
3.  **Real-Time PhRMA Compliance Audit (`analyze_compliance`)**:
    Type a non-compliant prompt in the chat:
    > *"Check compliance: I promised Dr. Chen a sponsored trip to Hawaii to cover flights and resort lodging."*
    Watch the agent evaluate the text and flag it in red as **Non-Compliant**, identifying the specific PhRMA travel violation.
4.  **Follow-up Scheduling & Email Scripts (`generate_follow_up`)**:
    Review the **Follow-up Tasks** list. Expand Dr. Jenkins' card to inspect the AI-generated email script. You can edit the text and click **Dispatch Email Draft** to trigger a mock transmission.
5.  **Audit History & Records Editing (`edit_interaction`)**:
    Go to **Logged Interactions History**. Click **Edit** on a log, change the meeting text, and save. The backend runs the edit tool and updates the database, dynamically re-checking PhRMA compliance.
#   A I - P o w e r e d - H e a l t h c a r e - C R M - S y s t e m  
 