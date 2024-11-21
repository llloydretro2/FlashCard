import gradio as gr
import pandas as pd
import os
import sys
import json
import DataframeOps

CARDS_PATH = 'Cards'

def get_files(directory):
    try:
        return [
            d for d in os.listdir(directory)
            if os.path.isfile(os.path.join(directory, d))
        ]
    except Exception as e:
        return []


with gr.Blocks() as demo:
    with gr.Tabs():
        with gr.TabItem("Make Flashcard"):
            with gr.Column():
                with gr.Row():
                    file_dropdown = gr.Dropdown(label="Existed Cards",
                                                choices=get_files(CARDS_PATH),
                                                interactive=True,
                                                scale=1)
                    btn_load_file = gr.Button("Load",
                                              scale=0)

                with gr.Row():
                    dataframe_view = gr.DataFrame(value=DataframeOps.initialize_data_frame(),
                                                  label="Editable Dataframe",
                                                  interactive=True,
                                                  scale=1)
                    with gr.Column(scale=0):
                        btn_add_row = gr.Button("Add a Row", scale=0)
                        btn_save_df = gr.Button("Save", scale=0)

                with gr.Row():
                    msg_box = gr.Textbox(label="Message",
                                         interactive=False,
                                         scale=1)
                    btn_reboot = gr.Button("Reboot Tool",
                                           scale=0)

demo.launch()
