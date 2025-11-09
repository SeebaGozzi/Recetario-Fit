
# Recetario Fit (PWA)

App PWA de recetas saludables con backend FastAPI y base de datos PostgreSQL.
El backend sirve la SPA construida para que puedas desplegar **un solo servicio** en Render.

## Tech
- **Frontend**: React (Vite) + Tailwind CSS, colores: beige `#F5F0E6`, verde `#2E7D32`, negro `#111111`
- **Backend**: FastAPI + SQLAlchemy
- **DB**: PostgreSQL (Render) — local fallback a SQLite
- **PWA**: manifest + service worker simple (cache-first)

## Estructura
```
recetario-fit/
├─ app/                 # Backend FastAPI
│  ├─ main.py
│  ├─ database.py
│  ├─ models.py
│  ├─ schemas.py
│  └─ seed.py           # Inserta 3 recetas saludables por defecto
├─ frontend/            # Frontend Vite React
│  ├─ public/
│  │  ├─ manifest.webmanifest
│  │  ├─ sw.js
│  │  └─ icons/icon-*.png
│  ├─ src/
│  │  ├─ App.jsx
│  │  ├─ main.jsx
│  │  └─ index.css
│  ├─ index.html
│  ├─ package.json
│  └─ tailwind.config.js
├─ requirements.txt
├─ start.sh
└─ render.yaml
```

## Desarrollo local
1. **Backend**:
   ```bash
   python -m venv .venv && source .venv/bin/activate  # En Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   export DATABASE_URL=sqlite:///./local.db  # opcional para local
   uvicorn app.main:app --reload
   ```

2. **Frontend** (en otra terminal):
   ```bash
   cd frontend
   npm i
   npm run dev
   ```
   Para producción local:
   ```bash
   npm run build
   cd ..
   rm -rf app/static && mkdir -p app/static
   cp -r frontend/dist/* app/static/
   uvicorn app.main:app --reload
   ```

## Deploy en Render
1. Sube este repo a GitHub.
2. En Render crea un **Web Service** desde el repo.
3. Render detectará `render.yaml`:
   - Instala Python deps
   - Construye el frontend (`npm ci && npm run build`)
   - Copia `frontend/dist` dentro de `app/static`
   - Arranca `uvicorn`
4. Configura `DATABASE_URL` (provisión de PostgreSQL de Render) en las **Env Vars**.
5. Abrí tu URL — la app debería cargar el frontend y la API en el mismo dominio.

## Endpoints rápidos
- `GET /api/recipes` lista de recetas saludables (precargadas).
- `POST /api/recipes` crea receta JSON:
  ```json
  {
    "title": "Pan de avena",
    "category": "panes",
    "ingredients": ["avena", "agua"],
    "steps": "Mezclar y hornear"
  }
  ```
- `POST /api/pdfs` (multipart form) campos: `title`, `description?`, `file` (PDF). Guarda el PDF dentro de la DB.
- `GET /api/pdfs` lista metadatos.
- `GET /api/pdfs/{id}` descarga el PDF.

> Para CORS no hace falta config extra en Render porque todo sirve del mismo servicio.
