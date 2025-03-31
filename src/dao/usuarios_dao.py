from sqlalchemy.orm import Session
from src.models.index_models import *
from src.schemas.usuarios_schemas import UsuarioCreate, UsuarioUpdate
from sqlalchemy.orm import selectinload
from uuid import uuid4



class UsuariosDAO:
    _instance = None
    
    def __new__(cls):
        """Implementa el patrón Singleton para asegurar una única instancia."""
        if cls._instance is None:
            cls._instance = super(UsuariosDAO, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """COnstructor de usuariosDAO"""
        pass
    
    def get_user_by_username(self, db: Session, username: str):
        """
        Obtiene un usuario por su nombre de usuario.
        """
        return db.query(Usuario).filter(Usuario.nombre_usuario == username).first()

    def create_user(self, db: Session, user: UsuarioCreate):
        """
        Crea un nuevo usuario en la base de datos.
        """
        db_user = Usuario(
            id=str(uuid4()),
            persona_id=user.persona_id,
            nombre_usuario=user.nombre_usuario,
            correo_electronico=user.correo_electronico,
            contrasena=user.contrasena,
            numero_telefonico_movil=user.numero_telefonico_movil,
            estatus=user.estatus,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    def get_user_by_credentials(self, db: Session, username: str, password: str):
        """
        Obtiene un usuario que coincida con sus credenciales (usuario, correo o teléfono y contraseña).
        """
        return (
            db.query(Usuario)
            .filter(Usuario.nombre_usuario == username, Usuario.contrasena == password)
            .options(selectinload(Usuario.usuario_roles).selectinload(UsuariosRoles.rol))  # para pre-cargar roles
            .first()
        )
        
    def get_users(self, db: Session, skip: int = 0, limit: int = 10):
        """
        Obtiene una lista de usuarios paginada.
        """
        return db.query(Usuario).offset(skip).limit(limit).all()
    
    def obtener_persona_usuario_por_id(self, db: Session, usuario_id: str):
        resultado = (
            db.query(
                Persona.titulo,
                (Persona.nombre + " " + Persona.primer_apellido + " " + Persona.segundo_apellido).label("nombre_completo"),
                Persona.grupo_sanguineo,
                Usuario.correo_electronico,
                Usuario.numero_telefonico_movil
            )
            .join(Usuario, Usuario.persona_id == Persona.id)
            .filter(Usuario.id == usuario_id)
            .first()
        )

        if resultado is None:
            return None

        return {
            "titulo": resultado.titulo,
            "nombre_completo": resultado.nombre_completo.strip(),
            "grupo_sanguineo": resultado.grupo_sanguineo,
            "correo_electronico": resultado.correo_electronico,
            "numero_telefonico_movil": resultado.numero_telefonico_movil
        }
    
usuariosDAO = UsuariosDAO()
