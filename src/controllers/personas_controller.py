from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from src.db.db_mysql import databaseMysql
from src.dao.personas_dao import personasDAO
from src.schemas.personas_schemas import PersonaCreate, PersonaUpdate

class PersonasController:
    """Clase controladora para manejar la lógica de personas con patrón Singleton."""

    _instance = None  # Variable de clase para almacenar la única instancia

    def __new__(cls):
        """Implementa Singleton: Si no hay instancia, la crea."""
        if cls._instance is None:
            cls._instance = super(PersonasController, cls).__new__(cls)
        return cls._instance

    def crear_persona(self, persona: PersonaCreate, db: Session = Depends(databaseMysql.get_db)):
        """Crea una nueva persona."""
        nueva_persona = personasDAO.create_persona(db, persona)
        return JSONResponse(content={"message": "Persona creada", "id": nueva_persona.id}, status_code=201)

    def obtener_persona(self, persona_id: str, db: Session = Depends(databaseMysql.get_db)):
        """Obtiene una persona por ID."""
        persona = personasDAO.get_persona_by_id(db, persona_id)
        if not persona:
            raise HTTPException(status_code=404, detail="Persona no encontrada")
        return persona

    def obtener_todas(self, db: Session = Depends(databaseMysql.get_db)):
        """Obtiene todas las personas."""
        return personasDAO.get_personas(db)

    def actualizar_persona(self, persona_id: str, persona_update: PersonaUpdate, db: Session = Depends(databaseMysql.get_db)):
        """Actualiza los datos de una persona."""
        persona_actualizada = personasDAO.update_persona(db, persona_id, persona_update)
        if not persona_actualizada:
            raise HTTPException(status_code=404, detail="Persona no encontrada")
        return {"message": "Persona actualizada"}

    def eliminar_persona(self, persona_id: str, db: Session = Depends(databaseMysql.get_db)):
        """Elimina una persona por ID."""
        persona_eliminada = personasDAO.delete_persona(db, persona_id)
        if not persona_eliminada:
            raise HTTPException(status_code=404, detail="Persona no encontrada")
        return {"message": "Persona eliminada"}

# Se obtiene la instancia única del controlador
personas_controller = PersonasController()
