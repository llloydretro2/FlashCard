import gradio as gr

import DataframeOps
import Arguments
import Server
import FileManage

args = Arguments.parse_args()
df = DataframeOps.initialize_dataframe()
df_id = DataframeOps.initialize_dataframe_id()

with gr.Blocks() as demo:
    
    # 添加卡片
    with gr.Tabs():
        with gr.TabItem("添加卡片"):

            msg_box_AC = gr.Textbox(label="信息", interactive=False, scale=1)
                                    
            with gr.Column():
                
                gr.Markdown("# 加载卡组")
                with gr.Row():
                    file_dropdown_AC = gr.Dropdown(label="卡组列表",
                                                choices=FileManage.get_files(
                                                    args.card_path),
                                                interactive=True,
                                                scale=1)
                    btn_load_file_AC = gr.Button("加载", scale=0)
                    
                    
                gr.Markdown("# 添加卡片")
                with gr.Row():
                    question_enter_AC = gr.Textbox(label="新的问题",
                                                interactive=True,
                                                scale=1)
                    answer_enter_AC = gr.Textbox(label="新的答案",
                                              interactive=True,
                                              scale=1)
                    btn_add_card_AC = gr.Button("将卡片加入到卡组", scale=0)
                
                gr.Markdown("# 卡组预览")
                with gr.Row():
                    dataframe_view_AC = gr.DataFrame(value=df,
                                                  interactive=False,
                                                  scale=1)
                    with gr.Column(scale=0):
                        save_file_name_AC = gr.Textbox(
                            label="保存卡组名",
                            interactive=True,
                        )
                        btn_save_df_AC = gr.Button("保存")
                        
        # 删除卡片
        with gr.TabItem("删除卡片"):
            msg_box_DC = gr.Textbox(label="信息", interactive=False, scale=1)
            
            with gr.Column():
                
                gr.Markdown("# 加载卡组")
                with gr.Row():
                    file_dropdown_DC = gr.Dropdown(label="卡组列表",
                                                choices=FileManage.get_files(
                                                    args.card_path),
                                                interactive=True,
                                                scale=1)
                    btn_load_file_DC = gr.Button("加载", scale=0)  
                
                gr.Markdown("# 卡组预览")
                with gr.Row():
                    dataframe_view_DC = gr.DataFrame(value=df_id,
                                                  interactive=False,
                                                  scale=1)  
                    
                    
                         
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
        Binding functions to keys: Add Card
        '''
        btn_add_card_AC.click(
            fn=DataframeOps.add_card,
            inputs=[question_enter_AC, answer_enter_AC, dataframe_view_AC],
            outputs=[dataframe_view_AC])
        btn_load_file_AC.click(fn=DataframeOps.load_dataframe,
                            inputs=[file_dropdown_AC],
                            outputs=[dataframe_view_AC])
        btn_save_df_AC.click(fn=DataframeOps.save_dataframe,
                          inputs=[save_file_name_AC, dataframe_view_AC],
                          outputs=[msg_box_AC, file_dropdown_AC])
        
        
        
        
        
        '''
        Binding functions to keys: Delete Card
        '''
        btn_load_file_DC.click(fn=DataframeOps.load_dataframe_id,
                            inputs=[file_dropdown_DC],
                            outputs=[dataframe_view_DC])
        
        
        
        
        
        
        
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
