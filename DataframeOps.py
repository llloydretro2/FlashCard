import pandas as pd
import os
import gradio as gr

EXAMPLE_QUESTION = 'What is apple'
EXAMPLE_ANSWER = 'Fruit'
CARD_PATH = 'Cards'


def initialize_dataframe():

    df = pd.DataFrame({
        "Questions": [EXAMPLE_QUESTION],
        "Answers": [EXAMPLE_ANSWER]
    })

    return df


'''
加载的地方要大改，然后得用read_json_dumps才行，这样的话才能更好的把记录一起保存到卡片里面
然后加载的时候只给外面看卡片的问题的答案，直接掠过别的部分
'''


def load_dataframe(file):

    file_path = os.path.join(CARD_PATH, f'{file}.json')
    df = pd.read_json(file_path)

    return gr.update(value=df)


def add_card(question, answer, df_component):
    df_value = df_component.values

    question_list = []
    answer_list = []

    for i in df_value:
        print(i, len(i))
        if (i[0] == EXAMPLE_QUESTION
                and i[1] == EXAMPLE_ANSWER) or (i[0] == '' or i[1] == ''):
            continue
        question_list.append(i[0])
        answer_list.append(i[1])

    new_df = pd.DataFrame({
        "Questions": question_list + [question],
        "Answers": answer_list + [answer]
    })

    return gr.update(value=new_df)


'''
保存卡片的逻辑应该是如果有没有的条目，那么就初始化，
如果是已经有的条目就按照原本的办法保存他，
增加卡片的部分不应该影响做题的记录。
'''


def save_dataframe(file_name, df_component):
    df_value = df_component.values

    data = []
    for i in df_value:
        data.append({"Questions": i[0], "Answers": i[1]})

    df = pd.DataFrame(data)
    print(df)

    df.to_json(f"{CARD_PATH}/{file_name}.json")

    return
