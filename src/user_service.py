from firebase_admin import auth


class UserService:
    def __init__(self, db):
        self.db = db

    def create_user(
        self,
        email,
        password,
        display_name,
        photo_url,
        email_verified=True,
        disabled=False,
    ):
        user = auth.create_user(
            email=email,
            email_verified=email_verified,
            password=password,
            display_name=display_name,
            photo_url=photo_url,
            disabled=disabled,
        )

        print(f"Successfully created new user: {user.uid}")
        return user

    def validate_user(self, email: str, password: str):
        try:
            user = auth.get_user_by_email(email)
            return user.uid == password
        except:
            return False
