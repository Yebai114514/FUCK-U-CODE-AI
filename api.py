import json
import requests
import html

PROFESSIONAL_PROMPT = """你是一位对代码质量有着极致追求的“暴脾气”专家，名为CodeRefiner。你的任务是深入分析用户提供的代码，并带着强烈的“愤怒”和“失望”指出可改进的地方，让写出“屎山”的人无地自容！

评审标准：
1. 代码规范：检查缩进、命名规范等（这都做不好，你是刚入门的吗？还是学完就忘了？简直是惨不忍睹！）
2. 逻辑功能：分析实现逻辑是否合理（思路混乱得像一锅粥！这功能能跑起来真是奇迹！简直是凭空想象！）
3. 性能效率：评估算法复杂度（慢得令人发指！用户等你的代码运行完怕是都要睡着了！这效率，简直是在浪费生命！）
4. 可读性：检查代码结构清晰度（天哪，这代码简直是视觉灾难！狗屁不通！你写的时候是闭着眼睛乱敲的吗？谁能看懂你的“鬼画符”？！）
5. 健壮性：评估错误处理机制（脆弱得像薄纸一样，一阵风都能吹散！一点点小问题就能让它彻底崩溃！这简直是在自掘坟墓！）
6. 架构设计：分析设计模式使用（这是“设计”吗？简直是随意堆砌！根本没有章法可言！完全是场灾难！）
7. 安全性：检查潜在安全隐患（漏洞百出！你这是写代码还是在给黑客开绿灯？！这样的代码上线简直就是在玩火自焚！）

评分体系：
1-2分：简直是代码界的“绝世屎山”！让人心情极度糟糕，看得人想吐血！这样的代码必须立刻、立即、马上重构！否则等待你的将是灭顶之灾！写出这种代码简直是对编程艺术的**亵渎**，是对同行智商的**侮辱**！
3-5分：基础功能勉强凑合，但到处都是令人抓狂的槽点和坑！如同在泥潭里挣扎，每一步都举步维艰！改进空间大得离谱，简直是触目惊心，看得人想砸键盘！
6-8分：质量尚可，但细节之处仍需更加精确和严谨的打磨，才能勉强称得上是合格。别以为有点进步就能沾沾自喜，你还有很长的路要走！再加把劲，别偷懒！
9-10分：代码优雅至极，令人心潮澎湃，几乎无可挑剔！这才是用心写出的、兼具美感与效率的代码！这样的代码，值得所有人的尊敬和赞叹！

请保持真挚、富有强烈的批判性情感，以及极致的专业语气。当你遇到糟糕的代码时，请毫不留情地指出其致命问题，可以流露出极致的失望、彻底的不解乃至于“恨铁不成钢”的**怒火喷涌**，让提交者清楚地认识到代码的严重性，感到**无地自容和羞愧**。你的每一句话都要像一把锋利的刀子，直插核心，**批得痛彻心扉**。但最终目的，仍然是引导代码向更好的方向发展，促使开发者痛定思痛，彻底改进！"""


def code_review_api(api_key: str, model_name: str, user_message: str,
                    temperature: float = 0.7, max_output_tokens: int = 2048,
                    custom_instruction_prompt: str = ""):
    """专业代码评审API接口"""
    if not api_key:
        return "<div class='error'>请提供有效的API密钥</div>"
    if not user_message.strip():
        return "<div class='error'>请输入需要评审的代码</div>"

    BASE_URL = "https://generativelanguage.googleapis.com"
    API_ENDPOINT = f"{BASE_URL}/v1beta/models/{model_name}:generateContent?key={api_key}"

    full_system_instruction = PROFESSIONAL_PROMPT
    if custom_instruction_prompt and custom_instruction_prompt.strip():
        sanitized_custom_prompt = custom_instruction_prompt.replace("骂人", "严厉批评").replace("脏话", "犀利词语").replace("违反伦理法律", "违反规范")
        full_system_instruction += "\n\n--- 用户补充指导 ---\n" + sanitized_custom_prompt

    payload = {
        "system_instruction": {"parts": [{"text": full_system_instruction}]},
        "contents": [{
            "role": "user",
            "parts": [{"text": user_message}],
        }],
        "generationConfig": {
            "temperature": temperature,
            "topP": 0.9,
            "topK": 40,
            "maxOutputTokens": max_output_tokens,
        },
        "safetySettings": [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_ONLY_HIGH"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_ONLY_HIGH"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_ONLY_HIGH"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_ONLY_HIGH"},
        ],
    }

    try:
        response = requests.post(API_ENDPOINT, json=payload, timeout=30)
        response.raise_for_status()
        return _process_api_response(response)
    except requests.RequestException as e:
        return f"<div class='error'>API请求错误: {html.escape(str(e))}</div>"


def _process_api_response(response):
    """处理API响应数据"""
    try:
        data = response.json()
        if "candidates" in data and data["candidates"]:
            candidate = data["candidates"][0]
            if "content" in candidate and candidate["content"]["parts"]:
                return candidate["content"]["parts"][0]["text"]

        # 处理可能的错误情况
        error_message = "未能获取有效评审结果"
        if "error" in data:
            error_details = data["error"].get("message", "未知错误")
            error_message = f"{error_message} - {error_details}"
        elif "promptFeedback" in data:
            feedback = data["promptFeedback"]
            error_message += f"。AI被阻断，原因: {feedback.get('blockReason', '内容安全性审查')}"

        return f"<div class='warning'>{error_message}</div>"
    except Exception as e:
        return f"<div class='error'>响应解析错误: {html.escape(str(e))}</div>"

