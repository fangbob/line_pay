from flask import Flask, request, abort
from event.about_us import about_us_event
from event.products import products_event
from event.cart import cart_event
from event.contact import contact_event
from event.exchange_rate import exchange_rate_event
from event.line_bot_api import *
from event.booking import booking_event
from urllib.parse import parse_qsl
from modles.database import db_session, init_db
from modles.user import User
from modles.appointment import Appointment
import datetime

app = Flask(__name__)


@app.before_first_request
def init():
    init_db()


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


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
    user_id = event.source.user_id
    user = User.query.filter(User.id == user_id).first()
    if not user:
        user = User(id=user_id)
        db_session.add(user)
        db_session.commit()

    if event.message.text == "What is your story?":
        about_us_event(event)
    elif event.message.text == "i am ready to order":
        products_event(event)
    elif event.message.text == "my cart":
        cart_event(event)
    elif "換" in event.message.text:
        exchange_rate_event(event)
    elif event.message.text == "contact":
        contact_event(event)
    elif event.message.text == "預約":
        booking_event(event)
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=event.message.text))


@handler.add(PostbackEvent)
def handler_postback(event):
    data = dict(parse_qsl(event.postback.data))
    if data['action'] == 'step2':
        now = datetime.datetime.now()
        max_date = now + datetime.timedelta(days=30)
        line_bot_api.reply_message(event.reply_token,
                                   TemplateSendMessage(
                                       alt_text="時間選擇",
                                       template=ImageCarouselTemplate(
                                           columns=[
                                               ImageCarouselColumn(
                                                   image_url='https://i.imgur.com/z8AaD3D.png',
                                                   action=DatetimePickerAction(
                                                       label="挑選時間",
                                                       data="action=step3&service={}".format(data['service']),
                                                       mode="datetime",
                                                       initial=now.strftime("%Y-%m-%dT00:00"),
                                                       min=now.strftime("%Y-%m-%dT00:00"),
                                                       max=max_date.strftime("%Y-%m-%dT23:59")
                                                   )
                                               )
                                           ]
                                       )
                                   ))
    if data['action'] == 'step3':
        data['time'] = datetime.datetime.strptime(event.postback.params.get('datetime'), '%Y-%m-%dT%H:%M')
        data['name'] = line_bot_api.get_profile(event.source.user_id).display_name
        appointment = Appointment(user_id=data['name'],
                                  appointment_service=data['service'],
                                  appointment_datetime=data['time'])
        db_session.add(appointment)
        db_session.commit()
        line_bot_api.reply_message(event.reply_token,
                                   TextSendMessage(
                                       text="用戶{}\n你預約了{}\n時間為\n{}\n謝謝"
                                           .format(data['name'], data['service'], data['time'])))


if __name__ == "__main__":
    app.run()
