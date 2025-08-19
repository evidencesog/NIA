from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from fastapi import APIRouter, Form, File, UploadFile
import os
from starlette.status import HTTP_303_SEE_OTHER
import random

BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

router = APIRouter()

# Login page
@router.get("/login")
async def login(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

# Create Account page GET
@router.get("/create_account")
async def create_account_get(request: Request):
    return templates.TemplateResponse("create_account.html", {"request": request})

# Create Account page POST
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
    ssn: str = Form(...),
    home_address: str = Form(...),
    kids: int = Form(...),
    job: str = Form(...),
    marital_status: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
    id_card: UploadFile = File(...)
):
   # Validate password only if user submitted it
  if password.strip() or confirm_password.strip():
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
            "ssn": ssn,
            "home_address": home_address,
            "kids": kids,
            "job": job,
            "marital_status": marital_status
        })

  # Example: save uploaded file to disk
    file_location = f"uploads/{id_card.filename}"
    with open(file_location, "wb") as buffer:
        buffer.write(await id_card.read())

    #return {"message": "Form submitted successfully!", "filename": id_card.filename}
    
    # Generate dummy NIA ID
    nia_id = "NIA" + str(random.randint(100000000, 999999999))

    # Render confirmation page
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
    
