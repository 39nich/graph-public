# Temporarily allow script execution
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

# Activate venv
.\venv\Scripts\Activate.ps1

# Run Django dev server
python manage.py runserver
