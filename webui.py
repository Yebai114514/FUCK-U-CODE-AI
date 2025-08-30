import gradio as gr
from api import code_review_api
import json
import os

class BrightCourt(gr.themes.Base):
    def __init__(self):
        super().__init__(
            primary_hue=gr.themes.colors.blue,
            secondary_hue=gr.themes.colors.blue,
            neutral_hue=gr.themes.colors.gray,
            font=[gr.themes.GoogleFont("Inter"), "ui-sans-serif", "system-ui", "sans-serif"],
        )
        self.set(
            body_background_fill="#f0f0f0",
            body_background_fill_dark="#f0f0f0",
            body_text_color="#333333",

            background_fill_primary="#ffffff",
            background_fill_secondary="#f8f2f2",
            border_color_accent_dark="#cccccc",

            button_primary_background_fill="#0d6efd",
            button_primary_background_fill_hover="#0b5ed7",
            button_primary_text_color="white",

            button_secondary_background_fill="#e0e0e0",
            button_secondary_background_fill_hover="#d0d0d0",
            button_secondary_text_color="#333333",

            button_cancel_background_fill="#a0a0a0",
            button_cancel_background_fill_hover="#909090",

            input_background_fill="#ffffff",
            input_border_color="#cccccc",
            input_placeholder_color="#aaaaaa",

            block_radius="12px",
            block_shadow="0 4px 15px rgba(0,0,0,0.1)",
            block_title_background_fill="*background_fill_primary",

            slider_color="#0d6efd",
        )



def load_api_key_from_file(filepath="./assets/api_key.json"):
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f).get("api_key", "")
        except:
            return ""
    return ""


CSS = """
/* 全局基础样式 */
.gradio-container { 
    background-color: #f0f0f0 !important; 
    color: #333333 !important; 
    font-family: 'Inter', ui-sans-serif, system-ui, sans-serif;
    padding: 20px; /* 增加整体内边距 */
}
footer { display: none !important; } 

/* 结果显示区域样式 */
#result-markdown, #result-markdown-multi { 
    border-left: 3px solid #0d6efd; 
    padding-left: 20px; 
    background-color: #f8f8f8; 
    min-height: 400px; 
    color: #333333;
    border-radius: 8px; 
    box-shadow: 0 2px 8px rgba(0,0,0,0.05); 
    margin-top: 20px; /* 结果区和上面内容隔开 */
}
#result-markdown details, #result-markdown-multi details { 
    background-color: #ffffff; 
    border: 1px solid #e0e0e0; 
    margin-bottom: 10px; 
    border-radius: 6px; 
    color: #333333; 
    box-shadow: 0 1px 4px rgba(0,0,0,0.03); 
}
#result-markdown summary, #result-markdown-multi summary { 
    font-weight: bold; 
    cursor: pointer; 
    color: #0d6efd; 
    padding: 10px 15px; 
    background-color: #f0f0f0; 
    border-radius: 6px 6px 0 0;
}
#result-markdown summary:hover, #result-markdown-multi summary:hover {
    background-color: #e8e8e8; 
}

/* 标题样式 */
#main-title { 
    transition: all 0.3s ease; 
    margin-bottom: 20px; 
}
#main-title:hover { 
    box-shadow: 0 6px 20px rgba(13, 110, 253, 0.2) !important; 
}
#main-title h1 {
    font-size: 2.2em; 
    font-weight: 700;
}
#main-title p {
    font-size: 1.0em;
    font-weight: 300;
}

/* Markdown头部样式 */
.markdown-header h3 {
    border-bottom: 2px solid #0d6efd; 
    padding-bottom: 5px;
    margin-bottom: 15px;
    color: #222;
}

/* 错误与警告信息样式 */
.error { color: red; font-weight: bold; }
.warning { color: orange; font-weight: bold; }

/* Gradio Accordion 样式调整 */
.gradio-accordion {
    margin-bottom: 15px; 
    border-radius: 12px !important; 
    box-shadow: 0 2px 10px rgba(0,0,0,0.08); 
    border: 1px solid var(--border_color_accent_dark); 
    background-color: var(--background_fill_primary); 
}
.gradio-accordion > .label {
    font-weight: bold; 
    font-size: 1.1em;
    padding: 15px 20px; 
    background-color: var(--background_fill_secondary); 
    border-radius: 12px 12px 0 0 !important; 
    cursor: pointer;
    border-bottom: 1px solid var(--border_color_accent_dark); 
    color: var(--body_text_color); 
}
.gradio-accordion > .label.closed {
    border-radius: 12px !important; 
    border-bottom: none; 
}
.gradio-accordion > .label:hover {
    background-color: #e8e8e8; 
}
.gradio-accordion > .panel {
    padding: 20px; 
    border-radius: 0 0 12px 12px !important; 
    background-color: var(--background_fill_primary);
}
.gradio-accordion.closed > .panel {
    display: none; 
}


/* 响应式布局 */
@media screen and (max-width: 768px) {
    #main-layout { flex-direction: column; }
    .gradio-container { padding: 15px !important; }
    #main-title h1 { font-size: 1.8rem !important; }
}
"""


