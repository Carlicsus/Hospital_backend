# src/models/index_models.py

# Importar primero modelos sin dependencias o con menos relaciones cruzadas
from src.models.areas_medicas_model import AreaMedica
from src.models.roles_model import Roles
from src.models.personas_model import Persona
from src.models.servicios_medicos_model import ServicioMedico

# Luego los que dependen de los anteriores
from src.models.usuarios_model import Usuario
from src.models.usuarios_roles_model import UsuariosRoles
from src.models.departamentos_model import Departamento
from src.models.espacios_model import Espacio
from src.models.personal_medico_model import PersonalMedico
from src.models.citas_medicas_model import CitaMedica
from src.models.bitacora_model import Bitacora



# Definir qué se exporta al importar desde src.models
__all__ = [
    "AreaMedica",
    "Roles",
    "Persona",
    "Usuario",
    "UsuariosRoles",
    "Departamento",
    "PersonalMedico",
    "CitaMedica",
    "ServicioMedico",
    "Espacio",
    "Bitacora"
]
