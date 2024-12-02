import pandas as pd
import os
import gradio as gr
import json

import FileManage

CARD_PATH = 'Cards'
'''
一张卡片的结构为
{
    "ID": ID
    "Question": 问题,
    "Answer" : 答案,
    "某一时间戳": 0/1, 0为错误，1为正确,
    “某一时间戳”: ... ,
    ...
}
那么读取卡片的时候只会读取[问题]和[答案]
'''


def initialize_dataframe_id():

    df = pd.DataFrame({"ID": [], "Questions": [], "Answers": []})

    return df


def load_dataframe_edit(file):

    file_path = os.path.join(CARD_PATH, f'{file}.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    card_data = data['cards']
    print('卡片原数据:\n', card_data)

    question_list = []
    answer_list = []
    record_list = []
    for item in card_data:
        question_list.append(item["Question"])
        answer_list.append((item["Answer"]))
        record_list.append(item["Records"])
    id_list = list(range(1, len(question_list) + 1))

    df = pd.DataFrame({
        "ID": id_list,
        "Questions": question_list,
        "Answers": answer_list,
        "Records": record_list
    })
    print('处理后数据:', df)

    return gr.update(value=df), gr.update(choices=id_list)


def add_card(question, answer, df_component):

    # 如果新增的卡片不完整，直接返回
    if question == '' or answer == '':
        return gr.update(), gr.update(value="卡片不完整，请重新输入")

    df_value = df_component.values

    question_list = []
    answer_list = []
    record_list = []

    for i in df_value:
        if (i[1] == '' or i[2] == ''):
            continue
        question_list.append(i[1])
        answer_list.append(i[2])
        record_list.append(i[3])

    new_qestion_list = question_list + [question]
    new_answer_list = answer_list + [answer]
    new_record_list = record_list + [[]]
    id_list = list(range(1, len(new_qestion_list) + 1))

    new_df = pd.DataFrame({
        "ID": id_list,
        "Questions": new_qestion_list,
        "Answers": new_answer_list,
        "Records": new_record_list
    })

    print("After Adding Card:\n", new_df)

    return gr.update(value=new_df), gr.update(value="卡片添加成功")


def save_dataframe(save_file_name, load_file_name, df_component):

    if save_file_name == '':
        save_file_name = load_file_name

    file_path = os.path.join(CARD_PATH, f'{save_file_name}.json')

    df_value = df_component.values

    new_json_data = {"cards": []}

    for i in df_value:
        if (i[1] == '' or i[2] == ''):
            continue
        temp_card = {
            "ID": i[0],
            "Question": i[1],
            "Answer": i[2],
            "Records": i[3]
        }
        new_json_data["cards"].append(temp_card)

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(new_json_data, f, ensure_ascii=False, indent=4)

    return gr.update(value=f"保存成功至{save_file_name}"), gr.update(
        choices=FileManage.get_files(CARD_PATH))


def delete_card_id(id, df_component):

    df_value = df_component.values
    print("原数据:\n", df_value)

    question_list = []
    answer_list = []
    record_list = []

    for i in df_value:
        if i[0] == id:
            continue
        question_list.append(i[1])
        answer_list.append(i[2])
        record_list.append(i[3])
    id_list = list(range(1, len(question_list) + 1))

    new_df = pd.DataFrame({
        "ID": id_list,
        "Questions": question_list,
        "Answers": answer_list,
        "Records": record_list
    })

    print("处理后数据:\n", new_df)

    return gr.update(value=f"已删除卡片{id}"), gr.update(value=new_df), gr.update(
        choices=id_list)
