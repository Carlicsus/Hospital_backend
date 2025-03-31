import uuid
from sqlalchemy import Column, CHAR, String, Enum, DateTime, Text, func, ForeignKey
from sqlalchemy.orm import relationship
from src.db.db_mysql import databaseMysql
import enum

class CitaMedica(databaseMysql.get_base()):
    __tablename__ = "tbb_citas_medicas"

    id = Column("ID", CHAR(36), primary_key=True, server_default=func.uuid())
    personal_medico_id = Column("Personal_Medico_ID", CHAR(36), ForeignKey("tbb_personal_medico.id"), nullable=False)
    paciente_id = Column("Paciente_ID", CHAR(36), ForeignKey("tbb_personas.id"), nullable=False)
    servicio_medico_id = Column("Servicio_Medico_ID", CHAR(36), ForeignKey("tbc_servicios_medicos.ID"), nullable=False)
    folio = Column("Folio", String(60), unique=True, nullable=False)
    tipo = Column("Tipo", Enum('Revisión', 'Diagnóstico', 'Tratamiento', 'Rehabilitación', 'Preoperatoria', 'Postoperatoria', 'Procedimientos', 'Seguimiento'), nullable=False)
    espacio_id = Column("Espacio_ID", CHAR(36), ForeignKey("tbc_espacios.ID"), nullable=False)
    fecha_programada = Column("Fecha_Programada", DateTime, default=func.now(), nullable=False)
    fecha_inicio = Column("Fecha_Inicio", DateTime, nullable=True)
    fecha_termino = Column("Fecha_Termino", DateTime, nullable=True)
    observaciones = Column("Observaciones", Text, nullable=False)
    estatus = Column("Estatus", Enum('Programada', 'Atendida', 'Cancelada', 'Reprogramada', 'No Atendida', 'EnProceso'), default='Programada', nullable=False)
    fecha_registro = Column("Fecha_Registro", DateTime, default=func.now(), nullable=False)
    fecha_actualizacion = Column("Fecha_Actualizacion", DateTime, nullable=True, onupdate=func.now())

    personal_medico = relationship("PersonalMedico", back_populates="citas")
    paciente = relationship("Persona", back_populates="citas")
    servicio_medico = relationship("ServicioMedico", back_populates="citas")
    espacio = relationship("Espacio", back_populates="citas")


    def __repr__(self):
        return f"<CitaMedica(id={self.id}, folio={self.folio}, tipo={self.tipo}, estatus={self.estatus})>"
