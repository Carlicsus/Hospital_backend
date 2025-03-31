from sqlalchemy.orm import Session
from sqlalchemy import desc
from src.models.citas_medicas_model import CitaMedica
from src.db.db_mysql import databaseMysql
from src.websockets.ws_manager import ws_manager

# =========================
# CONFIGURACIÓN
# =========================
last_cita_id = None
MODO_DETALLADO = True  # ✅ Si quieres notificar cita por cita

def revisar_citas_medicas():
    """
    Revisa nuevos registros de citas médicas y notifica al médico correspondiente.
    """
    global last_cita_id

    db: Session = next(databaseMysql.get_db())
    try:
        query = db.query(CitaMedica).order_by(CitaMedica.fecha_registro.asc())

        if last_cita_id:
            query = query.filter(CitaMedica.id > last_cita_id)

        nuevas_citas = query.limit(20).all()

        if not nuevas_citas:
            return

        citas_por_medico = {}

        for cita in nuevas_citas:
            medico_id = str(cita.personal_medico.persona_id)
            if medico_id not in citas_por_medico:
                citas_por_medico[medico_id] = []
            citas_por_medico[medico_id].append({
                "id": cita.id,
                "folio": cita.folio,
                "tipo": cita.tipo,
                "estatus": cita.estatus,
                "fecha_programada": str(cita.fecha_programada),
                "observaciones": cita.observaciones
            })

        # Enviar notificación al médico correspondiente
        for medico_id, citas in citas_por_medico.items():
            client_id = ws_manager.user_client_map.get(medico_id)
            if client_id:
                if MODO_DETALLADO:
                    # Un WS por cada cita
                    for cita in citas:
                        ws_manager.send_message_to_client_sync(client_id, {
                            "message": "Nueva cita médica registrada",
                            "cita": cita
                        })
                else:
                    # Consolidado
                    ws_manager.send_message_to_client_sync(client_id, {
                        "message": "Tienes nuevas citas médicas",
                        "citas": citas
                    })

        # Actualizar el último ID procesado
        last_cita_id = max(cita.id for cita in nuevas_citas)

    finally:
        db.close()
