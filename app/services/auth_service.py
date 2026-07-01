from app.extensions import db, bcrypt
from app.models.user import User
from app.models.participant import Participant
from flask_login import login_user, logout_user


class AuthService:
    def login(self, email: str, password: str):
        """
        验证用户登录。
        返回: (success: bool, user: User|None, message: str)
        """
        user = User.query.filter_by(email=email).first()
        if user is None:
            return False, None, "No account found with this email."
        if not bcrypt.check_password_hash(user.password_hash, password):
            return False, None, "Incorrect password."
        login_user(user)
        return True, user, "Login successful."

    def signup(self, nickname: str, email: str, password: str,
               first_name: str, second_name: str,
               contact_number: str, street_address: str):
        """
        注册新用户（默认为 Participant 类型）。
        返回: (success: bool, user: User|None, message: str)
        """
        # 检查邮箱是否已注册
        existing = User.query.filter_by(email=email).first()
        if existing:
            return False, None, "This email is already registered."

        # 哈希密码
        password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

        # 创建 Participant（继承 User），默认注册用户都是 Participant
        new_user = Participant(
            nickname=nickname,
            email=email,
            password_hash=password_hash,
            contact_number=contact_number,
            street_address=street_address,
            first_name=first_name,
            second_name=second_name,
        )
        db.session.add(new_user)
        db.session.commit()
        return True, new_user, "Registration successful."

    def logout(self):
        """登出当前用户。"""
        logout_user()
        return True
