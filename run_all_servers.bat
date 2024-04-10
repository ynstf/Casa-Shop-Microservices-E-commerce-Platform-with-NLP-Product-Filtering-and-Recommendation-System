@echo off

REM Start Django servers
start cmd /k "venv\Scripts\activate && python EcommerceAI\manage.py runserver"
start cmd /k "venv\Scripts\activate && python product\manage.py runserver 5555"
start cmd /k "venv\Scripts\activate && python django-auth\manage.py runserver 7777"
start cmd /k "venv\Scripts\activate && python policy\manage.py runserver 9999"

REM Start Flask servers
start cmd /k "venv\Scripts\activate && python search-category\server.py"
start cmd /k "venv\Scripts\activate && python search-products\server.py"
start cmd /k "venv\Scripts\activate && python similarity-model\server.py"

REM Start FastAPI server
start cmd /k "venv\Scripts\activate && cd Product-classification-policy && uvicorn app:app --host 0.0.0.0 --port 1111"
