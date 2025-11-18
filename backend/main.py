from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.rh_routes import router as rh_router
# futuro: from backend.api.pdf_routes import router as pdf_router
# futuro: from backend.api.system_routes import router as system_router


app = FastAPI(
    title="PDFCompile API",
    version="0.1.0",
    description="API backend para compilação automática de documentos RH (PRR/PT2030).",
)

# CORS – por agora deixamos aberto; mais tarde podes restringir ao domínio da app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "PDFCompile API running",
        "version": "0.1.0",
    }


# Routers
app.include_router(rh_router, prefix="/rh", tags=["rh"])
# app.include_router(pdf_router, prefix="/pdf", tags=["pdf"])
# app.include_router(system_router, prefix="/system", tags=["system"])
