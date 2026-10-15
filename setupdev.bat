@echo off
echo ===== Checking prerequisites =====
where python >nul 2>nul || (echo ERROR: Python is not installed or not on PATH. & exit /b 1)
where node >nul 2>nul || (echo ERROR: Node.js is not installed or not on PATH. & exit /b 1)

echo ===== Setting up backend =====
python -m venv env
call env\Scripts\activate
pip install -r requirements.txt
pip install .\moderation_sdk
alembic upgrade head

echo ===== Setting up frontend =====
cd frontend
call npm install
cd ..

echo Setup complete.