import os
import googlemaps
from linebot import LineBotApi, WebhookParser
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from googletrans import Translator

channel_access_token = "JATPy5NQa60v82IZzvV3TbGDb+A0cc6Z1oKpt90x/XIt+Rfc3heUJi4bEQkqXq5qy1GGxd3jVe+AzMQj7euk2xWprua0AJ6pIkHVRNyMg8BYOPbJjS3tCqyIPFU9FHCTw2MsPKZ4Slwep9keKgVcHgdB04t89/1O/w1cDnyilFU="
user_id = "Ue15abf7a16fa682af293717a1d7e5848"
line_bot_api = LineBotApi(channel_access_token)

def send_text_message(reply_token, text):
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))
    return "OK"

def push_message(push_text_str):
    line_bot_api.push_message(user_id, TextSendMessage(text=push_text_str))

def transE2C(str1):
    dest = 'zh-tw'
    translator = Translator()
    result = translator.translate(str1, dest).text
    return result

def transC2E(str1):
    dest = 'en'
    translator = Translator()
    result = translator.translate(str1, dest).text
    return result

def trans2J(str1):
    dest = 'ja'
    translator = Translator()
    result = translator.translate(str1, dest).text
    return result



"""
def send_image_url(id, img_url):
    pass

def send_button_message(id, text, buttons):
    pass
"""