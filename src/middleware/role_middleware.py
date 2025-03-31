from fastapi import HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials
from src.middleware.auth_middleware import auth_middleware, security_scheme

class RoleRequired:
    def __init__(self, required_roles: list[str]):
        self.required_roles = required_roles

    def __call__(
        self,
        usuario=Depends(auth_middleware.autenticate_login),
        credentials: HTTPAuthorizationCredentials = Depends(security_scheme)  # esto activa el candado
    ):
        if not any(rol in self.required_roles for rol in getattr(usuario, "roles", [])):
            raise HTTPException(status_code=403, detail="Acceso denegado: Rol insuficiente")
        return usuario
