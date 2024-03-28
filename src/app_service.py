from src.ai_service import AIService
from src.config import *
from src.models import *


class AppService:
    def __init__(self, db):
        self.db = db
        self.ai_service = AIService()

    def check_duplicate(self, ref, field, value):
        query = ref.where(field, ATTR_EQUAL, value)
        items = query.stream()
        return len(list(items)) > 0

    def get_category_doc_ref(self, id: str):
        return self.db.collection(FIREBASE_COLLECTION_CATEGORIES).document(id)

    def get_modified_app_json(self, id: str, name: str):
        return {PROMPT_ATTR_ID: id, PROMPT_ATTR_NAME: name}

    def create_app(self, app_data: App):
        apps_ref = self.db.collection(FIREBASE_COLLECTION_APPS)

        if self.check_duplicate(apps_ref, PROMPT_ATTR_NAME, app_data.name):
            print(f"The app with name '{app_data.name}' already exists.")
            return None

        category_refs = [
            self.db.collection(FIREBASE_COLLECTION_CATEGORIES).document(category_id)
            for category_id in app_data.categories
        ]

        data = {
            PROMPT_ATTR_NAME: app_data.name,
            PROMPT_ATTR_DESCRIPTION: app_data.description,
            PROMPT_ATTR_ICON: app_data.icon,
            PROMPT_ATTR_CATEGORIES: category_refs,
        }

        doc_ref = apps_ref.document()
        doc_ref.set(data)

        messages_collection = doc_ref.collection(FIREBASE_SUB_COLLECTION_MESSAGES)

        for message in app_data.messages:
            messages_collection.add(message.dict())

        return self.get_modified_app_json(doc_ref.id, app_data.name)

    def update_app(self, app_id: str, new_app_data: App):
        apps_ref = self.db.collection(FIREBASE_COLLECTION_APPS)
        app_ref = apps_ref.document(app_id)

        if not app_ref.get().exists:
            print(f"The app with ID '{app_id}' does not exist.")
            return None

        category_refs = [
            self.db.collection(FIREBASE_COLLECTION_CATEGORIES).document(category_id)
            for category_id in new_app_data.categories
        ]

        data = {
            PROMPT_ATTR_NAME: new_app_data.name,
            PROMPT_ATTR_DESCRIPTION: new_app_data.description,
            PROMPT_ATTR_ICON: new_app_data.icon,
            PROMPT_ATTR_CATEGORIES: category_refs,
        }

        doc_ref = apps_ref.document()
        doc_ref.set(data)

        messages_collection = doc_ref.collection(FIREBASE_SUB_COLLECTION_MESSAGES)
        messages = messages_collection.stream()

        for message in messages:
            message.reference.delete()

        for message in new_app_data.messages:
            messages_collection.add(message.dict())

        return self.get_modified_app_json(doc_ref.id, new_app_data.name)

    def get_app_by_id(self, id: str):
        apps_ref = self.db.collection(FIREBASE_COLLECTION_APPS)
        app_ref = apps_ref.document(id)

        if not app_ref.get().exists:
            print(f"The app with ID '{id}' does not exist.")
            return None

        data = app_ref.get().to_dict()
        category_refs = data[PROMPT_ATTR_CATEGORIES]
        category_names = [
            category_ref.get().to_dict()[PROMPT_ATTR_NAME]
            for category_ref in category_refs
        ]

        messages_collection = (
            self.db.collection(FIREBASE_COLLECTION_APPS)
            .document(id)
            .collection(FIREBASE_SUB_COLLECTION_MESSAGES)
        )
        messages = messages_collection.stream()

        app_data = {
            PROMPT_ATTR_ID: id,
            PROMPT_ATTR_NAME: data[PROMPT_ATTR_NAME],
            PROMPT_ATTR_DESCRIPTION: data[PROMPT_ATTR_DESCRIPTION],
            PROMPT_ATTR_ICON: data[PROMPT_ATTR_ICON],
            PROMPT_ATTR_CATEGORIES: [
                {
                    PROMPT_ATTR_ID: category_ref.id,
                    PROMPT_ATTR_NAME: category_name,
                }
                for category_ref, category_name in zip(category_refs, category_names)
            ],
            PROMPT_ATTR_MESSAGES: [
                {PROMPT_ATTR_ID: message.id, **message.to_dict()}
                for message in messages
            ],
        }

        return app_data

    def search_apps(self, query=None, category=None):
        apps_list = []
        apps_ref = self.db.collection(FIREBASE_COLLECTION_APPS)

        if category:
            category_ref = self.get_category_doc_ref(category)
            apps_ref = apps_ref.where(
                PROMPT_ATTR_CATEGORIES, ATTR_ARRAY_CONTAINS, category_ref
            )

        apps = apps_ref.stream()

        for app in apps:
            data = app.to_dict()
            category_refs = data[PROMPT_ATTR_CATEGORIES]
            category_names = [
                category_ref.get().to_dict()[PROMPT_ATTR_NAME]
                for category_ref in category_refs
            ]

            messages_collection = (
                self.db.collection(FIREBASE_COLLECTION_APPS)
                .document(app.id)
                .collection(FIREBASE_SUB_COLLECTION_MESSAGES)
            )
            messages = messages_collection.stream()

            apps_list.append(
                {
                    PROMPT_ATTR_ID: app.id,
                    PROMPT_ATTR_NAME: data[PROMPT_ATTR_NAME],
                    PROMPT_ATTR_DESCRIPTION: data[PROMPT_ATTR_DESCRIPTION],
                    PROMPT_ATTR_ICON: data[PROMPT_ATTR_ICON],
                    PROMPT_ATTR_CATEGORIES: [
                        {
                            PROMPT_ATTR_ID: category_ref.id,
                            PROMPT_ATTR_NAME: category_name,
                        }
                        for category_ref, category_name in zip(
                            category_refs, category_names
                        )
                    ],
                    PROMPT_ATTR_MESSAGES: [
                        {PROMPT_ATTR_ID: message.id, **message.to_dict()}
                        for message in messages
                    ],
                }
            )

        if query:
            new_apps_list = [
                app
                for app in apps_list
                if query.lower() in app[PROMPT_ATTR_NAME].lower()
            ]

            return new_apps_list

        return apps_list

    def replace_content(self, content_role_list, variable_list):
        updated_content_role_list = []
        for message in content_role_list:
            updated_message = message.copy()  # Create a copy of the original message
            if message["type"] == "text":
                for variable in message["variables"]:
                    placeholder = f"{{{variable['content']}}}"
                    if placeholder in updated_message["content"]:
                        for variable_obj in variable_list:
                            if variable_obj.id == variable["id"]:
                                updated_message["content"] = updated_message[
                                    "content"
                                ].replace(placeholder, variable_obj.content)
                                break
            updated_content_role_list.append(updated_message)
        return updated_content_role_list

    def use_app(self, use_app: UseApp):
        app = self.get_app_by_id(use_app.app_id)

        updated_content_role_list = self.replace_content(
            app["messages"], use_app.variables
        )

        role_mapping = {"user": "human", "assistant": "ai", "system": "system"}

        content_role_tuples = [
            (role_mapping.get(message["role"], message["role"]), message["content"])
            for message in updated_content_role_list
        ]

        return self.ai_service.send_custom_context_message(content_role_tuples)
