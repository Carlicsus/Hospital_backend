import uuid
import enum
from sqlalchemy import Column, CHAR, String, Enum, Integer, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from src.db.db_mysql import databaseMysql

class TipoEspacioEnum(str, enum.Enum):
    Piso = "Piso"
    Consultorio = "Consultorio"
    Laboratorio = "Laboratorio"
    Quirófano = "Quirófano"
    Sala_Espera = "Sala de Espera"
    Edificio = "Edificio"
    Estacionamiento = "Estacionamiento"
    Habitación = "Habitación"
    Cama = "Cama"
    Sala_Maternidad = "Sala Maternidad"
    Cunero = "Cunero"
    Morgue = "Morgue"
    Oficina = "Oficina"
    Sala_Juntas = "Sala de Juntas"
    Auditorio = "Auditorio"
    Cafeteria = "Cafeteria"
    Capilla = "Capilla"
    Farmacia = "Farmacia"
    Ventanilla = "Ventanilla"
    Recepción = "Recepción"

class EstatusEspacioEnum(str, enum.Enum):
    Activo = "Activo"
    Inactivo = "Inactivo"
    Remodelacion = "En remodelación"
    Clausurado = "Clausurado"
    Reubicado = "Reubicado"
    Temporal = "Temporal"

class Espacio(databaseMysql.get_base()):
    __tablename__ = "tbc_espacios"

    ID = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    Tipo = Column(Enum('Piso', 'Consultorio', 'Laboratorio', 'Quirófano', 'Sala de Espera', 'Edificio', 'Estacionamiento', 'Habitación', 'Cama', 'Sala Maternidad', 'Cunero', 'Morgue', 'Oficina', 'Sala de Juntas', 'Auditorio', 'Cafeteria', 'Capilla', 'Farmacia', 'Ventanilla', 'Recepción'), nullable=False)
    Nombre = Column(String(100), unique=True, nullable=False)
    Departamento_ID = Column(CHAR(36), ForeignKey("tbc_departamentos.id"), nullable=False)
    Estatus = Column(Enum('Activo', 'Inactivo', 'En remodelación', 'Clausurado', 'Reubicado', 'Temporal'), default=EstatusEspacioEnum.Activo, nullable=False)
    Fecha_Registro = Column(DateTime, default=func.now(), nullable=False)
    Fecha_Actualizacion = Column(DateTime, onupdate=func.now())
    Capacidad = Column(Integer, nullable=False, default=0)
    Espacio_Superior_ID = Column(CHAR(36), ForeignKey("tbc_espacios.ID"), nullable=True)

    departamento = relationship("Departamento", backref="espacios")
    espacio_superior = relationship("Espacio", remote_side=[ID], backref="subespacios")
    citas = relationship("CitaMedica", back_populates="espacio")

    def __repr__(self):
        return f"<Espacio(id={self.ID}, nombre={self.Nombre}, tipo={self.Tipo}, estatus={self.Estatus})>"
