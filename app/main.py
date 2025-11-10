import os
from typing import List, Optional
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from . import models, schemas, seed

# Crear tablas
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Recetario Fit API", version="1.0.5")

# CORS
origins = os.environ.get("CORS_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Seed inicial
@app.on_event("startup")
def startup_event():
    db = next(get_db())
    if db.query(models.Recipe).count() == 0:
        seed.insert_initial_recipes(db)

# ---------------- API ----------------
@app.get("/api/recipes", response_model=List[schemas.RecipeOut])
def list_recipes(db: Session = Depends(get_db)):
    return db.query(models.Recipe).order_by(models.Recipe.id.desc()).all()

@app.post("/api/recipes", response_model=schemas.RecipeOut)
def create_recipe(recipe: schemas.RecipeCreate, db: Session = Depends(get_db)):
    new_r = models.Recipe(
        title=recipe.title,
        category=recipe.category,
        ingredients=recipe.ingredients,
        steps=recipe.steps,
        is_healthy=True if recipe.is_healthy is None else recipe.is_healthy
    )
    db.add(new_r); db.commit(); db.refresh(new_r)
    return new_r

@app.get("/api/recipes/{recipe_id}", response_model=schemas.RecipeOut)
def get_recipe(recipe_id: int, db: Session = Depends(get_db)):
    r = db.get(models.Recipe, recipe_id)
    if not r:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return r

@app.post("/api/pdfs", response_model=schemas.PDFOut)
async def upload_pdf(
    title: str = Form(...),
    description: Optional[str] = Form(None),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Solo se permiten archivos PDF.")
    data = await file.read()
    pdf = models.RecipePDF(
        title=title,
        description=description,
        filename=file.filename,
        content_type=file.content_type or "application/pdf",
        data=data
    )
    db.add(pdf); db.commit(); db.refresh(pdf)
    return pdf

@app.get("/api/pdfs", response_model=List[schemas.PDFOutMeta])
def list_pdfs(db: Session = Depends(get_db)):
    q = db.query(models.RecipePDF.id, models.RecipePDF.title, models.RecipePDF.description, models.RecipePDF.filename)\
          .order_by(models.RecipePDF.id.desc()).all()
    return [{"id": r[0], "title": r[1], "description": r[2], "filename": r[3]} for r in q]

@app.get("/api/pdfs/{pdf_id}")
def download_pdf(pdf_id: int, db: Session = Depends(get_db)):
    pdf = db.get(models.RecipePDF, pdf_id)
    if not pdf:
        raise HTTPException(status_code=404, detail="PDF no encontrado")
    return StreamingResponse(
        iter([pdf.data]),
        media_type=pdf.content_type,
        headers={"Content-Disposition": f'attachment; filename="{pdf.filename}"'}
    )

# ---------------- STATIC (SPA) ----------------
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(STATIC_DIR, exist_ok=True)

# Servir colecciones directamente en rutas top-level
app.mount("/assets", StaticFiles(directory=os.path.join(STATIC_DIR, "assets"), html=False), name="assets")
app.mount("/icons", StaticFiles(directory=os.path.join(STATIC_DIR, "icons"), html=False), name="icons")
app.mount("/static", StaticFiles(directory=STATIC_DIR, html=False), name="static")  # por compatibilidad

def _index_response():
    index_path = os.path.join(STATIC_DIR, "index.html")
    if os.path.isfile(index_path):
        return FileResponse(index_path)
    return HTMLResponse(
        "<h1>Recetario Fit</h1><p>Build del frontend no encontrado en app/static. Revisá el build de Vite.</p>",
        status_code=200
    )

@app.get("/manifest.webmanifest", include_in_schema=False)
def manifest():
    return FileResponse(os.path.join(STATIC_DIR, "manifest.webmanifest"))

@app.get("/sw.js", include_in_schema=False)
def service_worker():
    # SW debe servirse en la raíz
    return FileResponse(os.path.join(STATIC_DIR, "sw.js"))

@app.get("/", include_in_schema=False)
def root():
    return _index_response()

@app.get("/{full_path:path}", include_in_schema=False)
def spa_fallback(full_path: str, request: Request):
    # No pisar endpoints de API
    if full_path.startswith("api/"):
        raise HTTPException(status_code=404, detail="Not Found")
    return _index_response()
