import openai

# 首先，需要设置API的访问秘钥
openai.api_key = "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"

# 定义一个函数来与GPT-3模型进行交互
def openai_reply(content):
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-0301",
    messages=[
    {"role": "user", "content": content}
    ],
    temperature=0.5,
    max_tokens=2000,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    )
    # print(response)
    return response.choices[0].message.content

def generate_prompt(input_text):
    prompt_template = "你是一名专业的视频口博话术编辑师，请根据以下文案要求，生成用于口播短视频的文案：" \
                      """ \
                      "文案要求: {}" \
                      """
    return prompt_template.format(input_text)

def generate_ai_text(input_text):
    return openai_reply(generate_prompt(input_text))