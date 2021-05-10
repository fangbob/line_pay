from event.line_bot_api import *

def cart_event(event):
    image="https://i.imgur.com/lnpba.jpg"
    text="車"
    line_bot_api.reply_message(event.reply_token, [TextSendMessage(text=text),
                                                   ImageSendMessage(original_content_url=image,
                                                                    preview_image_url=image)])