import openai
from config import API_KEY

openai.api_key = API_KEY

def extract_info (text_from_voice):
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo-preview",  
        messages=[
            {"role": "user", "content": f"Extract the only app name from this text:"+ text_from_voice + " If no app was asked to open, extract subject key word"}
        ]
    )
    print(response.choices[0].message['content'].strip().split('\n')[0])
    return response.choices[0].message['content'].strip().split('\n')[0]



