from event.line_bot_api import *

def products_event(event):
     image="https://i.imgur.com/ZKTt259.jpg"
     text="商品列表"
     line_bot_api.reply_message(event.reply_token,[TextSendMessage(text=text),
                                                   ImageSendMessage(original_content_url=image,
                                                                    preview_image_url=image)])