def review_single_file(api_key, model, temperature, max_output_tokens, custom_instruction_prompt, file_obj):
    """
    处理单个代码文件的评审请求。
    """
    if file_obj is None: return "<div class='error'>请上传文件。</div>"
    try:
        filename = os.path.basename(file_obj.name)
        with open(file_obj.name, 'r', encoding='utf-8') as f:
            code_content = f.read()
        if not code_content.strip(): return f"<div class='warning'>文件 '{filename}' 是空的，请检查。</div>"

        result = code_review_api(api_key, model, code_content,
                                 temperature=temperature,
                                 max_output_tokens=max_output_tokens,
                                 custom_instruction_prompt=custom_instruction_prompt)
        return f"<h3>文件 '{filename}' 评审结果:</h3>{result}"
    except Exception as e:
        return f"<div class='error'>读取文件 '{filename}' 时出错: {str(e)}</div>"


def review_multiple_files(api_key, model, temperature, max_output_tokens, custom_instruction_prompt, file_objs):
    if not file_objs: return "<div class='error'>请选择文件。</div>"
    all_results = [f"<h3>收到 {len(file_objs)} 个文件的批量评审请求...</h3>"]
    for file_obj in file_objs:
        try:
            filename = os.path.basename(file_obj.name)
            with open(file_obj.name, 'r', encoding='utf-8') as f:
                code_content = f.read()
            if not code_content.strip():
                result_html = f"<div class='warning'>文件 '{filename}' 是空的。</div>"
            else:
                result_html = code_review_api(api_key, model, code_content,
                                              temperature=temperature,
                                              max_output_tokens=max_output_tokens,
                                              custom_instruction_prompt=custom_instruction_prompt)
            all_results.append(f"<details><summary>📄 {filename}</summary><div>{result_html}</div></details>")
        except Exception as e:
            all_results.append(f"<div class='error'>处理文件 '{filename}' 时出错: {str(e)}</div>")
    return "".join(all_results)


