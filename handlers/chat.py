from tornado.websocket import WebSocketHandler
from handlers.session import BaseHandler
import json


class ChatPageHandler(BaseHandler):
    def get(self):
        user = self.current_user
        if user:
            self.user = user.decode()
            print(self.user, "已登录")
            self.render("chat.html")
        else:
            self.redirect("/login")


class ChatWebSocket(WebSocketHandler, BaseHandler):
    clients = set()

    def open(self):
        user = self.get_current_user()
        if user:
            self.user = user.decode()
            ChatWebSocket.clients.add(self)

    def on_message(self, message):
        message_data = json.loads(message)
        full_message = {'user': self.user, 'text': message_data['text']}
        for client in ChatWebSocket.clients:
            client.write_message(json.dumps(full_message))

    def on_close(self):
        ChatWebSocket.clients.remove(self)
        print(self.user, "已下线")
