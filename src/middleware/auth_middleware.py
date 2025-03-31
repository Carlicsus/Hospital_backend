from fastapi import HTTPException, Request, Depends
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from src.helpers.jwt_config import jwt_config
from src.dao.usuarios_dao import usuariosDAO
from src.db.db_mysql import databaseMysql
from fastapi.security import HTTPAuthorizationCredentials


class AuthMiddleware(HTTPBearer):
    """Middleware para validar tokens JWT en las rutas protegidas."""

    _instance = None  # Variable de clase para almacenar la única instancia

    def __new__(cls):
        """Implementa Singleton: Si no hay instancia, la crea."""
        if cls._instance is None:
            cls._instance = super(AuthMiddleware, cls).__new__(cls)
        return cls._instance

    async def autenticate_login(self, request: Request, db: Session = Depends(databaseMysql.get_db)):
        autorizacion = await super().__call__(request)
        datos_token = jwt_config.valida_token(autorizacion.credentials)

        usuario = usuariosDAO.get_user_by_credentials(db, 
            username=datos_token["nombre_usuario"],
            password=datos_token["contrasena"]
        )

        if usuario is None:
            raise HTTPException(status_code=401, detail="Token inválido")

        # Cargar roles desde el token
        usuario.roles = datos_token.get("roles", [])

        return usuario


# Se obtiene la única instancia de AuthMiddleware
auth_middleware = AuthMiddleware()

security_scheme = HTTPBearer()

