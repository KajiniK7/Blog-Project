# 🖋️ LuxBlog — AI-Moderated Publishing Platform

A modern, full-stack Medium-style blogging platform built with **FastAPI**, **React (Vite)**, **Turso / libSQL / SQLite**, and real-time **Groq AI Content Moderation**. Features an obsidian-and-warm-gold luxury aesthetic, dark/light theme switching, live title search, draft-only edit workflows, user-scoped privacy, and interactive real-time story analytics charts.

---

## ✨ Features

- **🛡️ Real-Time Groq AI Moderation**: Automated post analysis to evaluate, approve, or flag articles based on safety and quality guidelines (length, profanity, and tone).
- **🔐 User Authentication**: Register and log in with persistent user accounts stored securely with PBKDF2 password hashing.
- **👤 Multi-User Ownership & Privacy**:
  - Each author owns and creates stories under their unique `@username`.
  - **Flagged and draft articles are private**: Only visible to the author who created them.
  - **Universal published articles**: Any article published by an author can be read by all platform visitors.
- **📊 Real-Time User Analytics Chart**: A dedicated visual widget beneath the sidebar guidelines providing a single proportional stacked bar chart and interactive metrics for the user's Drafts, Flagged, Approved, and Published stories with a live sync indicator.
- **🎨 Luxury Dark / Light Mode**: Obsidian & warm gold color palette inspired by high-end editorial magazines with an instant theme toggle.
- **🔍 Live Search**: Search and filter articles dynamically by title right from the top navigation bar.
- **📑 Status Filters**: Filter posts across 5 tabs: **For you**, **Published**, **Approved**, **Flagged**, and **Drafts**.
- **✏️ Strict Draft-Only Editing**: Edit options are strictly enabled only when an article is in `draft` status, locking down approved and published content.
- **⏱️ Timestamp & Author Tag**: Formatted creation date and time (`Oct 14 at 8:27 PM`) with personalized author attribution (`@username`).
- **☁️ Cloud & Local Database Support**: Plug-and-play support for remote **Turso libSQL cloud** or local **SQLite** (`posts.db`).

---

## 📋 Prerequisites

Ensure you have the following installed on your machine:

