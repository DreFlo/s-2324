from openai import OpenAI
import os
from dotenv import load_dotenv

from utils.chat_gpt_query_templates import get_explain_company_prediction_query

load_dotenv()

CHAT_GPT_API_KEY = os.getenv('CHAT_GPT_API_KEY')

class ChatGPTWrapper:
    __client = OpenAI(api_key=CHAT_GPT_API_KEY)

    def __init__(self) -> None:
        pass

    def explain_prediction(prediction : dict, text_style : str = 'casually, as if between friends, but don\'t be long-winded') -> str:
        query = get_explain_company_prediction_query(prediction=prediction, style=text_style)

        response = ChatGPTWrapper.__client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You generate output based on the instructions given to you"},
                {"role": "user", "content": query}
            ]
        )

        return response.choices[0].message.content
