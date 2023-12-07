from openai import OpenAI

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

    def chat(self, msg_list):
        self.messages = msg_list
        if len(self.messages) >= 6:
            self.messages.pop(0)
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

    # Example dummy function hard coded to return the same weather
    # In production, this could be your backend API or an external API
    # def get_current_weather(self, location, unit="fahrenheit"):
    #     """Get the current weather in a given location"""
    #     if "tokyo" in location.lower():
    #         return json.dumps({"location": "Tokyo", "temperature": "10", "unit": unit})
    #     elif "san francisco" in location.lower():
    #         return json.dumps(
    #             {"location": "San Francisco", "temperature": "72", "unit": unit}
    #         )
    #     elif "paris" in location.lower():
    #         return json.dumps({"location": "Paris", "temperature": "22", "unit": unit})
    #     else:
    #         return json.dumps({"location": location, "temperature": "unknown"})

    # def run_conversation(self):
    #     # Step 1: send the conversation and available functions to the model
    #     messages = [
    #         {
    #             "role": "user",
    #             "content": "What's the weather like in San Francisco, Tokyo, and Paris?",
    #         }
    #     ]
    #     tools = [
    #         {
    #             "type": "function",
    #             "function": {
    #                 "name": "get_current_weather",
    #                 "description": "Get the current weather in a given location",
    #                 "parameters": {
    #                     "type": "object",
    #                     "properties": {
    #                         "location": {
    #                             "type": "string",
    #                             "description": "The city and state, e.g. San Francisco, CA",
    #                         },
    #                         "unit": {
    #                             "type": "string",
    #                             "enum": ["celsius", "fahrenheit"],
    #                         },
    #                     },
    #                     "required": ["location"],
    #                 },
    #             },
    #         }
    #     ]
    #     response = self.client.chat.completions.create(
    #         model="gpt-4",
    #         messages=messages,
    #         tools=tools,
    #         tool_choice="auto",  # auto is default, but we'll be explicit
    #     )
    #     response_message = response.choices[0].message
    #     tool_calls = response_message.tool_calls
    #     # Step 2: check if the model wanted to call a function
    #     if tool_calls:
    #         # Step 3: call the function
    #         # Note: the JSON response may not always be valid; be sure to handle errors
    #         available_functions = {
    #             "get_current_weather": self.get_current_weather,
    #         }  # only one function in this example, but you can have multiple
    #         messages.append(
    #             response_message
    #         )  # extend conversation with assistant's reply
    #         # Step 4: send the info for each function call and function response to the model
    #         for tool_call in tool_calls:
    #             function_name = tool_call.function.name
    #             function_to_call = available_functions[function_name]
    #             function_args = json.loads(tool_call.function.arguments)
    #             function_response = function_to_call(
    #                 location=function_args.get("location"),
    #                 unit=function_args.get("unit"),
    #             )
    #             messages.append(
    #                 {
    #                     "tool_call_id": tool_call.id,
    #                     "role": "tool",
    #                     "name": function_name,
    #                     "content": function_response,
    #                 }
    #             )  # extend conversation with function response
    #         second_response = self.client.chat.completions.create(
    #             model="gpt-4",
    #             messages=messages,
    #         )  # get a new response from the model where it can see the function response
    #         return second_response


if __name__ == "__main__":
    # 以下代码用于直接运行该文件时测试该文件中的工具类功能
    chat = ChatUtil()
    msg = True
    messages = []
    while msg:
        if msg is not True:
            stream = chat.chat(msg)
            answer = "bot: "
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    msg = chunk.choices[0].delta.content or ''
                    answer += msg
                    print(msg, end='')
            chat.messages.append({'role': 'assistant', 'content': answer})
        msg = input("\n> ")
