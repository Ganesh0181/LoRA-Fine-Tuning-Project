from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from model.inference import predict_tool_call
from api.auth import (
    init_auth_db,
    create_user,
    authenticate_user,
    create_token,
    verify_token
)

app = FastAPI(title="AI Tool Orchestrator API")

init_auth_db()


class SignupRequest(BaseModel):
    username: str
    password: str
    role: str = "user"


class LoginRequest(BaseModel):
    username: str
    password: str


class ToolRequest(BaseModel):
    user_input: str


@app.get("/")
def home():
    return {
        "status": "success",
        "message": "AI Tool Orchestrator API running"
    }


@app.post("/signup")
def signup(request: SignupRequest):
    success, message = create_user(
        username=request.username,
        password=request.password,
        role=request.role
    )

    if not success:
        raise HTTPException(status_code=400, detail=message)

    return {
        "status": "success",
        "message": message
    }


@app.post("/login")
def login(request: LoginRequest):
    user = authenticate_user(request.username, request.password)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = create_token(user)

    return {
        "access_token": token,
        "token_type": "bearer",
        "username": user["username"],
        "role": user["role"]
    }


def require_auth(authorization: str):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing token")

    token = authorization.replace("Bearer ", "").strip()
    payload = verify_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return payload


@app.post("/predict")
def predict(request: ToolRequest, authorization: str = Header(default=None)):
    user = require_auth(authorization)

    result = predict_tool_call(request.user_input)

    result["auth_user"] = {
        "username": user["sub"],
        "role": user["role"]
    }

    return result