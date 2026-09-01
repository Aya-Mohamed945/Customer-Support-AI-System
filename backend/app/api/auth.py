# app/api/auth.py
"""
Authentication API Routes
"""

import hashlib
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.core.dependencies import (  # ✅ أضيفي get_current_user
    create_access_token,
    get_current_user,
    load_users,
    save_users,
)

router = APIRouter()


class SignupRequest(BaseModel):
    name: str
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/signup")
async def signup(request: SignupRequest):
    """Register a new user"""
    users = load_users()

    if request.email in users:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed = hashlib.sha256(request.password.encode()).hexdigest()
    is_admin = len(users) == 0

    users[request.email] = {
        "name": request.name,
        "email": request.email,
        "password": hashed,
        "role": "admin" if is_admin else "user",
        "created_at": datetime.now().isoformat(),
    }

    save_users(users)
    return {"message": "User created successfully", "role": "admin" if is_admin else "user"}


@router.post("/login")
async def login(request: LoginRequest):
    """Login and return JWT token"""
    users = load_users()

    if request.email not in users:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    hashed = hashlib.sha256(request.password.encode()).hexdigest()
    if users[request.email]["password"] != hashed:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(
        {"sub": request.email, "email": request.email, "role": users[request.email].get("role", "user")}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",  # nosec B105
        "user": {
            "name": users[request.email]["name"],
            "email": request.email,
            "role": users[request.email].get("role", "user"),
        },
    }


@router.get("/me")
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """Get current authenticated user info"""
    users = load_users()
    email = current_user.get("email")
    if email not in users:
        raise HTTPException(status_code=404, detail="User not found")

    return {"name": users[email]["name"], "email": email, "role": users[email].get("role", "user")}
