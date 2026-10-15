BlogHub — AI-Moderated Publishing Platform
BlogHub is a full-stack blogging platform inspired by Medium. It is built using FastAPI, React (Vite), and Turso/libSQL or SQLite, with Groq AI for content moderation. Users can write and publish articles, save drafts, search stories, switch between dark and light themes, and view analytics about their posts.

✨ Features
- AI Content Moderation: Uses Groq AI to review submitted articles based on content length, profanity, tone, and safety guidelines.
- User Authentication: Users can register and log in. Passwords are stored securely using PBKDF2 hashing.
- User Privacy: Each author can manage their own stories. Drafts and flagged articles are private, while published articles are visible to everyone.
- Story Analytics: Displays the user's Draft, Flagged, Approved, and Published stories in a chart that updates automatically.
- Dark and Light Mode: Users can switch between a dark obsidian-and-gold theme and a light theme.
- Live Search: Search for articles by title using the search bar.
- Post Filters: Browse articles using the For You, Published, Approved, Flagged, and Drafts tabs.
- Draft Editing: Articles can be edited only while they are in draft status.
- Author and Timestamp: Each article displays the author's username and its creation date and time.
- Database Support: Supports both a cloud-based Turso/libSQL database and a local SQLite database.

📋 Prerequisites
Before running the project, make sure you have installed the following:
1. Python 3.10 or later: Download Python
2. Node.js 18 or later and npm: Download Node.js
3. Groq API key: Get an API key — optional if you do not want to configure AI moderation.

⚡ Option 1: Quick Setup on Windows
The project includes batch scripts to simplify installation and execution.
Step 1: Install dependencies
Double-click setupdev.bat or run the following command from the project directory:
setupdev.bat


This script creates the Python virtual environment, installs the backend dependencies and moderation SDK, runs database migrations, and installs the frontend packages.
Step 2: Start the application
Double-click runapplication.bat or run:
runapplication.bat


This starts the FastAPI backend and React frontend in separate terminal windows.

🛠️ Option 2: Manual Installation
Use these steps if you prefer to start the backend and frontend separately or are using macOS or Linux.
1. Configure environment variables
Create a .env file in the root project directory.
On Windows:
copy .env.example .env


On Linux or macOS:
cp .env.example .env


Open the .env file and add your configuration:
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=openai/gpt-oss-safeguard-20b

# Optional: Turso cloud database configuration
TURSO_DATABASE_URL=libsql://your-db-name.turso.io
TURSO_AUTH_TOKEN=your-turso-auth-token


If you want to use the local SQLite database, you can leave the Turso settings empty or omit them.
2. Set up and run the backend
Open a terminal in the project directory:
cd Blog


Create a Python virtual environment:
python -m venv env


Activate the environment.
On Windows:
env\Scripts\activate


On Linux or macOS:
source env/bin/activate


Install the required packages:
pip install -r requirements.txt
pip install ./moderation_sdk


Run the database migrations:
alembic upgrade head


Start the FastAPI server:
python main.py


The backend will be available at http://localhost:8000.
3. Set up and run the frontend
Open a second terminal and navigate to the frontend directory:
cd Blog/frontend


Install the frontend dependencies:
npm install


Start the Vite development server:
npm start


Alternatively, use:
npm run dev


The frontend will be available at http://localhost:3000.

🌐 Application URLs
Service	URL	Purpose
Frontend	http://localhost:3000	Main blogging interface
Backend	http://localhost:8000	FastAPI server
Swagger API Docs	http://localhost:8000/docs	Test API endpoints
ReDoc API Docs	http://localhost:8000/redoc	View API documentation

📖 How to Use the Application
1. Register or sign in
Open http://localhost:3000 and click Sign In or Get Started. Choose the account creation option, enter a username and password, and create your account. After registration, you will be logged in and your username will appear in the header.
2. Write a story
Click the Write button in the header. Enter your article title, content, and an optional image URL.
You can choose between two options:
- Save Draft: Saves the article privately so you can continue working on it later.
- Submit for Review: Sends the article through the Groq AI moderation workflow.
Each article is associated with the username of its author.
3. Understand the privacy rules
Drafts and flagged articles are visible only to their authors. For example, if Alice creates a draft, Bob cannot see it from his account.
Once an article is approved and published, it becomes available for everyone to read through the public feed.
4. View story analytics
The analytics chart is located below the publishing guidelines in the right-hand sidebar.
It displays the number of your stories in four categories:
- Published
- Approved
- Draft
- Flagged
Click a status card to filter the feed by that category. The chart refreshes automatically every five seconds and displays a sync indicator and timestamp.
5. Edit a draft
Open the Drafts tab and click the Edit button on the article you want to update. The article will reopen in the editor.
Editing is disabled for approved and published articles to maintain the moderation workflow.
6. Search for articles
Use the Search stories... field in the top navigation bar to filter articles by title.
7. Change the theme
Click the sun or moon button in the top bar to switch between dark and light mode.

📂 Project Structure
The project is organized into separate backend, frontend, database migration, and moderation modules.
Blog/
├── alembic/                    # Database migrations
├── app/                        # Backend application
│   ├── auth_service.py         # Password hashing and authentication
│   ├── crud.py                 # Database operations and privacy rules
│   ├── database.py             # Database connection and configuration
│   ├── main_app.py             # FastAPI application and CORS
│   ├── models.py               # User and Post database models
│   ├── schemas.py              # Pydantic validation schemas
│   └── routers/                # Post, authentication, and moderation APIs
├── frontend/                   # React and Vite frontend
│   ├── src/
│   │   ├── components/         # Reusable UI components
│   │   ├── App.jsx             # Main application and state
│   │   └── index.css           # Theme and chart styling
│   ├── package.json            # Frontend dependencies
│   └── vite.config.js          # Vite configuration
├── moderation_sdk/             # Groq AI moderation client
├── runapplication.bat          # Starts the application on Windows
├── setupdev.bat                # Installs project dependencies
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation



🧪 Testing
To run the backend test suite, activate the Python virtual environment and execute:
pytest


To run tests related to privacy and author-specific access:
pytest -k "privacy or author"


To check the Groq API connection:
python groq_smoke.py


These commands help verify the backend functionality, privacy rules, and Groq integration.

📝 Project Summary
BlogHub is a full-stack blogging application that combines article publishing with AI-based content moderation. It allows users to create accounts, write stories, manage drafts, and publish approved content while keeping private articles accessible only to their authors. With its React interface, FastAPI backend, database options, and story analytics, the project brings together content management, privacy, and AI moderation in one application.