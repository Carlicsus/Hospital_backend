from fastapi import HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from src.schemas.usuarios_schemas import UsuarioCreate, UsuarioLogin
from src.db.db_mysql import databaseMysql
from src.models.index_models import *
from src.dao.usuarios_dao import usuariosDAO
from src.helpers.jwt_config import jwt_config
from datetime import date
from decimal import Decimal

class UsuariosController:
    """Clase controladora para manejar la lógica de usuario con patrón Singleton."""

    _instance = None  # Variable de clase para almacenar la única instancia

    def __new__(cls):
        """Implementa Singleton: Si no hay instancia, la crea."""
        if cls._instance is None:
            cls._instance = super(UsuariosController, cls).__new__(cls)
        return cls._instance

    def create_user(self, user: UsuarioCreate, db: Session = Depends(databaseMysql.get_db)):
        """Crea un nuevo usuario en la base de datos."""
        db_user = usuariosDAO.get_user_by_username(db, username=user.nombre_usuario)
        if db_user:
            raise HTTPException(status_code=400, detail="Usuario existente, intenta nuevamente")
        return usuariosDAO.create_user(db=db, user=user)

    from datetime import date

    def read_credentials(self, usuario: UsuarioLogin, db: Session = Depends(databaseMysql.get_db)):
        """Valida credenciales y genera un token de autenticación con información del rol del usuario."""
        db_credentials = db.query(Usuario).filter(
            Usuario.nombre_usuario == usuario.nombre_usuario,
            Usuario.contrasena == usuario.contrasena
        ).first()

        if db_credentials is None:
            return JSONResponse(content={'mensaje': 'Acceso denegado'}, status_code=404)

        # Obtener el rol del usuario
        usuario_rol = db.query(UsuariosRoles).filter(
            UsuariosRoles.Usuario_ID == db_credentials.id
        ).first()
        
        if usuario_rol:
            rol = usuario_rol.rol.Nombre  # Accede al nombre del rol
        else:
            rol = "Sin Rol"

        # Construir el payload del token
        token_data = {
            "nombre_usuario": usuario.nombre_usuario,
            "contrasena": usuario.contrasena,
            "rol": rol  # Agregar el rol del usuario al token
        }

        # Generar el token JWT
        token: str = jwt_config.solicita_token(token_data)

        return JSONResponse(status_code=200, content={"token": token, "rol": rol})

    
    def read_users(self, skip: int = 0, limit: int = 10, db: Session = Depends(databaseMysql.get_db)):
        db_users = usuariosDAO.get_users(db=db, skip=skip, limit=limit)
        return db_users

# Se obtiene la instancia única de UsuariosController
usuarios_controller = UsuariosController()
