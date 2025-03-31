from sqlalchemy import Column, String, Text, DateTime, Boolean, func
from sqlalchemy.orm import relationship
from src.db.db_mysql import databaseMysql
import uuid

class Roles(databaseMysql.get_base()):
    __tablename__ = "tbc_roles"

    ID = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False)
    Nombre = Column(String(50), nullable=False)
    Descripcion = Column(Text)
    Estatus = Column(Boolean, default=True, nullable=False)
    Fecha_Registro = Column(DateTime, default=func.now(), nullable=False)
    Fecha_Actualizacion = Column(DateTime, onupdate=func.now())

    roles_usuarios = relationship("UsuariosRoles", back_populates="rol", cascade='all, delete-orphan')
