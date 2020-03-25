import os
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
    line_bot_api.reply_message(
        event.reply_token,
        message)

if __name__=="__main__":
    port=int(os.environ.get("port",5000))
    app.run(host="0.0.0.0",port=port)