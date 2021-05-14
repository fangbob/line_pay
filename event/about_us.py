from event.line_bot_api import *

def about_us_event(event):
     image="https://i.imgur.com/LRoLTlK.jpg"
     text="這是測試機器人"
     title_text = "快樂的地方"
     address_text = "260宜蘭縣宜蘭市神農路一段1號"
     latitude = 24.7462462
     longitude = 121.745512
     line_bot_api.reply_message(event.reply_token,[TextSendMessage(text=text),
                                                   ImageSendMessage(original_content_url=image,
                                                                    preview_image_url=image),
                                                   LocationSendMessage(title=title_text, address=address_text,
                                                                       latitude=latitude,
                                                                       longitude=longitude) ])