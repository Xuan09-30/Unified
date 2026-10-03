@echo off
echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment and installing dependencies...
call venv\Scripts\activate
pip install -r requirements.txt

echo Starting Docker containers...
docker-compose up -d

echo Setup complete! Activate your environment using: .\venv\Scripts\activate
pause