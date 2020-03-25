from flask import Flask,request,abort
from linebot import (LineBotApi,WebhookHandler)
from linebot.exceptions import(InvalidSignatureError)
from linebot.models import *
app=Flask(__name__)
line_bot_api=LineBotApi("3qEABhBBt6smIAMBTnI+foIZyd8DTFQzdcE7pYrNnXzK5nlWZrmUszAA2kb/1bw2r7nIMYSi6Fn7aHJa8/2Awd6gfOySueDIMS2M+uv9ciUL+6xSj9qZNRLAP9pANDr/xSVtzNHz0+7y0/Xpwwc/CgdB04t89/1O/w1cDnyilFU=")
handler=WebhookHandler("65e77c3ebca3faa86b2db416a2b85bec")
@app.route("/callback",methods=["POST"])
def callback():
    signature=request.headers["x-Line-Signature"]
    body=request.get_data(as_text=True)
    app.logger.info("Request body:"+body)
    try:
        handler.handle(body,signature)
    except InvalidSignatureError:
        abort(400)
    return "ok"
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text == "開始玩":
        buttons_template = TemplateSendMessage(
            alt_text='開始玩 template',
            template=ButtonsTemplate(
                title='選擇服務',
                text='請選擇',
                thumbnail_image_url='https://i.imgur.com/xQF5dZT.jpg',
                actions=[
                    MessageTemplateAction(
                        label='新聞',
                        text='新聞'
                    ),
                    MessageTemplateAction(
                        label='電影',
                        text='電影'
                    ),
                    MessageTemplateAction(
                        label='看廢文',
                        text='看廢文'
                    ),
                    MessageTemplateAction(
                        label='正妹',
                        text='正妹'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template)
        return 0
    message = TemplateSendMessage(
    alt_text='目錄 template',
    template=CarouselTemplate(
        columns=[
            CarouselColumn(
                    thumbnail_image_url='https://i.imgur.com/PN23ONG.png',
                    title='選擇服務',
                    text='請選擇',
                    actions=[
                        MessageAction(
                            label='開始玩',
                            text='開始玩'
                        ),
                        URIAction(
                            label='韓團 SISTAR',
                            uri='https://www.youtube.com/watch?v=E0ZHXVp_wUE'
                        ),
                        URIAction(
                            label='粉絲團',
                            uri='https://www.facebook.com/mengno.1/'
                        )
                    ]
                ),
            CarouselColumn(
                    thumbnail_image_url='https://i.imgur.com/DrsmtKS.jpg',
                    title='選擇服務',
                    text='請選擇',
                    actions=[
                        MessageAction(
                            label='other bot',
                            text='imgur bot'
                        ),
                        MessageAction(
                            label='油價查詢',
                            text='油價查詢'
                        ),
                        URIAction(
                            label='聯絡作者',
                            uri='https://ptt-beauty-infinite-scroll.herokuapp.com/'
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://i.imgur.com/h4UzRit.jpg',
                    title='選擇服務',
                    text='請選擇',
                    actions=[
                        URIAction(
                            label='分享 bot',
                            uri='https://ptt-beauty-infinite-scroll.herokuapp.com/'
                        ),
                        URIAction(
                            label='PTT正妹網',
                            uri='https://ptt-beauty-infinite-scroll.herokuapp.com/'
                        ),
                        URIAction(
                            label='youtube 程式教學分享頻道',
                            uri='https://ptt-beauty-infinite-scroll.herokuapp.com/'
                        )
                    ]
                )
            ]
        )
    )

    line_bot_api.reply_message(
        event.reply_token,
        message)

import os

if __name__=="__main__":
    port=int(os.environ.get("port",5000))
    app.run(host="0.0.0.0",port=port)