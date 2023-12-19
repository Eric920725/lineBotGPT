from flask import Flask
app = Flask(__name__)

from flask import request, abort
from linebot import  LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os
from openai import OpenAI

line_bot_api = LineBotApi(os.environ.get('line_access_token'))
handler = WebhookHandler(os.environ.get('line_channel_secret'))

client = OpenAI(
    # api_key='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'
    api_key=(os.environ.get('openAI_key'))
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
    
        replyMSG=response.choices[0].message.content
        message = TextSendMessage(
            text = replyMSG
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
if __name__ == '__main__':
    app.run()
