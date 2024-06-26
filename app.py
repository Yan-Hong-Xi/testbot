# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 21:16:35 2021

@author: Ivan
版權屬於「行銷搬進大程式」所有，若有疑問，可聯絡ivanyang0606@gmail.com

Line Bot聊天機器人
第一章 Line Bot申請與串接
Line Bot機器人串接與測試
"""
#載入LineBot所需要的套件
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *



app = Flask(__name__)


# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('rOtH8cmDleBWSPtM0oaXNGt+vunKGgyB15kqiVu2LPcKLcbqOYNdK/zGjc22ME4ZOpWsUEujXswLMCaSTlWFM1oEFHWiwpE+7GRjXqPhdvSA0aca9wLCWAjXTB7RXeAZ+p7uW+pslK9PnxI/d+4enwdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的Channel Secret
handler = WebhookHandler('04c8536a5735865ce3f076a4aed1e13c')

line_bot_api.push_message('U6affcd3fde969a82bb289fc2a73c75f6', TextSendMessage(text='你可以開始了'))

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

#訊息傳遞區塊
##### 基本上程式編輯都在這個function #####


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    
    # 要发送消息的用户 ID
    user_id = event.source.user_id
    message_text = event.message.text
    print(f"Received message from {user_id}: {message_text}")

    # 发送确认消息
    
    confirmation_message = TextSendMessage(text="Webhook has been updated.")
    line_bot_api.reply_message(event.reply_token, confirmation_message)
    
    # 定义文件消息的 URL
    file_url = 'https://github.com/Yan-Hong-Xi/testbot/blob/main/test.pdf'

    # 创建按钮模板消息
    buttons_template = TemplateSendMessage(
        alt_text='Document',
        template=ButtonsTemplate(
            title='Document',
            text='Click the button below to open the document',
            actions=[
                URITemplateAction(
                    label='Open Document',
                    uri=file_url
                )
            ]
        )
    )
    # 发送文件消息
    line_bot_api.reply_message(event.reply_token, buttons_template)

#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)