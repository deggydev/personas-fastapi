from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from app.database import lifespan
from app.routers.personas import router as personas_router

app = FastAPI(title="API Personas FastAPI", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", include_in_schema=False)
def formulario():
    return FileResponse(Path(__file__).with_name("formulario.html"))


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(personas_router)
