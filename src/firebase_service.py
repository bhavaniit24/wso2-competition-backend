from src.category_service import CategoryService
from src.prompt_service import PromptService
from src.user_service import UserService
from src.app_service import AppService
from src.config import *
from src.models import *
from firebase_admin import credentials, firestore, initialize_app


class FirebaseService:
    def __init__(self):
        cred = credentials.Certificate(FIREBASE_PATH)
        initialize_app(cred)
        self.db = firestore.client()
        self.app_service = AppService(self.db)
        self.prompt_service = PromptService(self.db)
        self.category_service = CategoryService(self.db)
        self.user_service = UserService(self.db)

    def get_prompt(self, id):
        return self.prompt_service.get_prompt(id)

    def search_prompts(self, query=None, category=None):
        return self.prompt_service.search_prompts(query, category)

    def get_prompts_by_category(self, category):
        return self.prompt_service.get_prompts_by_category(category)

    def create_prompt(self, prompt: Prompt):
        return self.prompt_service.create_prompt(prompt)

    def update_prompt(self, prompt_id, new_prompt_data: Prompt):
        return self.prompt_service.update_prompt(prompt_id, new_prompt_data)

    def delete_prompt(self, id):
        return self.prompt_service.delete_prompt(id)

    def create_category(self, category: Category):
        return self.category_service.create_category(category)

    def update_category(self, id, category: Category):
        return self.category_service.update_category(id, category)

    def get_category(self, id: str):
        return self.category_service.get_category(id)

    def get_all_categories(self):
        return self.category_service.get_all_categories()

    def create_app(self, app_data: App):
        return self.app_service.create_app(app_data)

    def update_app(self, app_id: str, new_app_data: App):
        return self.app_service.update_app(app_id, new_app_data)

    def use_app(self, app: UseApp):
        return self.app_service.use_app(app)

    def search_apps(self, query=None, category=None):
        return self.app_service.search_apps(query, category)

    def create_user(self, user: User):
        return self.user_service.create_user(
            email=user.email,
            password=user.password,
            display_name=user.display_name,
            photo_url=user.photo_url,
            email_verified=user.email_verified,
            disabled=user.disabled,
        )

    def validate_user(self, user: ValidateUser):
        return self.user_service.validate_user(user.email, user.password)
