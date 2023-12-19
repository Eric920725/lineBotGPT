from flask import Flask
app = Flask(__name__)

from flask import request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os
from openai import OpenAI

line_bot_api = LineBotApi(os.environ.get('yGxW+YC5ohqoo9zGT2T6gqP8Pm2WPgRnU315Kil+uw2lr2n8dwJJq12KT12PIJkCW4ievbCf9qndJxhM9NK9PnboXStnDa1vzAOywc6ukyPelFoVkcIk0lZ9ZUECsHZSHZUyevBMbY1osS3skXwPjAdB04t89/1O/w1cDnyilFU='))
handler = WebhookHandler(os.environ.get('0a4ae178ea21bdbfaf9540b56e97db7d'))

client = OpenAI(
    api_key=(os.environ.get('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'))
)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def chat(event):
    try:
        mtext = event.message.text
        print(f"Received message: {mtext}")

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "你是一位使用繁體中文的全能小幫手",
                },
                {
                    "role": "user",
                    "content": f"{mtext}",
                }
            ],
            max_tokens=256,
        )

        print(f"OpenAI response: {response}")

        replyMSG = response.choices[0].message.content
        print(f"Reply message: {replyMSG}")

        message = TextSendMessage(
            text=replyMSG
        )
        line_bot_api.reply_message(event.reply_token, message)
    except Exception as e:
        print(f"Error: {e}")
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤！'))

if __name__ == '__main__':
    app.run()


            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
