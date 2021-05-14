from event.line_bot_api import *

def contact_event(event):
    buttons_template_message = TemplateSendMessage(
        alt_text='Buttons template',
        template=ButtonsTemplate(
            thumbnail_image_url='https://i.imgur.com/W9NFUaw.jpg',
            title='Contact',
            text='Please select',
            actions=[
                URIAction(
                    label='Call us',
                    uri='tel:+0979580521'
                )
            ]
        )
    )
    line_bot_api.reply_message(
        reply_token=event.reply_token,
        messages=[buttons_template_message]
    )