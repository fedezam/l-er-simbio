import gradio as gr
from tools.base_entity import BaseEntity
import importlib
import inspect
import os
from pathlib import Path
from typing import Dict

# Carga din_mica de entidades
def cargar_entidades_dinamicamente(ruta: str = "./tools/entidades") -> Dict[str, BaseEntity]:
    entidades = {}
    ruta_absoluta = Path(ruta).resolve()

    for archivo in os.listdir(ruta_absoluta):
        if archivo.endswith(".py") and not archivo.startswith("__"):
            nombre_modulo = archivo[:-3]
            modulo_path = f"tools.entidades.{nombre_modulo}"

            modulo = importlib.import_module(modulo_path)

            for nombre, objeto in inspect.getmembers(modulo, inspect.isclass):
                if issubclass(objeto, BaseEntity) and objeto != BaseEntity:
                    instancia = objeto()
                    entidades[instancia.name] = instancia
    return entidades


class EntityChatSystem:
    def __init__(self):
        self.entities = cargar_entidades_dinamicamente()
        self.selected_entity = list(self.entities.keys())[0] if self.entities else None

    def switch_entity(self, entity_name):
        self.selected_entity = entity_name

    def chat(self, input_text, history):
        entity = self.entities[self.selected_entity]
        response = entity.generate_response(input_text, history)
        history.append((input_text, response))
        return history, history

    def launch_ui(self):
        with gr.Blocks(title="Entity Chat System") as demo:
            gr.Markdown("# _ Sistema de Chat con Entidades Reflexivas")

            with gr.Row():
                entity_selector = gr.Dropdown(choices=list(self.entities.keys()),
                                              value=self.selected_entity,
                                              label="Selecciona una entidad",
                                              interactive=True)

            chatbot = gr.Chatbot(label="Di_logo")
            msg = gr.Textbox(label="Mensaje")

            clear = gr.Button("_ Limpiar conversaci_n")

            state = gr.State([])

            entity_selector.change(fn=self.switch_entity, inputs=entity_selector)

            msg.submit(self.chat, [msg, state], [chatbot, state])
            clear.click(lambda: ([], []), None, [chatbot, state])

        demo.launch()


if __name__ == "__main__":
    chat_system = EntityChatSystem()
    chat_system.launch_ui()
