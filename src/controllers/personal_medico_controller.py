from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from src.db.db_mysql import databaseMysql
from src.dao.personal_medico_dao import personalMedicoDAO

class PersonalMedicoController:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PersonalMedicoController, cls).__new__(cls)
        return cls._instance

    def get_doctor(self, doctor_id: str, db: Session = Depends(databaseMysql.get_db)):
        doctor = personalMedicoDAO.get_doctor_by_id(db, doctor_id)
        if not doctor:
            raise HTTPException(status_code=404, detail="No se encontró el doctor con ese ID")
        return doctor
    
    def get_all_doctors(self, db: Session = Depends(databaseMysql.get_db)):
        doctors = personalMedicoDAO.get_all_doctors(db)
        if not doctors:
            raise HTTPException(status_code=404, detail="No se encontraron doctores")
        return doctors
    
    def get_nurse(self, nurse_id: str, db: Session = Depends(databaseMysql.get_db)):
        nurse = personalMedicoDAO.get_nurse_by_id(db,nurse_id)
        if not nurse:
            raise HTTPException(status_code=404, detail="No se encontró el enfermero con ese ID")
        return nurse
    
    def get_all_nurses(self, db: Session = Depends(databaseMysql.get_db)):
        nurses = personalMedicoDAO.get_all_nurses(db)
        if not nurses:
            raise HTTPException(status_code=404, detail="No se encontraron enfermeros")
        return nurses

personalMedicoController = PersonalMedicoController()