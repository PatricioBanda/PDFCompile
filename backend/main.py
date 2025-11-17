from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.rh_routes import router as rh_router
# no futuro: from backend.api.pdf_routes import router as pdf_router, etc.

app = FastAPI(
    title="RH Document Compiler API",
    version="0.1.0"
)

# CORS – permite que o frontend (no browser) fale com a API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # se quiseres, depois restringimos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(rh_router, prefix="/rh", tags=["rh"])


@app.get("/")
def read_root():
    return {"status": "ok", "message": "RH Document Compiler API"}
