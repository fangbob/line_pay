from flask import Flask, request, abort
from event.about_us import about_us_event
from event.products import products_event
from event.cart import cart_event
from event.line_bot_api import *
import requests
app = Flask(__name__)

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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message_text=str(event.message.text)
    coin_text=message_text.split("換")
    print(coin_text)
    if message_text=="What is your story?":
        about_us_event(event)
    elif message_text=="i am ready to order":
        products_event(event)
    elif message_text=="my cart":
        cart_event(event)
    elif "換" in message_text:
        resp = requests.get('https://tw.rter.info/capi.php')
        currency_data = resp.json()
        t=coin_text[0]+coin_text[1]
        print(t)
        _to_ = currency_data[t]['Exrate']
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="{}對{}=1:{}".format(coin_text[0],coin_text[1],_to_)))
    else:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=event.message.text))

if __name__ == "__main__":
    app.run()