from fastapi import Depends, FastAPI, WebSocket, WebSocketDisconnect,  HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
from src.tasks.citas_task import revisar_citas_medicas
from src.websockets.ws_manager import ws_manager
from src.db.db_mysql import databaseMysql
import asyncio
from src.tasks.task_manager import iniciar_tareas_background
from src.routes.usuarios_routes import usuario_routes
from src.routes.notas_medicas_routes import notasMedicasRoutes
from contextlib import asynccontextmanager
from src.routes.graficas_routes import graficas_routes
from src.routes.citas_routes import citas_routes
from src.routes.personal_medico_routes import personal_medico_routes
from src.dao.grupos_sanguineos_dao import grupos_sanguineos_dao
from src.dao.grupos_sanguineos_dao import grupos_sanguineos_dao
from sqlalchemy.orm import Session
from typing import List
import jwt
import os
from uuid import uuid4
from src.helpers.jwt_config import jwt_config
from src.tasks.bitacora_tasks import revisar_bitacora


class HospitalBackend:
    """Clase Singleton para manejar la configuración y creación de la aplicación FastAPI."""

    _instance = None  # Variable de clase para almacenar la única instancia

    def __new__(cls):
        """Implementa el patrón Singleton asegurando una única instancia."""
        if cls._instance is None:
            cls._instance = super(HospitalBackend, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Inicializa la configuración de la aplicación FastAPI."""
        # Inicialización de la aplicación FastAPI
        self.app = FastAPI(
            lifespan=self.lifespan,
            redirect_slashes=False,
            title="Backend del hospital",
            description="Backend del hospital",
        )
        
        # Configuración de CORS
        self._configure_cors()

        # Inclusión de rutas
        self._include_routes()

        # Incluir el WebSocket
        self._include_websocket()

        # Base de datos y creación de tablas
        self._configure_database()

    def _configure_cors(self):
        """Configura las opciones CORS para permitir peticiones desde Angular"""
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # Permitir solicitudes desde Angular
            allow_credentials=True,
            allow_methods=["*"],  # Permitir todos los métodos HTTP
            allow_headers=["*"],  # Permitir todos los encabezados
        )

    def _configure_database(self):
        """Configura la base de datos y crea las tablas"""
        Base = databaseMysql.get_base()
        Base.metadata.create_all(bind=databaseMysql.get_engine())

    def _include_routes(self):
        """Incluye las rutas en la aplicación FastAPI"""
        self.app.include_router(usuario_routes)
        self.app.include_router(notasMedicasRoutes)
        self.app.include_router(graficas_routes)
        self.app.include_router(citas_routes)
        self.app.include_router(personal_medico_routes)

    def _include_websocket(self):
        """Incluye el WebSocket en la aplicación FastAPI."""
        @self.app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket):
            """Maneja la conexión WebSocket con autenticación y manejo de clientes."""
            token = websocket.query_params.get("token")

            if not token:
                await websocket.close(code=1008)
                return

            client_id, roles = await ws_manager.connect(websocket, token)
            if client_id:
                await ws_manager.listen(websocket, client_id, roles)

                    
    @asynccontextmanager
    async def lifespan(self, app: FastAPI):
        """Maneja el ciclo de vida de la aplicación."""
        print("Aplicación iniciada")
        loop = asyncio.get_event_loop()
        iniciar_tareas_background(loop)
        yield  # Permite que FastAPI continúe su proceso
        print("Aplicación cerrada") 


    def get_app(self):
        """Devuelve la instancia de la aplicación FastAPI"""
        return self.app


# Crear la instancia única
app_instance = HospitalBackend()
app = app_instance.get_app()

# MANEJADORES DE EXCEPCIONES GLOBALES
# ----------------------------------
# Aseguran que, ante cualquier error (incluso 401, 403, 500, etc.), 
# la respuesta incluya encabezados CORS. 

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": f"Error interno en el servidor: {exc}"},
        headers={"Access-Control-Allow-Origin": "*"}
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
        headers={"Access-Control-Allow-Origin": "*"}
    )
app.lifespan = app_instance.lifespan

@app.get("/users/online-doctors")
async def get_online_doctors():
    return [
        {"user_id": user_id, "client_id": client_id}
        for user_id, client_id in ws_manager.user_client_map.items()
        if "Médico General" in ws_manager.channels and client_id in ws_manager.channels["Médico General"]
    ]

