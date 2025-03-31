from sqlalchemy import Column, Integer, String, Enum, Text, DateTime, Boolean
from src.db.db_mysql import databaseMysql

class Bitacora(databaseMysql.get_base()):
    __tablename__ = "tbi_bitacora"

    ID = Column(Integer, primary_key=True, autoincrement=True)
    Usuario = Column(String(50), nullable=False)
    Operacion = Column(Enum("Create", "Read", "Update", "Delete"), nullable=False)
    Tabla = Column(String(50), nullable=False)
    Descripcion = Column(Text, nullable=False)
    Estatus = Column(Boolean, default=True)
    Fecha_Registro = Column(DateTime, nullable=False)
