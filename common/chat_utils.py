from openai import OpenAI

from common.settings import OPENAI_API_KEY


class ChatUtil(object):
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.model = 'gpt-4 turbo'

    def chat(self, message):
        return
