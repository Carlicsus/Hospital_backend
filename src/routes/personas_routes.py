from fastapi import APIRouter, Depends
from src.controllers.personas_controller import personas_controller
from src.schemas.personas_schemas import PersonaCreate, PersonaUpdate
from src.middleware.role_middleware import RoleRequired

class PersonaRoutes:
    """Clase que maneja las rutas de usuario con un patrón Singleton."""

    _instance = None  # Variable de clase para almacenar la única instancia

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PersonaRoutes, cls).__new__(cls)
            cls._instance.router = APIRouter(prefix="/personas", tags=["Personas"])
            cls._instance.initialize_routes()
        return cls._instance

    def initialize_routes(self):
        """Registra los endpoints en el router usando el controlador."""
        self.router.post("/", dependencies=[Depends(RoleRequired(["Administrador"]))], response_model=dict)(personas_controller.crear_persona)
        self.router.get("/{persona_id}", dependencies=[Depends(RoleRequired(["Administrador", "Médico Especialista", "Médico General"]))], response_model=dict)(personas_controller.obtener_persona)
        self.router.get("/", dependencies=[Depends(RoleRequired(["Administrador", "Médico Especialista", "Médico General"]))], response_model=list)(personas_controller.obtener_todas)
        self.router.put("/{persona_id}", dependencies=[Depends(RoleRequired(["Administrador"]))], response_model=dict)(personas_controller.actualizar_persona)
        self.router.delete("/{persona_id}", dependencies=[Depends(RoleRequired(["Administrador"]))], response_model=dict)(personas_controller.eliminar_persona)

# Se obtiene la única instancia de la clase y se usa en FastAPI 
persona_routes = PersonaRoutes().router
