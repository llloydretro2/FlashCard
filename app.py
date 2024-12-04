import gradio as gr

import DataframeOps
import Arguments
import Server
import FileManage

args = Arguments.parse_args()
df_init = DataframeOps.initialize_dataframe_id()

with gr.Blocks(theme=gr.themes.Monochrome()) as demo:

    # 编辑卡片
    with gr.Tabs():
        with gr.TabItem("编辑卡片"):

            msg_box_EDIT = gr.Textbox(label="信息", interactive=False, scale=1)

            with gr.Column():

                gr.Markdown("# 选择加载卡组")
                with gr.Row():
                    file_dropdown_EDIT = gr.Dropdown(
                        label="卡组列表",
                        choices=FileManage.get_files(),
                        interactive=True,
                        scale=1)
                    btn_load_file_EDIT = gr.Button("加载", scale=0)

                gr.Markdown("# 添加卡片")
                with gr.Row():
                    question_enter_EDIT = gr.Textbox(label="新的问题",
                                                     interactive=True,
                                                     scale=1)
                    answer_enter_EDIT = gr.Textbox(label="新的答案",
                                                   interactive=True,
                                                   scale=1)
                    btn_add_card_EDIT = gr.Button("将卡片加入到卡组", scale=0)

                gr.Markdown("# 卡组预览")
                with gr.Row():
                    dataframe_view_EDIT = gr.DataFrame(value=df_init,
                                                       interactive=False,
                                                       scale=1)
                    with gr.Column(scale=0):

                        gr.Markdown("# 删除卡片")
                        with gr.Row():
                            delete_choice_EDIT = gr.Dropdown(label="问题ID",
                                                             choices=[],
                                                             interactive=True,
                                                             scale=1)
                            btn_delete_card_EDIT = gr.Button("删除卡片", scale=0)

                        gr.Markdown("# 保存卡组")
                        with gr.Row():
                            save_file_name_EDIT = gr.Textbox(label="保存卡组名",
                                                             interactive=True,
                                                             scale=1)
                            btn_save_df_EDIT = gr.Button("保存", scale=0)

                        gr.Markdown("# 删除卡组")
                        with gr.Row():
                            file_dropdown_DELETE = gr.Dropdown(
                                label="卡组列表",
                                choices=FileManage.get_files(),
                                interactive=True,
                                scale=1)
                            btn_delete_file = gr.Button("删除", scale=0)

        # 复习卡片
        with gr.TabItem("复习卡片"):

            gr.Markdown("# 加载卡组")
            with gr.Row():
                with gr.Column(scale=1):
                    gr.Markdown("## 1️⃣选择卡组")
                    file_dropdown_RC = gr.Dropdown(label="卡组列表",
                                               choices=FileManage.get_files(),
                                               interactive=True,
                                               scale=1)
                    deck_stats_RC = gr.Textbox(label="卡组统计",
                                           interactive=False,
                                           scale=1)
                with gr.Column(scale=0):
                    gr.Markdown("<h2 style='text-align: center;'>2️⃣选择模式</h2>")
                    btn_review_all_RC = gr.Button("复习全部")
                    btn_review_last_time_RC = gr.Button("复习上次错误项")
                    btn_review_today_RC = gr.Button("复习今天未复习项")
            btn_start_review_RC = gr.Button("3️⃣确认开始")


            gr.Markdown("---")  # 添加分割线

            gr.Markdown("# 复习卡片")
            with gr.Row():
                question_box_RC = gr.Textbox(label="问题",
                                             interactive=False,
                                             lines=10,
                                             scale=1)
                with gr.Column(scale=0):
                    gr.Markdown("<div style='height: 50px;'></div>")  # 添加空白区域
                    progress_RC = gr.Markdown(
                        value="<div style='text-align: center;'>进度: 0/0</div>")
                    btn_show_answer_RC = gr.Button("显示答案", elem_id="show-answer-button")
                answer_box_RC = gr.Textbox(label="答案",
                                           interactive=False,
                                           lines=10,
                                           scale=1)

            with gr.Row():
                btn_right_RC = gr.Button("正确", elem_id="right-button")
                btn_wrong_RC = gr.Button("错误", elem_id="wrong-button")

            current_card_id_RC = gr.Textbox(label="当前卡片ID", interactive=False)
            df_RC = gr.DataFrame(value=df_init, interactive=False)

        # 服务器管理
        with gr.TabItem("服务器管理"):
            with gr.Column():
                with gr.Row():
                    btn_reboot_local = gr.Button("重启本地服务器", scale=0)
                    btn_reboot_share = gr.Button("重启共享服务器", scale=0)

        # 编辑卡组
        btn_add_card_EDIT.click(fn=DataframeOps.add_card,
                                inputs=[
                                    question_enter_EDIT, answer_enter_EDIT,
                                    dataframe_view_EDIT
                                ],
                                outputs=[dataframe_view_EDIT, msg_box_EDIT])
        btn_load_file_EDIT.click(
            fn=DataframeOps.load_dataframe_edit,
            inputs=[file_dropdown_EDIT],
            outputs=[dataframe_view_EDIT, delete_choice_EDIT])
        btn_save_df_EDIT.click(
            fn=DataframeOps.save_dataframe,
            inputs=[
                save_file_name_EDIT, file_dropdown_EDIT, dataframe_view_EDIT
            ],
            outputs=[msg_box_EDIT, file_dropdown_EDIT, file_dropdown_DELETE])
        btn_delete_card_EDIT.click(
            fn=DataframeOps.delete_card_id,
            inputs=[delete_choice_EDIT, dataframe_view_EDIT],
            outputs=[msg_box_EDIT, dataframe_view_EDIT, delete_choice_EDIT])
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

        # 服务器管理
        btn_reboot_local.click(fn=Server.restart_server_local,
                               inputs=None,
                               outputs=None)
        btn_reboot_share.click(fn=Server.restart_server_public,
                               inputs=None,
                               outputs=None)

if __name__ == "__main__":

    demo.css = """
    #review-all-button {
        background-color: #4CAF50; /* 绿色 */
        color: white;
    }
    #review-last-time-button {
        background-color: #f44336; /* 红色 */
        color: white;
    }
    #review-today-button {
        background-color: #008CBA; /* 蓝色 */
        color: white;
    }
    #start-review-button {
        background-color: #e7e7e7; /* 灰色 */
        color: black;
        font-size: 15px;
        padding: 20px 60px;
    }
    #show-answer-button {
        background-color: #555555; /* 深灰色 */
        color: white;
        font-size: 15px;
        padding: 20px 60px;
    }
    #right-button {
        background-color: #4CAF50; /* 绿色 */
        color: white;
    }
    #wrong-button {
        background-color: #f44336; /* 红色 */
        color: white;
    }
    #update-progress-button {
        background-color: #008CBA; /* 蓝色 */
        color: white;
    }
    """

    if args.share:
        print(demo.launch(share=True, allowed_paths=["/"]))
    else:
        demo.launch(allowed_paths=["/"])
