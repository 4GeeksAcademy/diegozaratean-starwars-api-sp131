from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "notas": 5,
            # do not serialize the password, its a security breach
        }
    

class Empresa(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    ciudad: Mapped[str] = mapped_column(String(120), nullable=False)
    slogan: Mapped[str] = mapped_column(String(120))

    videojuegos: Mapped[list["Videojuego"]] = relationship(back_populates="empresa")

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "ciudad": self.ciudad,
            # do not serialize the password, its a security breach
        }


class Videojuego(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    year: Mapped[int] = mapped_column( nullable=False)

    empresa_id: Mapped[int] = mapped_column(ForeignKey("empresa.id"))
    empresa: Mapped["Empresa"] = relationship(back_populates="videojuegos")
    
    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre
            # do not serialize the password, its a security breach
        }
