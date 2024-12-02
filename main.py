import gradio as gr

import DataframeOps
import Arguments
import Server
import FileManage

args = Arguments.parse_args()
df_id = DataframeOps.initialize_dataframe_id()

with gr.Blocks() as demo:

    # 编辑卡片
    with gr.Tabs():
        with gr.TabItem("编辑卡片"):

            msg_box_EDIT = gr.Textbox(label="信息", interactive=False, scale=1)

            with gr.Column():

                gr.Markdown("# 加载卡组")
                with gr.Row():
                    file_dropdown_EDIT = gr.Dropdown(
                        label="卡组列表",
                        choices=FileManage.get_files(args.card_path),
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
                    dataframe_view_EDIT = gr.DataFrame(value=df_id,
                                                       interactive=False,
                                                       scale=1)
                    with gr.Column(scale=0):

                        gr.Markdown("# 删除卡片")
                        delete_choice_EDIT = gr.Dropdown(label="问题ID",
                                                         choices=[],
                                                         interactive=True,
                                                         scale=1)
                        btn_delete_card_EDIT = gr.Button("删除卡片")

                        gr.Markdown("# 保存卡组")
                        save_file_name_EDIT = gr.Textbox(
                            label="保存卡组名",
                            interactive=True,
                        )
                        btn_save_df_EDIT = gr.Button("保存")

        # 浏览卡片
        with gr.TabItem("浏览卡片"):
            msg_box_BC = gr.Textbox(label="信息", interactive=False, scale=1)

        # 复习卡片
        with gr.TabItem("复习卡片"):
            msg_box_RC = gr.Textbox(label="信息", interactive=False, scale=1)

        # 服务器管理
        with gr.TabItem("服务器管理"):
            with gr.Column():
                with gr.Row():
                    btn_reboot_local = gr.Button("重启本地服务器", scale=0)
                    btn_reboot_share = gr.Button("重启共享服务器", scale=0)
        '''
        Binding functions to keys: Edit Card
        '''
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
        btn_save_df_EDIT.click(fn=DataframeOps.save_dataframe,
                               inputs=[
                                   save_file_name_EDIT, file_dropdown_EDIT,
                                   dataframe_view_EDIT
                               ],
                               outputs=[msg_box_EDIT, file_dropdown_EDIT])
        btn_delete_card_EDIT.click(
            fn=DataframeOps.delete_card_id,
            inputs=[delete_choice_EDIT, dataframe_view_EDIT],
            outputs=[msg_box_EDIT, dataframe_view_EDIT, delete_choice_EDIT])
        '''
        Binding functions to keys: Server Management
        '''
        btn_reboot_local.click(fn=Server.restart_server_local,
                               inputs=None,
                               outputs=None)
        btn_reboot_share.click(fn=Server.restart_server_public,
                               inputs=None,
                               outputs=None)

if __name__ == "__main__":
    if args.share:
        print(demo.launch(share=True))
    else:
        demo.launch()
