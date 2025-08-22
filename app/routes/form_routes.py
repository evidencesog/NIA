from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from fastapi import APIRouter, Form, File, UploadFile
import os
from starlette.status import HTTP_303_SEE_OTHER
import random
import hashlib
import sqlite3

router = APIRouter()


# Base dir is project root (~/fast)
BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR / "uploads"
IDCARD_DIR = UPLOAD_DIR / "id_card"
SSN_DIR = UPLOAD_DIR / "ssn"

DB_PATH = os.path.join(BASE_DIR, "database", "users.db")

# make sure dirs exist
os.makedirs(IDCARD_DIR, exist_ok=True)
os.makedirs(SSN_DIR, exist_ok=True)

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Login page
@router.get("/login")
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})
    

@router.post("/login", response_class=HTMLResponse)
async def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...)
):
    # For now, we don’t check the database
    # Always show an alert
    return templates.TemplateResponse(
        "login.html",
        {"request": request, "error": "No account found. Please create one."}
    )


    
@router.get("/index")
async def login(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
    

@router.get("/create_account", response_class=HTMLResponse, name="create_account")
async def create_account(request: Request):
    return templates.TemplateResponse("create_account.html", {"request": request})

@router.post("/create_account")
async def create_account_post(
    request: Request,
    first_name: str = Form(...),
    middle_name: str = Form(...),
    last_name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    dob: str = Form(...),
    gender: str = Form(...),
    ssn: UploadFile = File(...),
    home_address: str = Form(...),
    kids: int = Form(...),
    job: str = Form(...),
    marital_status: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
    id_card: UploadFile = File(...)
):
    # ✅ Password validation
    if password.strip() and confirm_password.strip():
        if password != confirm_password:
            return templates.TemplateResponse("create_account.html", {
                "request": request,
                "error": "Passwords do not match",
                "first_name": first_name,
                "middle_name": middle_name,
                "last_name": last_name,
                "email": email,
                "phone": phone,
                "dob": dob,
                "gender": gender,
                "home_address": home_address,
                "kids": kids,
                "job": job,
                "marital_status": marital_status
            })

    # ✅ Save SSN file
    ssn_path = SSN_DIR / ssn.filename
    with open(ssn_path, "wb") as buffer:
        buffer.write(await ssn.read())

    # ✅ Save ID card file
    idcard_path = IDCARD_DIR / id_card.filename
    with open(idcard_path, "wb") as buffer:
        buffer.write(await id_card.read())

    # ✅ Generate dummy NIA ID
    nia_id = "NIA" + str(random.randint(100000000, 999999999))

    # ✅ Hash password before storing
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    # ✅ Store into SQLite3
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
       INSERT INTO users (
          first_name, middle_name, last_name, email,
          phone_number, dob, gender, address,
          kids, job, marital_status
       ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
    first_name, middle_name, last_name, email,
    phone,  # <-- match "phone_number" in DB with "phone" form field
    dob, gender,
    home_address,  # <-- match "address" in DB with "home_address" form field
    kids, job, marital_status
    ))
    conn.commit()
    conn.close()

    # ✅ Render confirmation page
    return templates.TemplateResponse("account_created.html", {
        "request": request,
        "first_name": first_name,
        "last_name": last_name,
        "nia_id": nia_id
    })
    
@router.get("/forget_password", response_class=HTMLResponse)
async def forget_password_page(request: Request):
    return templates.TemplateResponse("forget_password.html", {"request": request})

@router.post("/forget_password")
async def process_forget_password(email: str = Form(...)):
    # Here you’d handle sending the reset link to the email
    return {"message": f"If {email} exists, a reset link has been sent."}   
    
