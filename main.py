import gradio as gr
import pandas as pd
import os
import sys




with gr.Blocks() as demo:
    with gr.Tabs():
        with gr.TabItem("tab_1"):
            with gr.Column():
                with gr.Row():
                    file_input = gr.Textbox(label="Enter the csv/excel file address",
                                            placeholder="file address",
                                            value="",
                                            scale=1)
                    btn_load_file = gr.Button("Load",
                                              scale=0)

                dataframe_view = gr.DataFrame(value=pd.DataFrame(), label="Editable Dataframe", interactive=True)
                btn_save_df = gr.Button("Save")







demo.launch()
