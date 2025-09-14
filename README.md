# SIMPLE CHAT AI

## Frontend
VueJs + Vite + Axios

## Backend
FastAPI + SqlAlchemy + Alembic + OpenAI

## Installation
Clone the repository.
### Frontend
Install all packages
```
npm i
```
Run:
```
npm run dev
```
### Backend
Init venv in backend folder:
```
python3 -m venv .venv
```
Install packages:
```
pip install -r requirements
```
Fill out the .env config:
```
DB_HOST=""
DB_PORT=
DB_NAME=""
DB_USER=""
DB_PASSWORD=""
SECRET_KEY=""
OPEN_AI_API_KEY=""
```
Run the server:
```
uvicorn app.main:app --reload
```
