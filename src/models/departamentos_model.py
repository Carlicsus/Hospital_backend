import uuid
from sqlalchemy import Column, CHAR, String, ForeignKey, DateTime, Boolean, func
from sqlalchemy.orm import relationship
from src.db.db_mysql import databaseMysql

class Departamento(databaseMysql.get_base()):
    __tablename__ = "tbc_departamentos"

    id = Column(CHAR(36), primary_key=True, server_default=func.uuid())
    nombre = Column(String(100), nullable=False)
    abreviatura = Column(String(20), nullable=True)
    
    area_medica_id = Column(CHAR(36), ForeignKey("tbc_areas_medicas.id"), nullable=True)
    departamento_superior_id = Column(CHAR(36), ForeignKey("tbc_departamentos.id"), nullable=True)
    responsable_id = Column(CHAR(36), ForeignKey("tbb_personal_medico.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=True)

    estatus = Column(Boolean, nullable=False)
    fecha_registro = Column(DateTime, nullable=False, default=func.now())
    fecha_actualizacion = Column(DateTime, nullable=True, onupdate=func.now())

    # Relaciones
    area_medica = relationship("AreaMedica", back_populates="departamentos")
    departamento_superior = relationship("Departamento", remote_side=[id], backref="subdepartamentos")
    responsable = relationship("PersonalMedico", back_populates="departamentos", foreign_keys=[responsable_id])

    def __repr__(self):
        return f"<Departamento(id={self.id}, nombre={self.nombre}, estatus={'Activo' if self.estatus else 'Inactivo'})>"
