@echo off
echo Starting backend...
start "Backend" cmd /k "call env\Scripts\activate && python main.py"

timeout /t 4 /nobreak >nul

echo Starting frontend...
start "Frontend" cmd /k "cd frontend && npm start"

echo.
echo Backend:   http://localhost:8000
echo Swagger:   http://localhost:8000/docs
echo Frontend:  http://localhost:3000