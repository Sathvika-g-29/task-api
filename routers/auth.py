from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from supabase_client import supabase

router = APIRouter(prefix="/auth", tags=["Authentication"])


class AuthRequest(BaseModel):
    email: str
    password: str


@router.post("/signup", status_code=201)
def signup(request: AuthRequest):
    if not request.email.strip() or not request.password.strip():
        raise HTTPException(
            status_code=400,
            detail="Email and password are required"
        )

    try:
        response = supabase.auth.sign_up(
            {
                "email": request.email,
                "password": request.password
            }
        )

        return {
            "message": "Signup successful",
            "user": response.user
        }

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.post("/login")
def login(request: AuthRequest):
    if not request.email.strip() or not request.password.strip():
        raise HTTPException(
            status_code=400,
            detail="Email and password are required"
        )

    try:
        response = supabase.auth.sign_in_with_password(
            {
                "email": request.email,
                "password": request.password
            }
        )

        if response.session is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid credentials"
            )

        return {
            "access_token": response.session.access_token,
            "refresh_token": response.session.refresh_token
        }

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )