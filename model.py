import os
from openai import OpenAI
from dotenv import load_dotenv
class Model:
    def __init__(self):
        load_dotenv()
    @staticmethod
    def openai_chatgpt(transcript, prompt, extra=""):
        load_dotenv()
        client = OpenAI(api_key=os.getenv("API_KEY"),base_url="https://api.deepseek.com")
        try:
            response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content":prompt + extra + transcript},
                {"role": "user", "content": prompt + extra + transcript},
            ],
            stream=False
            )
            return response.choices[0].message.content
        except Exception as e:
            response_error = "There is a problem with the API key or with the Python module."
            return response_error,e


