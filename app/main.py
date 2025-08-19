from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path

# Import your form routes
from app.routes import form_routes  

app = FastAPI()

# Include router
app.include_router(form_routes.router)

# Base directory
BASE_DIR = Path(__file__).resolve().parent

# Mount static directory
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Templates directory
templates = Jinja2Templates(directory=BASE_DIR / "templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/form", response_class=HTMLResponse, name="form_page")
async def form_page(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})
