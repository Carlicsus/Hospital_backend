from fastapi import APIRouter, Depends
from typing import List
from src.controllers.personal_medico_controller import personalMedicoController
from src.schemas.personal_medico_schemas import PersonalMedicoResponse
from src.middleware.auth_middleware import auth_middleware
from src.middleware.role_middleware import RoleRequired

class PersonalMedicoRoutes:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PersonalMedicoRoutes, cls).__new__(cls)
            cls._instance.router = APIRouter(prefix="/api/empleado", tags=["Personal Médico"])
            cls._instance.initialize_routes()
        return cls._instance

    def initialize_routes(self):
        self.router.get("/doctor/{doctor_id}", dependencies=[Depends(RoleRequired(["Administrador","Administrativo","Direccion General"]))], response_model=PersonalMedicoResponse)(personalMedicoController.get_doctor)
        self.router.get("/getAllDoctors", dependencies=[Depends(RoleRequired(["Administrador","Administrativo","Direccion General"]))], response_model=List[PersonalMedicoResponse])(personalMedicoController.get_all_doctors)
        self.router.get("/nurse/{nurse_id}", dependencies=[Depends(RoleRequired(["Administrador","Administrativo","Direccion General"]))], response_model=PersonalMedicoResponse)(personalMedicoController.get_nurse)
        self.router.get("/getAllNurses", dependencies=[Depends(RoleRequired(["Administrador","Administrativo","Direccion General"]))], response_model=List[PersonalMedicoResponse])(personalMedicoController.get_all_nurses)
        # self.router.get("/doctor/{id}", response_model=PersonalMedicoResponse, dependencies=[Depends(auth_middleware.autenticate_login)])(personalMedicoController.get_doctor)
        # self.router.get("/getAllDoctors", response_model=PersonalMedicoResponse, dependencies=[Depends(auth_middleware.autenticate_login)])(personalMedicoController.get_all_doctors)
        # self.router.get("/nurse/{id}", response_model=PersonalMedicoResponse, dependencies=[Depends(auth_middleware.autenticate_login)])(personalMedicoController.get_nurse)
        # self.router.get("/getAllNurses", response_model=PersonalMedicoResponse, dependencies=[Depends(auth_middleware.autenticate_login)])(personalMedicoController.get_all_nurses)
        

personal_medico_routes = PersonalMedicoRoutes().router