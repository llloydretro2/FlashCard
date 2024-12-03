import pandas as pd
import os
import gradio as gr
import json
import random
from datetime import datetime

import FileManage
import Arguments

args = Arguments.parse_args()
'''
一张卡片的结构为
{
    "ID": ID
    "Question": 问题,
    "Answer" : 答案,
    "Records":[
        ["某一时间戳", 0/1], [“某一时间戳”, ...], ... (0为错误，1为正确)
    ]
}
'''


def initialize_dataframe_id():

    df = pd.DataFrame({"ID": [], "Questions": [], "Answers": []})

    return df


def load_dataframe_edit(file):

    file_path = os.path.join(args.card_path, f'{file}.json')
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

    file_path = os.path.join(args.card_path, f'{save_file_name}.json')

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
        choices=FileManage.get_files()), gr.update(
            choices=FileManage.get_files())


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


def review_all(file):

    file_path = os.path.join(args.card_path, f'{file}.json')
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
        "Records": record_list,
        "Status": [0] * len(id_list)
    })
    print('处理后数据:', df)

    deck_status_msg = f"卡组[{file}]加载成功🎉\n共{len(id_list)}张卡🃏\n本次需要复习{len(id_list)}张卡片"

    return gr.update(value=df), gr.update(value=deck_status_msg)


def df_to_list(df):
    df_value = df.values
    print("原数据:\n", df_value)

    question_list = []
    answer_list = []
    record_list = []
    status_list = []

    for i in df_value:
        question_list.append(i[1])
        answer_list.append(i[2])
        record_list.append(i[3])
        status_list.append(i[4])

    return question_list, answer_list, record_list, status_list


def get_new_card_id(df):
    question_list, answer_list, record_list, status_list = df_to_list(df)

    # 从未复习的卡片中随机选取一张
    unreviewed_id_list = []
    for i in range(len(status_list)):
        if status_list[i] == 0:
            unreviewed_id_list.append(i)

    if len(unreviewed_id_list) == 0:
        return gr.update(value=0)

    random_id = random.choice(unreviewed_id_list)
    return random_id


def pick_card(df):

    random_id = get_new_card_id(df)
    return gr.update(value=random_id)


def show_question(df, card_id):
    question_list, answer_list, record_list, status_list = df_to_list(df)
    question = question_list[int(card_id)]
    return gr.update(value=question)


def show_answer(df, card_id):

    question_list, answer_list, record_list, status_list = df_to_list(df)
    answer = answer_list[int(card_id)]
    return gr.update(value=answer)


def set_correct(df, card_id):
    question_list, answer_list, record_list, status_list = df_to_list(df)

    time_stemp = datetime.now().strftime('%Y-%m-%d')
    record_list[int(card_id)].append([time_stemp, 1])
    status_list[int(card_id)] = 1

    # 更新 DataFrame
    df.at[int(card_id), "Records"] = record_list[int(card_id)]
    df.at[int(card_id), "Status"] = status_list[int(card_id)]

    random_id = get_new_card_id(df)

    return gr.update(value=random_id), gr.update(value=df)


def set_wrong(df, card_id):
    question_list, answer_list, record_list, status_list = df_to_list(df)

    time_stemp = datetime.now().strftime('%Y-%m-%d')
    record_list[int(card_id)].append([time_stemp, 0])

    # 更新 DataFrame
    df.at[int(card_id), "Records"] = record_list[int(card_id)]

    # 错的时候尽量不要选同一个ID
    unreviewed_id_list = []
    for i in range(len(status_list)):
        if status_list[i] == 0:
            unreviewed_id_list.append(i)
    random_id = get_new_card_id(df)
    while random_id == int(card_id) and len(unreviewed_id_list) > 1:
        random_id = get_new_card_id(df)

    return gr.update(value=random_id), gr.update(value=df)


def update_progress(df):

    try:
        question_list, answer_list, record_list, status_list = df_to_list(df)

        total = len(status_list)
        reviewed = status_list.count(1)

        return gr.update(
            value=
            f"<div style='text-align: center;'>进度:{reviewed} / {total}</div>")

    except:
        return gr.update(
            value="<div style='text-align: center;'>进度: 0 / 0</div>")
