import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from fsm import TocMachine
from utils import*


machine = TocMachine(
    states=["user", "state1", "state2", "state3"],
    transitions=[
        {
            "trigger": "advance",
            "source": "user",
            "dest": "state1",
            "conditions": "is_going_to_state1",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "state2",
            "conditions": "is_going_to_state2",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "state3",
            "conditions": "is_going_to_state3",
        },
        {"trigger": "go_back", "source": ["state1", "state2", "state3"], "dest": "user"},
    ],
    initial="user",
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path="")


# get channel_secret and channel_access_token from your environment variable
channel_secret = "a93248a3fdd61da50bf216cc25eb3b73"
channel_access_token = "JATPy5NQa60v82IZzvV3TbGDb+A0cc6Z1oKpt90x/XIt+Rfc3heUJi4bEQkqXq5qy1GGxd3jVe+AzMQj7euk2xWprua0AJ6pIkHVRNyMg8BYOPbJjS3tCqyIPFU9FHCTw2MsPKZ4Slwep9keKgVcHgdB04t89/1O/w1cDnyilFU="

# if channel_secret is None:
#     print("Specify LINE_CHANNEL_SECRET as environment variable.")
#     sys.exit(1)
# if channel_access_token is None:
#     print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
#     sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)

# line_bot_api.push_message('Ue15abf7a16fa682af293717a1d7e5848', TextSendMessage(text = "你可以開始了"))

def instruction_help(event):
    msg = "輸入 m1 進入翻中模式 , 輸入 #exit 離開此模式\n\n輸入 m2 進入翻英模式 , 輸入 #eixt 離開此模式\
    \n\n輸入 m3 進入翻日模式 , 輸入 #eixt 離開此模式"
    line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text=msg)
    )

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue

        if(machine.state == "user"):
            response = machine.advance(event)
            if(response == True):
                print("enter success")  #進入到其他state了
            else:  #沒有進入到其他state 那就不用做事
                if(event.message.text == "#help"):
                    instruction_help(event)
                else:
                    line_bot_api.reply_message(
                        event.reply_token, TextSendMessage(text=event.message.text)
                    )

        elif(machine.state == "state1"):  # 翻中
            text = event.message.text

            if text == "#exit":
                machine.go_back()
                line_bot_api.reply_message(
                    event.reply_token, TextSendMessage(text="返回user模式")
                )
            else:
                translate_str = transE2C(text)
                line_bot_api.reply_message(
                    event.reply_token, TextSendMessage(text=translate_str)
                )

        elif(machine.state == "state2"):  # 翻英
            text = event.message.text

            if text == "#exit":
                machine.go_back()
                line_bot_api.reply_message(
                    event.reply_token, TextSendMessage(text="返回user模式")
                )
            else:
                translate_str = transC2E(text)
                line_bot_api.reply_message(
                    event.reply_token, TextSendMessage(text=translate_str)
                )
        else:   # 翻日
            text = event.message.text

            if text == "#exit":
                machine.go_back()
                line_bot_api.reply_message(
                    event.reply_token, TextSendMessage(text="返回user模式")
                )            
            else:
                translate_str = trans2J(text)
                line_bot_api.reply_message(
                    event.reply_token, TextSendMessage(text=translate_str)
                )

    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    return send_file("fsm.png", mimetype="image/png")

if __name__ == "__main__":
    push_message('輸入 #help 查看指令')
    port = os.environ.get("PORT", 80)
    app.run(host="0.0.0.0", port=port, debug=True)


# ngrok http 5000