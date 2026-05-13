# IAFIT

## Backend

Usa Python 3.11 o superior. Django 6 requiere Python 3.12, por eso el proyecto usa Django 5.2 LTS para que sea más fácil instalarlo en AWS y en los equipos del grupo.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
cd Backend
python manage.py runserver 0.0.0.0:8001
```

En Windows:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
cd Backend
python manage.py runserver 0.0.0.0:8001
```

## Frontend

```bash
cd Frontend/frontend-rag
npm ci
npm start
```
