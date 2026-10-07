from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Persona
from app.schemas import PersonaCreate, PersonaOut, PersonaUpdate

router = APIRouter(prefix="/api/personas", tags=["personas"])


def _buscar_o_404(db: Session, id: int) -> Persona:
    persona = db.get(Persona, id)
    if not persona:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    return persona


@router.post("", response_model=PersonaOut, status_code=201)
def registrar(data: PersonaCreate, db: Session = Depends(get_db)):
    persona = Persona(**data.model_dump())
    db.add(persona)
    db.commit()
    db.refresh(persona)
    return persona


@router.get("", response_model=list[PersonaOut])
def listar(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    return db.scalars(
        select(Persona).order_by(Persona.id.desc()).offset(offset).limit(limit)
    ).all()


@router.get("/{id}", response_model=PersonaOut)
def consultar(id: int, db: Session = Depends(get_db)):
    return _buscar_o_404(db, id)


@router.patch("/{id}", response_model=PersonaOut)
def editar(id: int, data: PersonaUpdate, db: Session = Depends(get_db)):
    persona = _buscar_o_404(db, id)
    for campo, valor in data.model_dump(exclude_unset=True).items():
        setattr(persona, campo, valor)
    db.commit()
    db.refresh(persona)
    return persona


@router.delete("/{id}", status_code=204)
def eliminar(id: int, db: Session = Depends(get_db)):
    persona = _buscar_o_404(db, id)
    db.delete(persona)
    db.commit()
