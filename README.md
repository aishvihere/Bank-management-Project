# Bank-management-Project 
1. The Bank Management Project is a Python-based REST API designed to simulate basic banking operations in a secure and user-friendly manner.
2. The project allows clients to create and manage bank accounts through a REST API built using FastAPI. It implements core banking functionalities such as account creation, authentication, deposits, withdrawals, account updates, and account deletion.
3. The backend logic is developed using Object-Oriented Programming (OOPS) principles to ensure modularity, reusability, and data encapsulation.
4. Persistent data storage is handled using JSON-based file handling, acting as a lightweight database. The application enforces validation rules such as age limits, PIN verification, transaction limits, and balance checks to maintain data integrity and security.
5. The project demonstrates a complete CRUD-based banking workflow exposed as a REST API, with interactive docs (Swagger UI / ReDoc) generated automatically by FastAPI.
6. Technologies Used
--Python
--FastAPI (REST API & Deployment)
--Uvicorn (ASGI server)
--JSON (File-based Database)
--OOPS Concepts
--File Handling
--Shallow & Deep Copy
--GitHub

## Running locally

```bash
pip install -r requirements.txt
uvicorn app:app --reload
```

The API will be available at `http://127.0.0.1:8000`, with interactive docs at
`http://127.0.0.1:8000/docs` (Swagger UI) and `http://127.0.0.1:8000/redoc` (ReDoc).

## API Endpoints

| Method | Endpoint                      | Description                              |
|--------|--------------------------------|-------------------------------------------|
| GET    | `/`                            | Health check                              |
| POST   | `/accounts`                    | Create a new account                      |
| POST   | `/accounts/view`               | View account details (requires PIN)       |
| POST   | `/accounts/{account_no}/deposit`  | Deposit money into an account          |
| POST   | `/accounts/{account_no}/withdraw` | Withdraw money from an account         |
| PATCH  | `/accounts/{account_no}`       | Update name/email/PIN                     |
| DELETE | `/accounts/{account_no}`       | Delete an account                         |

## Deployment

Any ASGI-compatible host works (Render, Railway, Fly.io, Heroku-style platforms, etc.).
A `Procfile` is included for Heroku-style platforms:

```
web: uvicorn app:app --host 0.0.0.0 --port $PORT
```

