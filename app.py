import requests
from bs4 import BeautifulSoup
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
def apple_news():
    target_url = 'https://tw.appledaily.com/new/realtime'
    print('Start parsing appleNews....')
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    soup = BeautifulSoup(res.text, 'html.parser')
    content = ""
    for index, data in enumerate(soup.select('.rtddt a'), 0):
        if index == 5:
            return content
        link = data['href']
        content += '{}\n\n'.format(link)
    return content
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text == "蘋果即時新聞":
        content = apple_news()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
    if event.message.text == "新聞":
        buttons_template = TemplateSendMessage(
            alt_text='新聞 template',
            template=ButtonsTemplate(
                title='新聞類型',
                text='請選擇',
                thumbnail_image_url='https://i.imgur.com/vkqbLnz.png',
                actions=[
                    MessageTemplateAction(
                        label='蘋果即時新聞',
                        text='蘋果即時新聞'
                    ),
                    MessageTemplateAction(
                        label='科技新報',
                        text='科技新報'
                    ),
                    MessageTemplateAction(
                        label='PanX泛科技',
                        text='PanX泛科技'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template)
        return 0
    if event.message.text == "開始玩":
        buttons_template = [
            TemplateSendMessage(
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
        ]
        line_bot_api.reply_message(event.reply_token, buttons_template)
        return 0
    message = TemplateSendMessage(
    alt_text='目錄 template',
    template=CarouselTemplate(
        columns=[
            CarouselColumn(
                thumbnail_image_url='https://i.imgur.com/A3mEp8q.png',
                title='選擇服務',
                text='請選擇',
                actions=[
                    MessageAction(
                        label='開始玩',
                        text='開始玩'
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