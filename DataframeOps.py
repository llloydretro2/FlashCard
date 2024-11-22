import pandas as pd
import os
import gradio as gr
import json

import FileManage

EXAMPLE_QUESTION = 'What is apple'
EXAMPLE_ANSWER = 'Fruit'
CARD_PATH = 'Cards'
'''
一张卡片的结构为
{
    "Question": 问题,
    "Answer" : 答案,
    "某一时间戳": 0/1, 0为错误，1为正确,
    “某一时间戳”: ... ,
    ...
}
那么读取卡片的时候只会读取[问题]和[答案]
'''


def initialize_dataframe():

    df = pd.DataFrame({
        "Questions": [],
        "Answers": []
    })

    return df

def initialize_dataframe_id():

    df = pd.DataFrame({
        "ID": [],
        "Questions": [],
        "Answers": []
    })

    return df


def load_dataframe(file):

    file_path = os.path.join(CARD_PATH, f'{file}.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    card_data = data['cards']
    print(data)
    print(card_data)

    question_list = []
    answer_list = []
    for item in card_data:
        question_list.append(item["Question"])
        answer_list.append((item["Answer"]))

    df = pd.DataFrame({"Questions": question_list, "Answers": answer_list})

    return gr.update(value=df)

def load_dataframe_id(file):

    file_path = os.path.join(CARD_PATH, f'{file}.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    card_data = data['cards']
    print(data)
    print(card_data)

    question_list = []
    answer_list = []
    for item in card_data:
        question_list.append(item["Question"])
        answer_list.append((item["Answer"]))
    id_list = list(range(1, len(question_list) + 1))

    df = pd.DataFrame({"ID": id_list, "Questions": question_list, "Answers": answer_list})

    return gr.update(value=df)




def add_card(question, answer, df_component):
    df_value = df_component.values

    question_list = []
    answer_list = []

    for i in df_value:
        if (i[0] == EXAMPLE_QUESTION
                and i[1] == EXAMPLE_ANSWER) or (i[0] == '' or i[1] == ''):
            continue
        question_list.append(i[0])
        answer_list.append(i[1])

    new_df = pd.DataFrame({
        "Questions": question_list + [question],
        "Answers": answer_list + [answer]
    })

    return gr.update(value=new_df), gr.update(value="卡片添加成功")


'''
保存卡片的逻辑应该是如果有没有的条目，那么就初始化，
如果是已经有的条目就按照原本的办法保存他，
增加卡片的部分不应该影响做题的记录。
'''


def save_dataframe(file_name, df_component):

    file_path = os.path.join(CARD_PATH, f'{file_name}.json')

    file_found = False
    json_card_data = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
            file_found = True
        json_card_data = json_data['cards']
    except FileNotFoundError:
        data = {"cards": []}

    df_value = df_component.values

    new_data = []
    for i in df_value:
        new_data.append({"Question": i[0], "Answer": i[1]})

    if file_found:
        combined_data = json_card_data + new_data
        print(combined_data)
        new_json_data = json_data
        new_json_data['cards'] = combined_data

    if not file_found:
        new_json_data = {'cards': new_data}

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(new_json_data, f, ensure_ascii=False, indent=4)

    return gr.update(value=f"保存成功至{file_name}"), gr.update(
        choices=FileManage.get_files(CARD_PATH))
