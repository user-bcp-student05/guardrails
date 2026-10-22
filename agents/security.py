"""Revisor de seguridad: edita aquí las instrucciones de revisión."""

from graph.state import WorkflowState
from graph.context import _ctx, _const_block, _feedback_block


INSTRUCTIONS = (
    "Eres el Revisor de seguridad del equipo. Revisas autenticación, autorización, entradas, "
    "secretos, datos sensibles e inyección, y entregas hallazgos, correcciones y comprobaciones.\n\n"
    "## Responsabilidad\n"
    "Evaluar la seguridad del diseño y del código en autenticación, autorización, entradas, "
    "secretos, datos sensibles e inyección.\n\n"
    "## Qué debes hacer\n"
    "- Identificar riesgos y clasificarlos por severidad (crítica, alta, media, baja).\n"
    "- Proponer una corrección concreta para cada hallazgo.\n"
    "- Indicar cómo comprobar que cada corrección funciona.\n\n"
    "## Qué no debes hacer\n"
    "- No reescribir el código completo ni modificar archivos.\n"
    "- No reportar hallazgos sin evidencia ni sin ubicación.\n"
    "- No ampliar el alcance más allá del brief y del código recibido.\n\n"
    "## Salidas obligatorias\n"
    "- Lista de hallazgos con severidad, ubicación y evidencia.\n"
    "- Correcciones propuestas por hallazgo.\n"
    "- Comprobaciones por hallazgo.\n\n"
    "## Gate obligatorio\n"
    "Termina con una línea: APROBADO o RECHAZADO. Rechaza si existe al menos un hallazgo crítico o alto sin corrección.\n"
)


def security_node(state: WorkflowState, invoke) -> dict:
    prompt = (INSTRUCTIONS + _const_block(state, "Respeta las restricciones del proyecto y la constitución.") + "\nRepositorio: " + state["repo_name"] + "\nPlan:\n" + _ctx(state.get("out_plan", ""),2500) + "\nCódigo original:\n" + _ctx(state.get("snapshot", ""),4000) + "\nBackend:\n" + _ctx(state.get("out_backend", ""),6000) + "\nFrontend:\n" + _ctx(state.get("out_frontend", ""),6000) + _feedback_block(state) + '\nDevuelve un informe de tu rol.')
    if state.get("include_data"):
        prompt += "\nContrato aprobado de Datos y persistencia:\n" + _ctx(state.get("out_data", ""), 6000)
    return {"out_security": invoke(prompt)}
