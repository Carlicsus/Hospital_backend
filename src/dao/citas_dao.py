from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime
from uuid import UUID
from src.models.citas_medicas_model import CitaMedica
from src.schemas.citas_schemas import CitaMedicaCreate, CitaMedicaUpdate
from src.models.personal_medico_model import PersonalMedico

class CitasMedicasDAO:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CitasMedicasDAO, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        pass

    def create_cita(self, db: Session, cita: CitaMedicaCreate):
        db_cita = CitaMedica(**cita.model_dump())
        db.add(db_cita)
        db.commit()
        db.refresh(db_cita)
        return db_cita

    def get_cita_by_id(self, db: Session, cita_id: str):
        return db.query(CitaMedica).filter(CitaMedica.id == cita_id).first()
    
    # def get_citas_by_month(self, db: Session, year: int, month: int, medico_id: UUID):
    #     start_date = datetime(year, month, 1)
    #     if month == 12:
    #         end_date = datetime(year + 1, 1, 1)
    #     else:
    #         end_date = datetime(year, month + 1, 1)

    #     personal_real = db.query(PersonalMedico).filter(PersonalMedico.persona_id == medico_id).first()

    #     return db.query(CitaMedica).filter(
    #         CitaMedica.fecha_programada >= start_date,
    #         CitaMedica.fecha_programada < end_date,
    #         CitaMedica.personal_medico_id == str(personal_real.id)
    #     ).all()

    def get_citas_by_month(self, db: Session, year: int, month: int, medico_id: UUID):
        start_date = datetime(year, month, 1)
        end_date = datetime(year + 1, 1, 1) if month == 12 else datetime(year, month + 1, 1)

        personal_real = db.query(PersonalMedico).filter(PersonalMedico.persona_id == str(medico_id)).first()

        if not personal_real:
            raise HTTPException(status_code=404, detail="No se encontró un médico con ese ID de persona.")

    # Consulta de citas
        return db.query(CitaMedica).filter(
            CitaMedica.fecha_programada >= start_date,
            CitaMedica.fecha_programada < end_date,
            CitaMedica.personal_medico_id == str(personal_real.id)
        ).all()


    def get_all_citas(self, db: Session, skip: int = 0, limit: int = 10):
        return db.query(CitaMedica).offset(skip).limit(limit).all()

    def update_cita(self, db: Session, cita_id: str, cita_update: CitaMedicaUpdate):
        db_cita = db.query(CitaMedica).filter(CitaMedica.id == cita_id).first()
        if not db_cita:
            return None
        for field, value in cita_update.model_dump(exclude_unset=True).items():
            setattr(db_cita, field, value)
        db.commit()
        db.refresh(db_cita)
        return db_cita

    def delete_cita(self, db: Session, cita_id: str):
        db_cita = db.query(CitaMedica).filter(CitaMedica.id == cita_id).first()
        if db_cita:
            db.delete(db_cita)
            db.commit()
            return True
        return False

citasDAO = CitasMedicasDAO()