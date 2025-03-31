from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean, func
from sqlalchemy.orm import relationship
from sqlalchemy.schema import PrimaryKeyConstraint
from src.db.db_mysql import databaseMysql

class UsuariosRoles(databaseMysql.get_base()):
    __tablename__ = "tbd_usuarios_roles"

    Usuario_ID = Column(String(36), ForeignKey("tbb_usuarios.id"), nullable=False)
    Rol_ID = Column(String(36), ForeignKey("tbc_roles.ID"), nullable=False)
    Estatus = Column(Boolean, default=True)
    Fecha_Registro = Column(DateTime, default=func.now(), nullable=False)
    Fecha_Actualizacion = Column(DateTime, onupdate=func.now())

    # Definir clave primaria compuesta
    __table_args__ = (
        PrimaryKeyConstraint("Usuario_ID", "Rol_ID"),
    )

    usuario = relationship("Usuario", back_populates="usuario_roles")
    rol = relationship("Roles", back_populates="roles_usuarios")
