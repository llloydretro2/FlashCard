import gradio as gr

import DataframeOps
import Arguments
import FileManage

args = Arguments.parse_args()
df_init = DataframeOps.initialize_dataframe_id()

with gr.Blocks(theme=gr.themes.Monochrome(spacing_size="sm",
                                          radius_size="none"),
               css_paths="styles.css") as demo:

    # 编辑卡片
    with gr.Tabs():
        with gr.TabItem("编辑卡片"):

            with gr.Column():

                gr.Markdown("<h1 style='text-align: center;'>选择卡组</h1>")
                with gr.Row():
                    file_dropdown_EDIT = gr.Dropdown(
                        label="卡组列表",
                        choices=FileManage.get_files(),
                        interactive=True,
                        scale=1)
                    with gr.Column(scale=0):
                        btn_refresh_EDIT = gr.Button("刷新")
                        btn_load_file_EDIT = gr.Button("加载")
                        btn_new_deck_EDIT = gr.Button("新建卡组")
                gr.Markdown(
                    "<hr style='border: 1px solid #000; margin: 20px 0;'>")

                gr.Markdown("<h1 style='text-align: center;'>添加卡片</h1>")
                with gr.Row():
                    question_enter_EDIT = gr.Textbox(label="新的问题",
                                                     interactive=True,
                                                     scale=1)
                    answer_enter_EDIT = gr.Textbox(label="新的答案",
                                                   interactive=True,
                                                   scale=1)
                    btn_add_card_EDIT = gr.Button("将卡片加入到卡组", scale=0)

                gr.Markdown(
                    "<hr style='border: 1px solid #000; margin: 20px 0;'>")

                gr.Markdown("<h1 style='text-align: center;'>卡组预览</h1>")
                msg_box_EDIT = gr.Textbox(label="信息",
                                          interactive=False,
                                          scale=1)
                with gr.Row():
                    dataframe_view_EDIT = gr.DataFrame(value=df_init,
                                                       interactive=False,
                                                       scale=2)
                    with gr.Column(scale=1):

                        gr.Markdown(
                            "<h1 style='text-align: center;'>删除卡片</h1>")
                        delete_choice_DELETE = gr.Dropdown(label="问题ID",
                                                           choices=[],
                                                           interactive=True)
                        with gr.Row():
                            btn_refresh_DELETE = gr.Button("刷新")
                            btn_delete_card_DELETE = gr.Button("删除卡片")

                        gr.Markdown(
                            "<h1 style='text-align: center;'>保存卡组</h1>")
                        with gr.Row():
                            save_file_name_EDIT = gr.Textbox(label="保存卡组名",
                                                             interactive=True)
                            btn_save_df_EDIT = gr.Button("保存",
                                                         elem_id="save-button")

                        gr.Markdown(
                            "<h1 style='text-align: center;'>删除卡组</h1>")
                        with gr.Row():
                            file_dropdown_DELETE = gr.Dropdown(
                                label="卡组列表",
                                choices=FileManage.get_files(),
                                interactive=True)
                            btn_delete_file = gr.Button(
                                "删除", elem_id="delete-button")

        # 复习卡片
        with gr.TabItem("复习卡片"):

            gr.Markdown("<h1 style='text-align: center;'>加载卡组</h1>")
            with gr.Row():
                with gr.Column(scale=1):
                    gr.Markdown("## 1️⃣选择卡组")
                    file_dropdown_RC = gr.Dropdown(
                        label="卡组列表",
                        choices=FileManage.get_files(),
                        interactive=True,
                        scale=1)
                    deck_stats_RC = gr.Textbox(label="卡组统计",
                                               interactive=False,
                                               scale=1)
                    btn_refresh_RC = gr.Button("刷新")
                with gr.Column(scale=0):
                    gr.Markdown("<h2 style='text-align: center;'>2️⃣选择模式</h2>")
                    btn_review_all_RC = gr.Button("复习全部")
                    btn_review_last_time_RC = gr.Button("复习上次错误项")
                    btn_review_today_RC = gr.Button("复习今天未复习项")
            btn_start_review_RC = gr.Button("3️⃣确认开始")

            gr.Markdown("<hr style='border: 1px solid #000; margin: 20px 0;'>")

            gr.Markdown("<h1 style='text-align: center;'>复习卡片</h1>")
            with gr.Row():
                question_box_RC = gr.Textbox(label="问题",
                                             interactive=False,
                                             lines=10,
                                             scale=1)
                with gr.Column(scale=0):
                    gr.Markdown("<div style='height: 50px;'></div>")  # 添加空白区域
                    progress_RC = gr.Markdown(
                        value="<div style='text-align: center;'>进度: 0/0</div>")
                    btn_show_answer_RC = gr.Button(
                        "显示答案", elem_id="show-answer-button")
                    btn_save_progress_RC = gr.Button("保存进度")
                answer_box_RC = gr.Textbox(label="答案",
                                           interactive=False,
                                           lines=10,
                                           scale=1)

            with gr.Row():
                btn_right_RC = gr.Button("正确", elem_id="right-button")
                btn_wrong_RC = gr.Button("错误", elem_id="wrong-button")

            # 隐藏的组件，用于调试
            current_card_id_RC = gr.Textbox(label="当前卡片ID",
                                            interactive=False,
                                            visible=False)
            df_RC = gr.DataFrame(value=df_init,
                                 interactive=False,
                                 visible=False)

        # 编辑卡组
        btn_add_card_EDIT.click(fn=DataframeOps.add_card,
                                inputs=[
                                    question_enter_EDIT, answer_enter_EDIT,
                                    dataframe_view_EDIT
                                ],
                                outputs=[dataframe_view_EDIT, msg_box_EDIT])
        btn_refresh_EDIT.click(fn=FileManage.update_file_dropdown,
                               outputs=[file_dropdown_EDIT])
        btn_load_file_EDIT.click(
            fn=DataframeOps.load_dataframe_edit,
            inputs=[file_dropdown_EDIT],
            outputs=[dataframe_view_EDIT, delete_choice_DELETE])
        btn_new_deck_EDIT.click(fn=DataframeOps.create_new_deck,
                                outputs=[dataframe_view_EDIT, msg_box_EDIT])
        btn_save_df_EDIT.click(
            fn=DataframeOps.save_dataframe,
            inputs=[
                save_file_name_EDIT, file_dropdown_EDIT, dataframe_view_EDIT
            ],
            outputs=[msg_box_EDIT, file_dropdown_EDIT, file_dropdown_DELETE])
        btn_delete_card_DELETE.click(
            fn=DataframeOps.delete_card_id,
            inputs=[delete_choice_DELETE, dataframe_view_EDIT],
            outputs=[msg_box_EDIT, dataframe_view_EDIT, delete_choice_DELETE])
        btn_refresh_DELETE.click(fn=FileManage.update_file_dropdown,
                                 outputs=[delete_choice_DELETE])
        btn_delete_file.click(
            fn=FileManage.delete_file,
            inputs=[file_dropdown_DELETE],
            outputs=[msg_box_EDIT, file_dropdown_EDIT, file_dropdown_DELETE])

        # 复习卡片
        btn_review_all_RC.click(fn=DataframeOps.review_all,
                                inputs=[file_dropdown_RC],
                                outputs=[df_RC, deck_stats_RC])
        btn_review_last_time_RC.click(fn=DataframeOps.review_last_time,
                                      inputs=[file_dropdown_RC],
                                      outputs=[df_RC, deck_stats_RC])
        btn_review_today_RC.click(fn=DataframeOps.review_today,
                                  inputs=[file_dropdown_RC],
                                  outputs=[df_RC, deck_stats_RC])
        btn_start_review_RC.click(fn=DataframeOps.pick_card,
                                  inputs=[df_RC],
                                  outputs=[current_card_id_RC])
        current_card_id_RC.change(fn=DataframeOps.show_question,
                                  inputs=[df_RC, current_card_id_RC],
                                  outputs=[question_box_RC])
        btn_show_answer_RC.click(fn=DataframeOps.show_answer,
                                 inputs=[df_RC, current_card_id_RC],
                                 outputs=[answer_box_RC])
        btn_right_RC.click(fn=DataframeOps.set_correct,
                           inputs=[df_RC, current_card_id_RC],
                           outputs=[current_card_id_RC, df_RC, answer_box_RC])
        btn_wrong_RC.click(fn=DataframeOps.set_wrong,
                           inputs=[df_RC, current_card_id_RC],
                           outputs=[current_card_id_RC, df_RC, answer_box_RC])
        df_RC.change(fn=DataframeOps.update_progress,
                     inputs=[df_RC, file_dropdown_RC],
                     outputs=[progress_RC])
        btn_save_progress_RC.click(fn=DataframeOps.save_progress,
                                   inputs=[df_RC, file_dropdown_RC],
                                   outputs=[progress_RC])
        btn_refresh_RC.click(fn=FileManage.update_file_dropdown,
                             outputs=[file_dropdown_RC])

if __name__ == "__main__":

    if args.share:
        print(demo.launch(share=True, allowed_paths=["/"]))
    else:
        demo.launch(allowed_paths=["/"])
