"""Ingeniero de pruebas: edita aquí las instrucciones de revisión."""

from graph.state import WorkflowState
from graph.context import _ctx, _const_block, _feedback_block


INSTRUCTIONS = 'Relaciona cada criterio de aceptación con una prueba y su resultado esperado.\n' \
'Incluye casos positivos, negativos, de borde e integración.\n' \
'Detalla preparación, datos de prueba, comandos y limpieza.\n' \
'Comprueba los contratos de API y persistencia y las correcciones propuestas.\n' \
'Marca NO EJECUTADO cuando no tengas una salida real. No inventes resultados.\n' \
'Devuelve un informe con cobertura por criterio, pruebas propuestas, comandos y resultados reales o NO EJECUTADO.'


def testing_node(state: WorkflowState, invoke) -> dict:
    prompt = (INSTRUCTIONS 
              + _const_block(state, "Respeta las restricciones del proyecto y la constitución.") 
              + "\nRepositorio: " + state["repo_name"] 
              + "\nPlan:\n" + _ctx(state.get("out_plan", ""),2500) 
              + "\nCódigo original:\n" + _ctx(state.get("snapshot", ""),4000) 
              + "\nBackend:\n" + _ctx(state.get("out_backend", ""),6000) 
              + "\nFrontend:\n" + _ctx(state.get("out_frontend", ""),6000) 
              + _feedback_block(state) + '\nDevuelve un informe de tu rol.')
    if state.get("include_data"):
        prompt += "\nContrato aprobado de Datos y persistencia:\n" + _ctx(state.get("out_data", ""), 6000)
    return {"out_testing": invoke(prompt)}
