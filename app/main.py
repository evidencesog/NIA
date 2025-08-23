#main.py

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import os

# Import your form routes
from app.routes import form_routes  

app = FastAPI()

# Include router
app.include_router(form_routes.router)


#Base Directory
BASE_DIR = Path(__file__).resolve().parent
print("BASE_DIR =>", BASE_DIR)



# Static
app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static",
)

# Templates
templates = Jinja2Templates(directory=BASE_DIR / "templates")



@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/form", response_class=HTMLResponse, name="form_page")
async def form_page(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})
