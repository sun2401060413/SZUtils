"""
This script is some examples of how to use the OpenAI API
Created by: Sun Zhu, 2023-05-11, version 0.0
"""

# ////////// IMPORT //////////
import os
import openai
# ======== Local Lib ========
if os.path.exists("config_private.py"):
    from config_private import *
else:
    from config import *

# ////////// CONFIG //////////
openai.api_key = openai_api_key
openai.organization = openai_organization
# ////////// CLASS //////////

# ////////// UTILS //////////

# ///////// TEST CASE ////////
# 实现接口函数
def get_completion(prompt, model="gpt-3.5-turbo", temperature=1):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]


if __name__ == "__main__":
    prompt = "什么是边缘计算？"
    print(prompt)
    response = get_completion(prompt)
    print(response)