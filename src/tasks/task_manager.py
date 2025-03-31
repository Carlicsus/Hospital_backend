import asyncio
from src.tasks.bitacora_tasks import revisar_bitacora
from src.tasks.citas_task import revisar_citas_medicas

def iniciar_tareas_background(loop):
    """
    Registra todas las tareas en segundo plano.
    """
    loop.create_task(_verificar_bitacora_periodicamente())
    loop.create_task(_verificar_citas_periodicamente())

async def _verificar_bitacora_periodicamente():
    while True:
        revisar_bitacora()
        await asyncio.sleep(4)

async def _verificar_citas_periodicamente():
    while True:
        revisar_citas_medicas()
        await asyncio.sleep(4)
