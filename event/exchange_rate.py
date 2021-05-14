import requests
from event.line_bot_api import *
def exchange_rate_event(event):
    coin_text = event.message.text.split("換")
    print(coin_text)
    resp = requests.get('https://tw.rter.info/capi.php')
    currency_data = resp.json()
    a = currency_data["USD" + coin_text[0]]['Exrate']
    b = currency_data["USD" + coin_text[1]]['Exrate']
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="{}對{}=1:{}".format(coin_text[0], coin_text[1], str(b / a))))