def create_web_interface():
    """
    创建 Gradio Web 用户界面。
    """
    initial_api_key = load_api_key_from_file()

    def _create_header_html():
        return gr.HTML(
            """
            <div id="main-title" style="text-align: center; padding: 25px 20px; background: linear-gradient(135deg, #0d6efd, #add8e6); color: #333333; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
                <h1 style="margin:0; padding:0; color: white;">FUCK_U_CODE</h1>
                <p style="margin-top: 8px; font-size: 1.1em; opacity: 0.8; color: white;">去你妈的屎山代码</p>
            </div>
            """
        )

    def _create_global_config_block(initial_api_key_val):
        with gr.Accordion("⚙️ 全局设置与模型参数", open=True, elem_classes="gradio-accordion"):
            api_key = gr.Textbox(label="API 密钥", type="password", value=initial_api_key_val,
                                 placeholder="请输入你的Google AI Studio API Key", interactive=True)
            model = gr.Dropdown(label="选择模型",
                                choices=["gemini-2.5-pro", "gemini-2.5-flash", "gemini-2.0-flash","gemini-1.5-pro","gemini-1.5-flash"],
                                value="gemini-2.5-flash", interactive=True)

            with gr.Row():
                temperature = gr.Slider(label="模型温度 (Temperature)", minimum=0.0, maximum=1.0, step=0.05, value=0.7,
                                        interactive=True,
                                        info="温度越高，模型输出的创造性和随机性越强，但可能不够稳定。建议0.7左右。")
                max_output_tokens = gr.Slider(label="最大输出Token数 (Max Output Tokens)", minimum=100, maximum=4096,
                                              step=50, value=2048, interactive=True,
                                              info="限制模型单次评审回复的最大长度，避免回复过长。")

            custom_instruction_prompt = gr.Textbox(label="自定义评审指令 (Custom Instruction)", lines=3,
                                                   placeholder="例如：请重点关注代码的安全性漏洞和潜在的性能问题，并给出改进建议。",
                                                   interactive=True,
                                                   info="在这里输入针对本次评审的特殊要求或指令，例如侧重安全、性能或代码风格等。")
        return api_key, model, temperature, max_output_tokens, custom_instruction_prompt

    def _create_file_operations_block():
        with gr.Accordion("📂 文件上传与评审操作", open=True, elem_classes="gradio-accordion"):
            single_file_input = None
            single_submit_btn = None
            single_clear_btn = None
            multi_file_input = None
            multi_submit_btn = None
            multi_clear_btn = None

            with gr.Tabs(elem_classes="action-tabs"):
                # 单文件评审标签页
                with gr.TabItem("🎯 单文件精准评审", elem_classes="tab-item"):
                    single_file_input = gr.File(label="上传单个代码文件", file_count="single", type="filepath",
                                                file_types=[".py", ".js", ".java", ".cpp", ".c", ".h", ".cs", ".go",
                                                            ".rb", ".php", ".html", ".css", ".md", ".json", ".xml",
                                                            ".yaml", ".txt"])
                    with gr.Row():
                        single_submit_btn = gr.Button("开始评审", variant="primary", scale=3, elem_classes="submit-btn")
                        single_clear_btn = gr.Button("清空", variant="secondary", elem_classes="clear-btn")
                # 多文件批量处理标签页
                with gr.TabItem("📚 多文件批量处理", elem_classes="tab-item"):
                    multi_file_input = gr.File(label="上传多个代码文件", file_count="multiple", type="filepath",
                                               file_types=[".py", ".js", ".java", ".cpp", ".c", ".h", ".cs", ".go",
                                                           ".rb", ".php", ".html", ".css", ".md", ".json", ".xml",
                                                           ".yaml", ".txt"])
                    with gr.Row():
                        multi_submit_btn = gr.Button("批量评审所有文件", variant="primary", scale=3,
                                                     elem_classes="submit-btn")
                        multi_clear_btn = gr.Button("清空", variant="secondary", elem_classes="clear-btn")
        return single_file_input, single_submit_btn, single_clear_btn, multi_file_input, multi_submit_btn, multi_clear_btn

    def _create_results_display():
        gr.Markdown("### 🔍 评审结果", elem_classes="markdown-header")
        output = gr.Markdown("结果会显示在这里...", elem_id="result-markdown")
        return output

    with gr.Blocks(title="CodeRefiner Ultimate", css=CSS, theme=BrightCourt()) as demo:
        _create_header_html()

        with gr.Row(elem_id="main-layout"):
            with gr.Column(scale=2, elem_classes="left-panel"):
                api_key, model, temperature, max_output_tokens, custom_instruction_prompt = _create_global_config_block(
                    initial_api_key)
                single_file_input, single_submit_btn, single_clear_btn, \
                    multi_file_input, multi_submit_btn, multi_clear_btn = _create_file_operations_block()

            with gr.Column(scale=3, elem_classes="right-panel"):
                output = _create_results_display()

        single_clear_btn.click(lambda: (None, "结果会显示在这里..."), outputs=[single_file_input, output])
        multi_clear_btn.click(lambda: (None, "结果会显示在这里..."), outputs=[multi_file_input, output])

        single_submit_btn.click(fn=review_single_file,
                                inputs=[api_key, model, temperature, max_output_tokens, custom_instruction_prompt,
                                        single_file_input],
                                outputs=output)
        multi_submit_btn.click(fn=review_multiple_files,
                               inputs=[api_key, model, temperature, max_output_tokens, custom_instruction_prompt,
                                       multi_file_input],
                               outputs=output)
    return demo


if __name__ == "__main__":
    interface = create_web_interface()
    interface.launch(server_name="0.0.0.0", share=False)