1. **Python 3.10+** — [Download Python](https://www.python.org/downloads/) *(Make sure to check "Add Python to PATH" during installation)*
2. **Node.js 18+ & npm** — [Download Node.js](https://nodejs.org/)
3. **Groq API Key** *(Optional for AI moderation)* — [Get an API Key](https://console.groq.com/)

---

## ⚡ Option 1: Quick 1-Click Setup & Launch (Windows)

If you are on Windows, you can use the pre-configured batch scripts:

### Step 1: Initial Setup
Double-click `setupdev.bat` or run it from the command line:
```cmd
setupdev.bat
```
*This automatically creates the Python virtual environment, installs backend dependencies and moderation SDK, executes database migrations, and installs frontend npm packages.*

### Step 2: Start the Application
Double-click `runapplication.bat` or run:
```cmd
runapplication.bat
```
*This opens both the FastAPI backend and React frontend in separate terminal windows.*

---

## 🛠️ Option 2: Manual Installation & Execution (Step-by-Step)

If you prefer to run each step manually or are on macOS/Linux:

### 1. Environment Configuration

Create a `.env` file in the root project directory:
```bash
# Copy example file
copy .env.example .env   # On Windows
# or: cp .env.example .env # On Linux/macOS
```

Open `.env` and fill in your keys:
```ini
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=openai/gpt-oss-safeguard-20b

# Optional: To connect to Turso Cloud (leave empty or omit to use local SQLite posts.db)
TURSO_DATABASE_URL=libsql://your-db-name.turso.io
TURSO_AUTH_TOKEN=your-turso-auth-token
```

---

### 2. Backend Setup & Run

1. **Open a terminal** and navigate to the project root:
   ```bash
   cd Blog
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv env
   ```

3. **Activate the virtual environment**:
   - **Windows (Command Prompt / PowerShell)**:
     ```cmd
     env\Scripts\activate
     ```
   - **Linux / macOS**:
     ```bash
     source env/bin/activate
     ```

4. **Install Python packages**:
   ```bash
   pip install -r requirements.txt
   pip install ./moderation_sdk
   ```

5. **Run Database Migrations**:
   ```bash
   alembic upgrade head
   ```

6. **Start the FastAPI Server**:
   ```bash
   python main.py
   ```
   *The backend will now be live at:* `http://localhost:8000`

---

### 3. Frontend Setup & Run

1. **Open a second terminal** and navigate to the `frontend` folder:
   ```bash
   cd Blog/frontend
   ```

2. **Install Node.js dependencies**:
   ```bash
   npm install
   ```

3. **Start the Vite development server**:
   ```bash
   npm start
   ```
   *(or `npm run dev`)*

   *The frontend will now be accessible at:* `http://localhost:3000`

---

## 🌐 Application URLs

| Service | URL | Description |
| :--- | :--- | :--- |
| **Frontend Application** | [http://localhost:3000](http://localhost:3000) | Main blog UI, reader view, analytics chart, and editor |
| **FastAPI Backend** | [http://localhost:8000](http://localhost:8000) | REST API server |
| **Interactive API Docs** | [http://localhost:8000/docs](http://localhost:8000/docs) | Swagger UI for testing API endpoints |
| **Alternative API Docs** | [http://localhost:8000/redoc](http://localhost:8000/redoc) | ReDoc API documentation |

---

## 📖 How to Use the Application

1. **Sign In / Register**:
   - When you first visit `http://localhost:3000`, click **Sign In** or **Get Started** in the top-right header or on the welcome card.
   - Switch to **Create account**, pick a username and password, and click **Create account**.
   - You are immediately logged in, and your username appears in the header.

2. **Write a Story**:
   - Click the **Write** button in the header.
   - Enter your title, content, and an optional image URL.
   - Stories are created with your `@username` attached as the author.
   - Choose **Save Draft** to store it privately, or **Submit for Review** to trigger the Groq AI moderation workflow.

3. **Multi-User Privacy Rules**:
   - **Drafts & Flagged Stories**: Strictly private. When user `alice` logs in, she only sees her own flagged or drafted stories. User `bob` will never see `alice`'s flagged content.
   - **Published Stories**: Fully public. Once an approved story is published, it appears on the global feed for everyone to read.

4. **Live User Story Analytics Chart**:
   - Located directly below the **Publishing Guidelines** in the right-hand sidebar.
   - View your own stories broken down across **Published**, **Approved**, **Draft**, and **Flagged** on a proportional horizontal chart.
   - Click any status card in the widget to filter your feed instantly.
   - Real-time updates poll automatically every 5 seconds with a live green indicator and sync timestamp.

5. **Edit a Draft**:
   - Go to the **Drafts** tab in the filter bar.
   - On any draft card, click the **✏️ Edit** button to load the article back into the composer.
   - *(Note: Once an article is Approved or Published, editing is locked to preserve moderation integrity).*

6. **Search Articles**:
   - Type in the **Search stories...** bar at the top to filter cards live by title.

7. **Toggle Theme**:
   - Click the **☀️ / 🌙** button in the top bar to toggle between obsidian luxury dark mode and clean paper light mode.

---

## 📂 Project Architecture

```
Blog/
├── alembic/                # Database migrations
├── app/                    # Backend application core
│   ├── auth_service.py     # Password hashing & user auth helpers
│   ├── crud.py             # Database CRUD queries & user privacy scoping
│   ├── database.py         # SQLAlchemy engine & Turso/libSQL connection
│   ├── main_app.py         # FastAPI application entry & CORS
│   ├── models.py           # Database models (Post, User)
│   ├── schemas.py          # Pydantic validation schemas
│   └── routers/            # API endpoints (posts, auth, moderation)
├── frontend/               # React + Vite frontend
│   ├── src/
│   │   ├── components/     # UI components (PostCard, UserPostAnalytics, AuthModal, etc.)
│   │   ├── App.jsx         # Main application container & state
│   │   └── index.css       # Luxury Obsidian theme & chart styles
│   ├── package.json        # Frontend dependencies
│   └── vite.config.js      # Vite build configuration
├── moderation_sdk/         # Groq AI moderation client package
├── runapplication.bat      # 1-Click launcher script for Windows
├── setupdev.bat            # 1-Click setup script for Windows
├── requirements.txt        # Python package dependencies
└── README.md               # Project documentation
```

---

## 🧪 Testing & Verification

To run backend test suites:
```bash
# Make sure the virtual environment is activated
pytest
```
To run targeted privacy & author scoping tests:
```bash
pytest -k "privacy or author"
```
To run Groq connection smoke tests:
```bash
python groq_smoke.py
```
