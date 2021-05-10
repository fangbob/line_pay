from event.line_bot_api import *

def about_us_event(event):
     image="https://i.imgur.com/LRoLTlK.jpg"
     text="這是測試機器人"
     line_bot_api.reply_message(event.reply_token,[TextSendMessage(text=text),
                                                   ImageSendMessage(original_content_url=image,
                                                                    preview_image_url=image)])