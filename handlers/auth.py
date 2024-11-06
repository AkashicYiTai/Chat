from sqlalchemy.future import select
from tornado.web import RequestHandler
from models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
from handlers.session import BaseHandler
import json
import uuid


class LoginHandler(BaseHandler):
    def prepare(self):
        if not self.get_secure_cookie("csrf_token"):
            self.csrf_token = str(uuid.uuid4())
            self.set_secure_cookie("csrf_token", self.csrf_token)
        else:
            self.csrf_token = self.get_secure_cookie("csrf_token").decode('utf-8')

    def check_csrf_token(self):
        request_csrf_token = self.get_argument("_csrf_token", None)
        server_csrf_token = self.csrf_token
        if not request_csrf_token or request_csrf_token != server_csrf_token:
            self.write(json.dumps({"success": False, "message": "CSRF validation failed"}))
            self.finish()

    def initialize(self, session):
        self.session = session()

    def get(self):
        self.render('login.html', csrf_token=self.csrf_token)

    async def post(self):
        self.check_csrf_token()

        username = self.get_argument('username')
        password = self.get_argument('password')

        async with self.session as session:
            result = await session.execute(select(User).filter_by(username=username))
            existing_user = result.scalar_one_or_none()
        if existing_user and check_password_hash(existing_user.password, password):
            self.set_secure_cookie("user", username, expires_days=5)
            self.write(json.dumps({"success": True, "message": "登录成功", "redirect": "/profile"}))
        else:
            self.write(json.dumps({"success": False, "message": "用户名或密码错误"}))


class RegisterHandler(RequestHandler):
    def initialize(self, session):
        self.session = session()

    def get(self):
        self.render('register.html')

    async def post(self):
        username = self.get_argument('username')
        password = self.get_argument('password')
        confirm_password = self.get_argument('confirm_password')

        if password != confirm_password:
            self.write(json.dumps({"success": False, "message": "两次输入的密码不匹配，请重新输入。"}))
            return

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)

        async with self.session as session:
            try:
                result = await session.execute(select(User).filter_by(username=username))
                existing_user = result.scalar_one_or_none()

                if existing_user:
                    self.write(json.dumps({"success": False, "message": "用户名已存在，请选择其他用户名。"}))
                else:
                    session.add(new_user)
                    await session.commit()
                    self.write(json.dumps({"success": True}))
            except Exception as e:
                session.rollback()
                self.write(json.dumps({"success": False, "message": str(e)}))


class ProfileHandler(BaseHandler):
    def get(self):
        user = self.current_user
        if user:
            self.render("profile.html")
        else:
            self.redirect("/login")


class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.redirect("/login")
