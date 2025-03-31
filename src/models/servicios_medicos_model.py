import uuid
from sqlalchemy import Column, CHAR, String, Text, DateTime, Boolean, func
from sqlalchemy.orm import relationship
from src.db.db_mysql import databaseMysql

class ServicioMedico(databaseMysql.get_base()):
    __tablename__ = "tbc_servicios_medicos"

    ID = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    Nombre = Column(String(255), unique=True, nullable=False)
    Descripcion = Column(Text, nullable=False)
    Observaciones = Column(Text, nullable=True)
    Fecha_Registro = Column(DateTime, default=func.now(), nullable=False)
    Fecha_Actualizacion = Column(DateTime, onupdate=func.now())
    Estatus = Column(Boolean, default=True, nullable=False)

    # Relación inversa desde CitaMedica
    citas = relationship("CitaMedica", back_populates="servicio_medico")

    def __repr__(self):
        return f"<ServicioMedico(id={self.ID}, nombre={self.Nombre}, estatus={self.Estatus})>"
