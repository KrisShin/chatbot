from collections import Counter
import re
from openai import OpenAI

from common.rag_util import RAGUtil
from common.settings import OPENAI_API_KEY


class ChatUtil(object):
    client = None
    model = 'gpt-4'

    def __init__(self):
        if self.client is None:
            self.client = ChatUtil.get_client()
        self.model = ChatUtil.model
        self.messages = []

    @classmethod
    def get_client(cls):
        return OpenAI(api_key=OPENAI_API_KEY)

    @staticmethod
    def limit_messages(messages):
        counter = Counter([msg['role'] for msg in messages if isinstance(msg, dict)])
        if counter['user'] > 3:
            messages.pop(0)
            for msg in messages:
                if isinstance(msg, dict) and msg['role'] == 'user':
                    break
                messages.pop(0)
        return messages

    def chat(self, msg_list):
        self.messages = ChatUtil.limit_messages(msg_list)
        stream = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            stream=True,
        )
        return stream

    @classmethod
    def create_chat(cls):
        chat = ChatUtil()
        chat.messages.clear()
        chat.client = ChatUtil.get_client()
        return chat

    def with_rag(self, web_paths, messages):
        messages = ChatUtil.limit_messages(messages)

        # Step 1: send the conversation and available functions to the model
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "load_rag_chain",
                    "description": "Get answer from the website",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "web_paths": {
                                "type": "string",
                                "description": "The web path tuple witch you want to parse.",
                            },
                            "question": {
                                "type": "string",
                                "description": "the question witch ask RAG.",
                            },
                        },
                        "required": ["web_paths", "question"],
                    },
                },
            }
        ]
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            tools=tools,
            tool_choice="auto",  # auto is default, but we'll be explicit
        )
        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls
        # Step 2: check if the model wanted to call a function
        if tool_calls:
            # Step 3: call the function
            # Note: the JSON response may not always be valid; be sure to handle errors
            available_functions = {
                "load_rag_chain": RAGUtil.invoke,
            }  # only one function in this example, but you can have multiple
            messages.append(
                response_message
            )  # extend conversation with assistant's reply
            # Step 4: send the info for each function call and function response to the model
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_to_call = available_functions[function_name]
                function_response = function_to_call(
                    web_paths=web_paths, question=messages[-2]['content']
                )
                messages.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": function_response,
                    }
                )  # extend conversation with function response
        second_response = self.client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            stream=True,
        )  # get a new response from the model where it can see the function response
        return second_response


if __name__ == "__main__":
    # 以下代码用于直接运行该文件时测试该文件中的工具类功能
    chat = ChatUtil()
    msg = '你好'
    messages = []
    web_paths = ("https://lilianweng.github.io/posts/2023-06-23-agent/",)
    while msg:
        if msg is not True:
            messages.append({'role': 'user', 'content': msg})
            stream = chat.with_rag(web_paths, messages)
            answer = ""
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    msg = chunk.choices[0].delta.content or ''
                    answer += msg
                    print(msg, end='')
            chat.messages.append({'role': 'assistant', 'content': answer})
        msg = input("\n> ")
    # messages.append({'role': 'user', 'content': 'from this site https://lilianweng.github.io/posts/2023-06-23-agent/ , 总结这篇文章?'})
    # stream = chat.with_rag(web_paths, messages)
    # answer = ""
    # for chunk in stream:
    #     if chunk.choices[0].delta.content is not None:
    #         msg = chunk.choices[0].delta.content or ''
    #         answer += msg
    #         print(msg, end='')
