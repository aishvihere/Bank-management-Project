from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional

from improved import Bank

# ---------- INITIAL SETUP ----------
bank = Bank()

app = FastAPI(
    title="Bank Management System API",
    description="REST API for basic banking operations: create, view, deposit, withdraw, update and delete accounts.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------- SCHEMAS ----------
class AccountCreate(BaseModel):
    name: str
    age: int = Field(ge=0)
    email: str
    pin: int = Field(ge=1000, le=9999)


class AccountDetails(BaseModel):
    name: str
    age: int
    email: str
    account_no: str
    balance: int


class AuthRequest(BaseModel):
    account_no: str
    pin: int


class PinRequest(BaseModel):
    pin: int


class AmountRequest(BaseModel):
    pin: int
    amount: int = Field(gt=0)


class UpdateRequest(BaseModel):
    pin: int
    name: Optional[str] = None
    email: Optional[str] = None
    new_pin: Optional[int] = Field(default=None, ge=1000, le=9999)


class MessageResponse(BaseModel):
    message: str


# ---------- HELPERS ----------
def get_authenticated_user(account_no: str, pin: int):
    user = bank.authenticate(account_no, pin)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid account number or PIN",
        )
    return user


# ---------- ROUTES ----------
@app.get("/", tags=["health"])
def health_check():
    return {"status": "ok", "service": "Bank Management System API"}


@app.post(
    "/accounts",
    response_model=AccountDetails,
    status_code=status.HTTP_201_CREATED,
    tags=["accounts"],
)
def create_account(payload: AccountCreate):
    success, result = bank.create_account(
        payload.name, payload.age, payload.email, payload.pin
    )
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result)
    return result


@app.post("/accounts/view", response_model=AccountDetails, tags=["accounts"])
def view_account(payload: AuthRequest):
    return get_authenticated_user(payload.account_no, payload.pin)


@app.post(
    "/accounts/{account_no}/deposit", response_model=AccountDetails, tags=["transactions"]
)
def deposit(account_no: str, payload: AmountRequest):
    user = get_authenticated_user(account_no, payload.pin)
    success, msg = bank.deposit(user, payload.amount)
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=msg)
    return user


@app.post(
    "/accounts/{account_no}/withdraw", response_model=AccountDetails, tags=["transactions"]
)
def withdraw(account_no: str, payload: AmountRequest):
    user = get_authenticated_user(account_no, payload.pin)
    success, msg = bank.withdraw(user, payload.amount)
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=msg)
    return user


@app.patch(
    "/accounts/{account_no}", response_model=AccountDetails, tags=["accounts"]
)
def update_account(account_no: str, payload: UpdateRequest):
    user = get_authenticated_user(account_no, payload.pin)
    success, result = bank.update_details(
        user,
        name=payload.name or None,
        email=payload.email or None,
        pin=payload.new_pin or None,
    )
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result)
    return result["new"]


@app.delete(
    "/accounts/{account_no}", response_model=MessageResponse, tags=["accounts"]
)
def delete_account(account_no: str, payload: PinRequest):
    user = get_authenticated_user(account_no, payload.pin)
    bank.delete_account(user)
    return {"message": "Account deleted successfully"}
