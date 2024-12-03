import os
import gradio as gr

import Arguments

args = Arguments.parse_args()


def get_files():
    directory = args.card_path

    json_list = []

    for item in os.listdir(directory):
        full_path = os.path.join(directory, item)
        if os.path.isfile(full_path) and item.endswith(".json"):
            json_list.append(item.replace(".json", ""))

    return json_list


def delete_file(file_name):

    directory = args.card_path

    file_path = os.path.join(directory, f'{file_name}.json')
    os.remove(file_path)
    return gr.update(value="删除成功"), gr.update(choices=get_files()), gr.update(
        choices=get_files())
