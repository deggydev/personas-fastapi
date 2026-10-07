from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class PersonaBase(BaseModel):
    nombre: str = Field(min_length=1, max_length=100)
    apellido: str = Field(min_length=1, max_length=100)
    correo: EmailStr = Field(max_length=254)
    mensaje: str = Field(min_length=1, max_length=2000)

    @field_validator("nombre", "apellido", "mensaje", mode="before")
    @classmethod
    def limpiar(cls, value):
        return value.strip() if isinstance(value, str) else value


class PersonaCreate(PersonaBase):
    pass


class PersonaUpdate(BaseModel):
    nombre: str | None = Field(default=None, min_length=1, max_length=100)
    apellido: str | None = Field(default=None, min_length=1, max_length=100)
    correo: EmailStr | None = Field(default=None, max_length=254)
    mensaje: str | None = Field(default=None, min_length=1, max_length=2000)

    @field_validator("nombre", "apellido", "mensaje", mode="before")
    @classmethod
    def limpiar(cls, value):
        if value is None:
            return value
        return value.strip() if isinstance(value, str) else value


class PersonaOut(PersonaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    creado_en: datetime
