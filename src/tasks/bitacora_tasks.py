from sqlalchemy import desc
from src.models.index_models import Bitacora
from sqlalchemy.orm import Session
from src.db.db_mysql import databaseMysql
from src.websockets.ws_manager import ws_manager
from src.dao.grupos_sanguineos_dao import grupos_sanguineos_dao

# =========================
# CONFIGURACIÓN
# =========================
last_bitacora_id = 0
MODO_DETALLADO = True  # ✅ Puedes prenderlo o apagarlo

def revisar_bitacora():
    global last_bitacora_id

    db: Session = next(databaseMysql.get_db())
    try:
        # Traer registros nuevos desde el último procesado
        entradas = (
            db.query(Bitacora)
            .filter(Bitacora.ID > last_bitacora_id)
            .order_by(Bitacora.ID)  # De abajo hacia arriba
            .limit(50)
            .all()
        )

        if not entradas:
            return

        personas_detectadas = [
            entrada for entrada in entradas if entrada.Tabla == "tbb_personas"
        ]

        if not personas_detectadas:
            # Si no hubo registros de personas, actualizar last_id
            last_bitacora_id = max(entrada.ID for entrada in entradas)
            return

        if MODO_DETALLADO and len(personas_detectadas) <= 3:
            # 🔥 Si solo detectamos pocos inserts, mandamos WS por cada uno
            for entrada in personas_detectadas:
                print(f"🟢 Enviando WS detallado por {entrada.Operacion}")
                grupo_sanguineos = grupos_sanguineos_dao.obtener_todos(db)
                ws_manager.broadcast_sync({
                    "message": f"Cambio en personas: {entrada.Operacion}",
                    "grupo_sanguineo": grupo_sanguineos
                }, ["Administrador"])
        else:
            # ✅ Consolidado
            print(f"🔔 Se detectó {len(personas_detectadas)} cambios en personas. Enviando solo un WS.")
            grupo_sanguineos = grupos_sanguineos_dao.obtener_todos(db)
            ws_manager.broadcast_sync({
                "message": "Actualización de personas detectada",
                "grupo_sanguineo": grupo_sanguineos
            }, ["Administrador"])

        # Actualizar last_id al máximo procesado
        last_bitacora_id = max(entrada.ID for entrada in entradas)

    finally:
        db.close()
