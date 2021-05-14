from event.line_bot_api import *
from modles.appointment import Appointment
from urllib.parse import parse_qsl
import datetime


def booking_event(event):
    appointment = Appointment.query.filter(Appointment.user_id == event.source.user_id).first()
    if not appointment:
        line_bot_api.reply_message(event.reply_token, TemplateSendMessage(
            alt_text='Carousel template',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/bO0kmAV.jpg',
                        title="服務項目",
                        text='請選擇服務',
                        actions=[
                            PostbackAction(
                                label='服務一',
                                display_text='服務一',
                                data='action=step2&service=服務一'
                            ),
                            PostbackAction(
                                label='服務二',
                                display_text='服務二',
                                data='action=step2&service=服務二'
                            ),
                            PostbackAction(
                                label='服務三',
                                display_text='服務三',
                                data='action=step2&service=服務三'
                            )
                        ]
                    )
                ]
            )
        ))
    else:
        data = dict(parse_qsl(event.postback.data))
        data['time'] = appointment.appointment_datetime.strptime(event.postback.params.get('datetime'),
                                                                 '%Y-%m-%dT%H:%M')
        data['name'] = line_bot_api.get_profile(event.source.user_id).display_name
        line_bot_api.reply_message(event.reply_token,
                                   [TextSendMessage(
                                       text="用戶{}\n你預約了{}\n時間為\n{}\n謝謝"
                                           .format(data['name'], data['service'], data['time'])),
                                       TemplateSendMessage(
                                           alt_text='Confirm template',
                                           template=ConfirmTemplate(
                                               text='要取消預約嗎',
                                               actions=[
                                                   MessageAction(
                                                       label='是',
                                                       text='@取消預約'
                                                   ),
                                                   MessageAction(
                                                       label='否',
                                                       text='@不'
                                                   )
                                               ]
                                           )
                                       )
                                   ])
