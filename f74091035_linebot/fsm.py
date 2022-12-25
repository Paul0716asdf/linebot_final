from transitions.extensions import GraphMachine
from utils import*

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)
        
    # state1 
    def is_going_to_state1(self, event):
        text = event.message.text
        return text.lower() == "m1"

    def on_enter_state1(self, event):
        print("I'm entering state1")

        reply_token = event.reply_token
        send_text_message(reply_token, "進入翻中")
        push_message("輸入句子")

    def on_exit_state1(self):
        print("Leaving state1")

    # state2
    def is_going_to_state2(self, event):
        text = event.message.text
        return text.lower() == "m2"

    def on_enter_state2(self, event):
        print("I'm entering state2")

        reply_token = event.reply_token
        send_text_message(reply_token, "進入翻英")
        push_message("輸入句子")

    def on_exit_state2(self):
        print("Leaving state2")

    # state3
    def is_going_to_state3(self, event):
        text = event.message.text
        return text.lower() == "m3"

    def on_enter_state3(self, event):        
        reply_token = event.reply_token
        send_text_message(reply_token, "進入翻日")
        push_message("輸入句子")

    def on_exit_state3(self):
        print("Leaving state3")