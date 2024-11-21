import gradio as gr
import os
import json

import DataframeOps
import Arguments
import Server

args = Arguments.parse_args()
df = DataframeOps.initialize_dataframe()


def get_files(directory):
    json_list = []

    for item in os.listdir(directory):
        full_path = os.path.join(directory, item)
        if os.path.isfile(full_path) and item.endswith(".json"):
            json_list.append(item.replace(".json", ""))

    return json_list


with gr.Blocks() as demo:
    with gr.Tabs():
        with gr.TabItem("Make Flashcard"):

            with gr.Row():
                msg_box = gr.Textbox(label="Message",
                                     interactive=False,
                                     scale=1)
                with gr.Column(scale=0):
                    btn_reboot_local = gr.Button("Reboot Locally")
                    btn_reboot_share = gr.Button("Reboot Publicly")

            with gr.Column():
                with gr.Row():
                    file_dropdown = gr.Dropdown(label="Existed Cards",
                                                choices=get_files(
                                                    args.card_path),
                                                interactive=True,
                                                scale=1)
                    btn_load_file = gr.Button("Load", scale=0)

                with gr.Row():
                    question_enter = gr.Textbox(label="New Question",
                                                interactive=True,
                                                scale=1)
                    answer_enter = gr.Textbox(label="New Answer",
                                              interactive=True,
                                              scale=1)
                    btn_add_card = gr.Button("Add Card", scale=0)

                with gr.Row():
                    dataframe_view = gr.DataFrame(value=df,
                                                  label="Editable Dataframe",
                                                  interactive=True,
                                                  scale=1)
                    with gr.Column(scale=0):
                        save_file_name = gr.Textbox(
                            label="Save Name",
                            interactive=True,
                        )
                        btn_save_df = gr.Button("Save")
        '''
        Binding functions to keys
        '''
        btn_add_card.click(
            fn=DataframeOps.add_card,
            inputs=[question_enter, answer_enter, dataframe_view],
            outputs=[dataframe_view])
        btn_load_file.click(fn=DataframeOps.load_dataframe,
                            inputs=[file_dropdown],
                            outputs=[dataframe_view])
        btn_reboot_local.click(fn=Server.restart_server_local,
                               inputs=None,
                               outputs=None)
        btn_reboot_share.click(fn=Server.restart_server_public,
                               inputs=None,
                               outputs=None)
        btn_save_df.click(fn=DataframeOps.save_dataframe,
                          inputs=[save_file_name, dataframe_view],
                          outputs=None)

if __name__ == "__main__":
    if args.share:
        print(demo.launch(share=True))
    else:
        demo.launch()
