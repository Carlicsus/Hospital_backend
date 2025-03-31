from fastapi import APIRouter, Depends
from src.controllers.citas_controller import citas_controller
from src.schemas.citas_schemas import CitaMedicaResponse, CitaMedicaCreate, CitaMedicaUpdate
from src.middleware.auth_middleware import auth_middleware
from src.middleware.role_middleware import RoleRequired

class CitasRoutes:
    """Clase que maneja las rutas de citas médicas con un patrón Singleton."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CitasRoutes, cls).__new__(cls)
            cls._instance.router = APIRouter(prefix="/citas", tags=["Citas Médicas"])
            cls._instance.initialize_routes()
        return cls._instance

    def initialize_routes(self):
        """Registra los endpoints en el router usando el controlador."""
        self.router.post("/register", dependencies=[Depends(RoleRequired(["Administrador","Médico Especialista","Médico General","Enfermero"]))], response_model=CitaMedicaResponse)(citas_controller.create_cita)
        self.router.get("/getAll", dependencies=[Depends(RoleRequired(["Administrador","Médico Especialista","Médico General","Enfermero"]))], response_model=list[CitaMedicaResponse])(citas_controller.read_citas)
        self.router.get("/get/{cita_id}", dependencies=[Depends(RoleRequired(["Administrador","Médico Especialista","Médico General","Enfermero"]))], response_model=CitaMedicaResponse)(citas_controller.read_cita)
        self.router.get("/by_month/{medico_id}", dependencies=[Depends(RoleRequired(["Administrador","Médico Especialista","Médico General","Enfermero"]))], response_model=list[CitaMedicaResponse])(citas_controller.get_citas_by_month)
        self.router.put("/update/{cita_id}", dependencies=[Depends(RoleRequired(["Administrador","Médico Especialista","Médico General","Enfermero"]))], response_model=CitaMedicaResponse)(citas_controller.update_cita)
        self.router.delete("/delete/{cita_id}")(citas_controller.delete_cita)

# Se obtiene la instancia única para ser usada en FastAPI
citas_routes = CitasRoutes().router
